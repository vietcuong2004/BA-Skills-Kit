#!/usr/bin/env python3
"""Dry-run by default; publish an approved, validated PBI pair without overwriting."""
import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path

from ba_core import BAError, Project, Validator, check_output_layout, errors_for, sha, slugify
from ba_public import public_bytes


def read_approvals(project, path):
    path = project.temporary_path(path)
    if not path.is_file():
        raise BAError("MISSING_APPROVAL", "Human checkpoint record is missing", path,
                      fix="Ghi quyết định thực tế của người dùng theo approvals.schema.json; không tự tạo phê duyệt.")
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (ValueError, OSError) as exc:
        raise BAError("INVALID_APPROVAL", str(exc), path) from exc
    issues = errors_for("approvals", data, path)
    if issues or data["project_id"] != project.config["project_id"]:
        raise BAError("INVALID_APPROVAL", issues[0]["message"] if issues else "Wrong project", path)
    return data["approvals"]


def checkpoint(project, approvals, name, allowed, paths, pbi_id=None):
    needed = {(project.relative(p), sha(p)) for p in paths}
    for record in reversed(approvals):
        if record["checkpoint"] != name or record["decision"] not in allowed:
            continue
        if pbi_id and pbi_id not in record["pbi_refs"]:
            continue
        supplied = {(project.relative(project.path(s["path"])), s["sha256"]) for s in record["documents"]}
        if needed.issubset(supplied):
            return record
    raise BAError("MISSING_APPROVAL", f"No current human {name} approval covering these bytes", paths[0],
                  fix="Trình manifest và blockers cho người dùng; ghi approval gắn hash sau quyết định rõ ràng.")


def prepare(project, pbi_id, approvals_path=None):
    check_output_layout(project)
    if not __import__("re").fullmatch(__import__("re").escape(project.config["pbi_prefix"]) + r"-[0-9]{3,}", pbi_id):
        raise BAError("PBI_MISMATCH", "An exact configured PBI ID is required", pbi_id)
    validator = Validator(project)
    backlog = validator.require_valid(project.planning / "product-backlog.md", "product-backlog")
    plan = validator.require_valid(project.planning / "round-plan.md", "round-plan")
    matches = [p for p in backlog.data["pbis"] if p["pbi_id"] == pbi_id]
    if len(matches) != 1:
        raise BAError("PBI_MISMATCH", "PBI must occur exactly once in backlog", backlog.path)
    pbi = matches[0]
    rounds = [r for r in plan.data["rounds"] if pbi_id in r["pbi_refs"]]
    if len(rounds) != 1:
        raise BAError("ROUND_MISMATCH", "PBI must have exactly one active Round", plan.path)
    rnd = rounds[0]
    business = validator.require_valid(project.planning / "drafts" / pbi_id / "business.md", "business", pbi_id)
    spec = validator.require_valid(project.planning / "drafts" / pbi_id / "spec.md", "spec", pbi_id)
    review = validator.require_valid(project.planning / "reviews" / f"{pbi_id}-review.md", "review", pbi_id)
    specified_sources = {(project.relative(project.path(s["path"])), s["sha256"]) for s in spec.metadata["source_documents"]}
    if (project.relative(business.path), sha(business.path)) not in specified_sources:
        raise BAError("SPEC_SOURCE_MISMATCH", "Spec does not use the selected business draft bytes", spec.path)
    for doc in (business, spec, review):
        if doc.data.get("round_id") != rnd["round_id"]:
            raise BAError("ROUND_MISMATCH", "Set current round_id and re-review before publish", doc.path)
    # The direct review sources must be exactly these drafts, not another valid lookalike.
    reviewed = {(project.relative(project.path(s["path"])), s["sha256"]) for s in review.metadata["source_documents"]}
    if not {(project.relative(d.path), sha(d.path)) for d in (business, spec)}.issubset(reviewed):
        raise BAError("REVIEW_SOURCE_MISMATCH", "Review does not cover selected draft bytes", review.path)
    if review.data["result"] == "FAIL" or any(d.data["blockers"] for d in (business, spec, review)):
        raise BAError("PUBLISH_BLOCKED", "Review FAIL or unresolved business blockers", review.path)
    target = project.path(Path(project.config["output_root"]) / rnd["round_id"] / f"{pbi_id}-{slugify(pbi['title'])}")
    output_root = project.path(project.config["output_root"])
    if output_root.exists():
        for folder in output_root.glob(f"*/{pbi_id}-*"):
            candidate = project.path(folder)
            if candidate != target:
                raise BAError("ROUND_TRANSFER_CONFLICT", "Existing PBI path requires an explicit migration/history decision", candidate)
    entries = []
    if target.exists() and (not target.is_dir() or {p.name for p in target.iterdir()} != {"business.md", "spec.md"}):
        raise BAError("PUBLISH_CONFLICT", "Existing PBI directory must contain exactly the two expected files", target)
    for doc in (business, spec):
        destination = project.path(target / doc.path.name)
        digest = hashlib.sha256(public_bytes(project, doc, validator)).hexdigest()
        action = "create" if not destination.exists() else "skip" if sha(destination) == digest else "conflict"
        entries.append({"source": project.relative(doc.path), "destination": project.relative(destination),
                        "source_sha256": sha(doc.path), "sha256": digest, "action": action})
    diagnostics = []
    try:
        approvals = read_approvals(project, approvals_path or project.planning / "approvals.json")
        checkpoint(project, approvals, "backlog", {"Approved"}, [backlog.path])
        checkpoint(project, approvals, "round-plan", {"Approved", "Proposed Allowed"}, [plan.path])
        allowed = {"Draft Publication"} if review.data["result"] == "CONDITIONAL" else {"Approved", "Draft Publication"}
        decision = checkpoint(project, approvals, "publish", allowed,
                              [backlog.path, plan.path, business.path, spec.path, review.path], pbi_id)
        if decision["decision"] == "Draft Publication" and any(d.metadata["status"] == "approved" for d in (business, spec)):
            raise BAError("APPROVAL_STATUS_MISMATCH", "Draft publication must retain draft/in_review status", target)
    except BAError as exc:
        diagnostics.append(exc.diagnostic)
    if any(e["action"] == "conflict" for e in entries):
        diagnostics.append(BAError("PUBLISH_CONFLICT", "Existing content differs; no overwrite was performed", target,
            fix="So sánh bản cũ/mới và thống nhất cách lưu lịch sử; công cụ này không tự ghi đè hoặc di chuyển.").diagnostic)
    snapshot = {project.relative(p): digest for p, digest in validator.fingerprints.items()}
    approval_file = project.path(approvals_path or project.planning / "approvals.json")
    if approval_file.is_file():
        snapshot[project.relative(approval_file)] = sha(approval_file)
    config_digest = sha(project.config_path)
    return {"pbi_id": pbi_id, "round_id": rnd["round_id"], "target": project.relative(target), "format": "pbi-template-v1", "entries": entries,
            "blocked": diagnostics, "snapshot": snapshot, "config_sha256": config_digest}


