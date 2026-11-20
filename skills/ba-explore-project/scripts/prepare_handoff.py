#!/usr/bin/env python3
"""Validate an agent-authored exploration inventory; render raw BA handoff files.

Renders exploration documents from an inventory authored by the agent.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
COMMON = SKILL / "references/kit/scripts"
if not COMMON.is_dir():
    COMMON = SKILL.parents[1] / "scripts"
sys.path.insert(0, str(COMMON))
from ba_core import BAError, Project, sha
from jsonschema import Draft202012Validator


def load_json(path):
    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"Duplicate JSON key: {key}")
            value[key] = item
        return value
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=unique)
    except (ValueError, OSError) as exc:
        raise BAError("INVALID_INVENTORY", str(exc), path) from exc


def validate_inventory(project, inventory_path):
    path = project.temporary_path(inventory_path)
    digest = sha(path) if path.is_file() else None
    data = load_json(path)
    contract = load_json(SKILL / "references/exploration.schema.json")
    errors = list(Draft202012Validator(contract).iter_errors(data))
    if errors:
        error = errors[0]
        raise BAError("SCHEMA_INVALID", error.message, path, "/" + "/".join(map(str, error.absolute_path)))
    if data["project_id"] != project.config["project_id"]:
        raise BAError("PROJECT_MISMATCH", "Inventory belongs to another project", path)
    paths = {}
    for item in data["source_files"]:
        source = project.path(item["path"])
        if source == path or source in paths:
            raise BAError("DUPLICATE_SOURCE", "Duplicate or self-referencing inventory source", source)
        if not source.is_file():
            raise BAError("MISSING_INPUT", "Evidence source is missing", source)
        if sha(source) != item["sha256"]:
            raise BAError("STALE_INPUT", "Evidence bytes changed; re-explore before refreshing hashes", source)
        paths[source] = item["sha256"]
    for scoped in data["scope"]["scanned_paths"]:
        if not project.path(scoped).exists():
            raise BAError("MISSING_INPUT", "Scanned path no longer exists", scoped)
    for skipped in data["scope"]["skipped"]:
        project.path(skipped["path"])
    evidence = {}
    for item in data["evidence"]:
        identifier = item["evidence_id"]
        if identifier in evidence:
            raise BAError("DUPLICATE_ID", identifier, path)
        source = project.path(item["path"])
        if source not in paths:
            raise BAError("UNHASHED_EVIDENCE", "Evidence must reference a fingerprinted source file", source)
        try:
            count = len(source.read_text(encoding="utf-8-sig").splitlines())
        except UnicodeError as exc:
            raise BAError("INVALID_ENCODING", "Line evidence expects UTF-8 text", source) from exc
        if not item["start_line"] <= item["end_line"] <= count:
            raise BAError("INVALID_EVIDENCE_RANGE", identifier, source)
        evidence[identifier] = item
    features = {}
    for feature in data["features"]:
        identifier = feature["feature_id"]
        if identifier in features:
            raise BAError("DUPLICATE_ID", identifier, path)
        features[identifier] = feature
        refs = set(feature["evidence_refs"])
        if refs - evidence.keys():
            raise BAError("BROKEN_REF", f"Unknown evidence: {sorted(refs - evidence.keys())}", path)
        kinds = {evidence[ref]["kind"] for ref in refs}
        level = feature["verification"]
        if level in ("STATIC_IMPLEMENTATION", "RUNTIME_VERIFIED") and "implementation" not in kinds:
            raise BAError("UNSUPPORTED_VERIFICATION", "Implementation evidence required for this verification level", path)
        if level == "RUNTIME_VERIFIED" and "runtime_result" not in kinds:
            raise BAError("UNSUPPORTED_VERIFICATION", "Runtime verification requires actual result evidence, not just tests", path)
        if level == "UI_ONLY" and "ui" not in kinds:
            raise BAError("UNSUPPORTED_VERIFICATION", "UI_ONLY requires UI evidence", path)
        if level in ("UNKNOWN", "UI_ONLY", "MOCK", "PARTIAL") and not (feature["gaps"] or feature["open_questions"]):
            raise BAError("MISSING_LIMITATION", "Incomplete verification requires gaps or open questions", path)
        for collection in ("behaviors", "flows", "rules", "data", "permissions"):
            for claim in feature[collection]:
                if set(claim["evidence_refs"]) - refs:
                    raise BAError("BROKEN_REF", "Claim references evidence outside this feature", path)
    for feature in features.values():
        if set(feature["dependencies"]) - features.keys() or feature["feature_id"] in feature["dependencies"]:
            raise BAError("BROKEN_REF", "Invalid feature dependency", path)
    if sha(path) != digest:
        raise BAError("STALE_INPUT", "Inventory changed during validation", path)
    return data, {path: digest, **paths}


def bullet(values):
    return "\n".join("- " + str(v) for v in values) or "- Chưa ghi nhận; không suy ra là không tồn tại."


def render_outputs(data):
    sections = []
    for feature in data["features"]:
        details = []
        for field in ("behaviors", "flows", "rules", "data", "permissions"):
            claims = [f"{c['text']} [{c['confirmation_status']}; {', '.join(c['evidence_refs'])}]" for c in feature[field]]
            details.append(f"### {field}\n\n{bullet(claims)}")
        sections.append(f"## {feature['feature_id']} — {feature['name']}\n\n"
                        f"Module: {feature['module']} | Availability: {feature['availability']} | Verification: {feature['verification']}\n\n"
                        f"Actors: {', '.join(feature['actors']) or 'Chưa rõ'}\n\nEntry points:\n{bullet(feature['entry_points'])}\n\n"
                        f"Evidence: {', '.join(feature['evidence_refs'])}\n\n" + "\n\n".join(details) +
                        f"\n\n### Gaps\n\n{bullet(feature['gaps'])}\n\n### Open Questions\n\n{bullet(feature['open_questions'])}\n\n"
                        f"Dependencies: {', '.join(feature['dependencies']) or 'Chưa ghi nhận'}")
    evd = [f"{e['evidence_id']}: {e['path']}:{e['start_line']}-{e['end_line']} ({e['symbol']}, {e['kind']}) — {e['observation']}"
           + (" | Runtime: " + json.dumps(e["runtime"], ensure_ascii=False) if "runtime" in e else "") for e in data["evidence"]]
    hashes = [s["path"] + " — SHA-256 " + s["sha256"] for s in data["source_files"]]
    report = ("# Khảo sát hiện trạng dự án\n\n" + data["summary"] +
              "\n\n## Phạm vi\n\n" + data["scope"]["requested"] + "\n\nĐã khảo sát:\n" + bullet(data["scope"]["scanned_paths"]) +
              "\n\nBỏ qua:\n" + bullet([s["path"] + ": " + s["reason"] for s in data["scope"]["skipped"]]) +
              "\n\n" + "\n\n".join(sections) + "\n\n## Evidence\n\n" + bullet(evd) +
              "\n\n## Source fingerprints\n\n" + bullet(hashes) + "\n\n## Limitations\n\n" + bullet(data["limitations"]) +
              "\n\n## Change history\n\n" + json.dumps(data["change_history"], ensure_ascii=False, indent=2) + "\n")
    brief = ("# Đầu vào cho ba-brainstorm — tài liệu hóa sản phẩm hiện có\n\n"
             "Mục tiêu: lập hồ sơ BA cho hành vi hiện hữu, không đề nghị xây mới các feature đã có.\n"
             "Đọc project-exploration.json và project-exploration.md cùng thư mục; giữ EXF/EVD refs.\n"
             "Giữ mức xác minh của từng tính năng, gồm phần chỉ có giao diện hoặc dữ liệu mẫu.\n"
             "Nguồn được hash trực tiếp trong brainstorm dạng kind: raw để downstream phát hiện stale code.\n"
             "Dùng phạm vi được nêu trong yêu cầu và ghi điều chưa rõ vào tài liệu.\n\n" + report +
             "\n## Tiếp theo\n\nDùng ba-workflow để lập backlog, Round, viết và kiểm tra các PBI rồi xuất hai file cho mỗi PBI.\n")
    return report, brief


def prepare(project, inventory_path, write=False):
    path = project.path(inventory_path)
    data, snapshot = validate_inventory(project, path)
    outputs = dict(zip(("project-exploration.md", "exploration-brief.md"), render_outputs(data)))
    plan = []
    for name, text in outputs.items():
        target = project.path(path.parent / name)
        if target in snapshot:
            raise BAError("SOURCE_OUTPUT_CONFLICT", "Generated output is also listed as source", target)
        content = text.encode("utf-8")
        if target.exists() and target.read_bytes() != content:
            raise BAError("EXPLORATION_CONFLICT", "Output differs; reconcile changes without blind overwrite", target)
        plan.append({"path": project.relative(target), "action": "skip" if target.exists() else "create"})
    for source, expected in snapshot.items():
        if sha(source) != expected:
            raise BAError("STALE_INPUT", "Evidence changed before handoff", source)
    if write:
        for item in plan:
            if item["action"] == "create":
                target = project.path(item["path"])
                # Exclusive create prevents concurrent overwrite; partial output remains visible on IO failure.
                with target.open("xb") as stream:
                    stream.write(outputs[target.name].encode("utf-8"))
        for source, expected in snapshot.items():
            if sha(source) != expected:
                raise BAError("STALE_INPUT", "Evidence changed during handoff write; do not consume outputs", source)
    import hashlib
    handoff = [{"path": project.relative(source), "sha256": digest, "kind": "raw"} for source, digest in snapshot.items()]
    handoff.extend({"path": project.relative(path.parent / name), "sha256": hashlib.sha256(content.encode("utf-8")).hexdigest(), "kind": "raw"}
                   for name, content in outputs.items())
    return {"result": "PASS", "written": write, "features": len(data["features"]), "outputs": plan,
            "source_documents": handoff,
            "next_skill": "ba-brainstorm", "note": "Future output hashes on dry-run; consume only after --write and validation."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-config", help="Path to .temp/ba-project.yaml (defaults to this path in the working directory)")
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        result = prepare(Project.load(args.project_config), args.inventory, args.write)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (BAError, OSError) as exc:
        diagnostic = exc.diagnostic if isinstance(exc, BAError) else BAError("IO_ERROR", str(exc), args.inventory).diagnostic
        print(json.dumps({"result": "FAIL", "diagnostics": [diagnostic]}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
