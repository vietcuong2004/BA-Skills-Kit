#!/usr/bin/env python3
"""Install portable BA skills with private contract resources. Dry-run unless --apply."""
import argparse
import json
import os
import tempfile
from pathlib import Path
from ba_core import BAError, KIT, safe_path, sha

RUNTIME = ["ba_core.py", "ba_public.py", "validate_ba_document.py", "publish_ba.py", "workflow_state.py", "check_ba_layout.py"]
MARKER = ".ba-kit-install.json"


def payload(skill):
    files = {}
    for path in skill.rglob("*"):
        if path.is_file() and "__pycache__" not in path.parts:
            content = path.read_bytes()
            if path.name == "SKILL.md":
                text = content.decode("utf-8")
                for folder in ("conventions", "contracts", "templates"):
                    text = text.replace(f"../../{folder}/", f"references/kit/{folder}/")
                content = text.encode("utf-8")
            files[path.relative_to(skill).as_posix()] = content
    for folder in ("contracts", "conventions", "templates"):
        for path in (KIT / folder).rglob("*"):
            if path.is_file():
                files[f"references/kit/{path.relative_to(KIT).as_posix()}"] = path.read_bytes()
    for name in RUNTIME:
        files[f"references/kit/scripts/{name}"] = (KIT / "scripts" / name).read_bytes()
    files["references/kit/requirements-kit.txt"] = (KIT / "requirements-kit.txt").read_bytes()
    return files


def plan_install(destination, update=False):
    import hashlib
    destination = Path(destination).resolve()
    result = []
    for skill in sorted((KIT / "skills").glob("ba-*")):
        files = payload(skill)
        hashes = {name: hashlib.sha256(content).hexdigest() for name, content in files.items()}
        target = safe_path(destination, skill.name)
        action, conflicts = "create", []
        if target.exists():
            marker = safe_path(destination, target / MARKER)
            try:
                old = json.loads(marker.read_text(encoding="utf-8"))["files"]
            except (ValueError, OSError, KeyError):
                old = {}
                conflicts.append("Existing folder is not a managed BA installation")
            for name, digest in old.items():
                path = safe_path(target, name)
                if not path.is_file() or sha(path) != digest:
                    conflicts.append(f"Locally modified/missing file: {name}")
            existing = {p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
            if existing - set(old) - {MARKER}:
                conflicts.append("Unmanaged files exist; preserve and resolve manually")
            if set(old) - set(hashes):
                conflicts.append("Update would remove files; preserve and resolve manually")
            same = old == hashes and not conflicts
            action = "skip" if same else "update" if update and not conflicts else "conflict"
        result.append({"skill": skill.name, "target": str(target), "action": action, "conflicts": conflicts, "files": hashes})
    return result


def install(destination, *, apply=False, update=False):
    plan = plan_install(destination, update)
    if any(item["action"] == "conflict" for item in plan):
        raise BAError("INSTALL_CONFLICT", json.dumps([{k: v for k, v in i.items() if k != "files"} for i in plan]), destination)
    if not apply:
        return plan
    # Re-plan immediately before mutation. Do not overwrite locally modified skill resources.
    if plan_install(destination, update) != plan:
        raise BAError("INSTALL_CONFLICT", "Installation changed after dry-run", destination)
    for item in plan:
        if item["action"] == "skip":
            continue
        target = Path(item["target"])
        target.parent.mkdir(parents=True, exist_ok=True)
        files = payload(KIT / "skills" / item["skill"])
        files[MARKER] = json.dumps({"kit_version": "1.0", "files": item["files"]}, indent=2).encode("utf-8")
        if item["action"] == "create":
            with tempfile.TemporaryDirectory(prefix=".ba-install-", dir=target.parent) as temp:
                stage = Path(temp) / item["skill"]
                for name, content in files.items():
                    path = safe_path(stage, name)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(content)
                if target.exists():
                    raise BAError("INSTALL_CONFLICT", "Destination appeared concurrently", target)
                os.rename(stage, target)
        else:
            # Keep other skills untouched. Updates are explicit and only managed unchanged files are replaced.
            for name, content in files.items():
                path = safe_path(target, name)
                path.parent.mkdir(parents=True, exist_ok=True)
                with tempfile.NamedTemporaryFile(prefix=".ba-update-", dir=path.parent, delete=False) as stream:
                    stream.write(content)
                    temp = Path(stream.name)
                os.replace(temp, path)
    return plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--project-root", help="Install into PROJECT/.agents/skills")
    group.add_argument("--skills-dir", help="Explicit discovery directory, e.g. ~/.agents/skills")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()
    destination = Path(args.project_root) / ".agents" / "skills" if args.project_root else Path(args.skills_dir).expanduser()
    try:
        result = install(destination, apply=args.apply, update=args.update)
        print(json.dumps([{k: v for k, v in i.items() if k != "files"} for i in result], ensure_ascii=False, indent=2))
        return 0
    except (BAError, OSError) as exc:
        print(json.dumps({"diagnostics": [exc.diagnostic if isinstance(exc, BAError) else BAError("IO_ERROR", str(exc)).diagnostic]}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