def publish(project, manifest):
    if manifest["blocked"]:
        raise BAError("PUBLISH_BLOCKED", "Dry-run has blocking diagnostics", manifest["target"])
    if sha(project.config_path) != manifest["config_sha256"]:
        raise BAError("STALE_INPUT", "Config changed after dry-run", project.config_path)
    check_output_layout(project)
    for path, expected in manifest["snapshot"].items():
        if sha(project.path(path)) != expected:
            raise BAError("STALE_INPUT", "Input changed after dry-run", path)
    target = project.path(manifest["target"])
    if all(e["action"] == "skip" for e in manifest["entries"]):
        if {p.name for p in target.iterdir()} != {"business.md", "spec.md"}:
            raise BAError("PUBLISH_CONFLICT", "Target changed after dry-run", target)
        for entry in manifest["entries"]:
            if sha(project.path(entry["destination"])) != entry["sha256"]:
                raise BAError("PUBLISH_CONFLICT", "Target bytes changed after dry-run", target)
        return {"created": [], "updated": [], "skipped": [e["destination"] for e in manifest["entries"]], "blocked": [], "conflicts": []}
    if target.exists():
        raise BAError("PUBLISH_CONFLICT", "Target appeared after dry-run", target)
    # Keep even temporary staging outside output_root. Cross-filesystem rename fails safely.
    stage_root = project.temporary_path(project.temp / "publish-staging")
    stage_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="pair-", dir=stage_root) as temp:
        staging = Path(temp) / "pair"
        staging.mkdir()
        for entry in manifest["entries"]:
            source = project.path(entry["source"])
            if sha(source) != entry["source_sha256"]:
                raise BAError("STALE_INPUT", "Draft changed after dry-run", source)
            validator = Validator(project)
            doc = validator.require_valid(source, Path(entry["destination"]).stem, manifest["pbi_id"])
            content = public_bytes(project, doc, validator)
            staged_file = staging / Path(entry["destination"]).name
            staged_file.write_bytes(content)
            if sha(staged_file) != entry["sha256"]:
                raise BAError("STALE_INPUT", "Rendered document changed after dry-run", entry["source"])
        for path, expected in manifest["snapshot"].items():
            if sha(project.path(path)) != expected:
                raise BAError("STALE_INPUT", "Input changed during staging", path)
        if sha(project.config_path) != manifest["config_sha256"]:
            raise BAError("STALE_INPUT", "Config changed during staging", project.config_path)
        # mkdir would reserve an empty target, but two-step copy could expose a partial pair.
        # Windows rename refuses an existing target; on POSIX guard existing paths immediately before rename.
        if target.exists():
            raise BAError("PUBLISH_CONFLICT", "Target created concurrently", target)
        check_output_layout(project)
        target.parent.mkdir(parents=True, exist_ok=True)
        os.rename(staging, target)
    validator = Validator(project)
    for entry in manifest["entries"]:
        path = project.path(entry["destination"])
        if sha(path) != entry["sha256"]:
            raise BAError("POST_PUBLISH_FAILED", "Published bytes differ", path)
        validator.require_valid(path, Path(entry["destination"]).stem, manifest["pbi_id"])
    if {p.name for p in target.iterdir()} != {"business.md", "spec.md"}:
        raise BAError("POST_PUBLISH_FAILED", "Unexpected file in published PBI", target)
    check_output_layout(project)
    return {"created": [e["destination"] for e in manifest["entries"]], "updated": [], "skipped": [], "blocked": [], "conflicts": []}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-config", help="Explicit config; default: .temp/ba-project.yaml, then legacy ba-project.yaml in CWD")
    parser.add_argument("--pbi-id", required=True)
    parser.add_argument("--approvals")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        project = Project.load(args.project_config)
        manifest = prepare(project, args.pbi_id, args.approvals)
        result = publish(project, manifest) if args.apply else manifest
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get("blocked") else 0
    except (BAError, OSError) as exc:
        issue = exc.diagnostic if isinstance(exc, BAError) else BAError("IO_ERROR", str(exc)).diagnostic
        print(json.dumps({"blocked": [issue]}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
