#!/usr/bin/env python3
"""Smoke-check an extracted package and its installed private runtime resources."""
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from ba_core import KIT, sha, render, HEADINGS


def main():
    archive = KIT / "dist/BA-Skills-Kit.zip"
    with tempfile.TemporaryDirectory(prefix="ba-package-") as temp:
        destination = Path(temp)
        with zipfile.ZipFile(archive) as z:
            if z.testzip():
                raise ValueError("ZIP CRC failure")
            if any(name.startswith("BA-Skills-Kit/tests/") for name in z.namelist()):
                raise ValueError("Local tests must not be included in the installation package")
            for name in z.namelist():
                if not (destination / name).resolve().is_relative_to(destination):
                    raise ValueError("Unsafe ZIP member")
            z.extractall(destination)
        extracted = destination / "BA-Skills-Kit"
        for name in ("README.md", "GUIDE_EXISTING_PROJECT.md", "GUIDE_NEW_PROJECT.md", "INSTALL.md"):
            if not (extracted / name).is_file():
                raise ValueError(f"Missing user guide: {name}")
        manifest = json.loads((extracted / "KIT-MANIFEST.json").read_text(encoding="utf-8"))
        for name, expected in manifest["files"].items():
            if sha(extracted / name) != expected:
                raise ValueError(f"Manifest mismatch: {name}")
        # A disposable smoke document avoids depending on local tests/ in distributed packages.
        project = destination / "smoke-project"
        project.mkdir()
        config = project / ".temp/ba-project.yaml"
        config.parent.mkdir()
        config.write_bytes((extracted / "templates/ba-project.example.yaml").read_bytes())
        idea = project / ".temp/inputs/idea.txt"
        idea.parent.mkdir(parents=True, exist_ok=True)
        idea.write_text("Smoke-check a notes discovery document.", encoding="utf-8")
        fact = {"text": "Synthetic package smoke check", "confirmation_status": "Proposed", "source_refs": [".temp/inputs/idea.txt"]}
        data = {"product_overview": fact, "vision": fact, "target_users": ["User"], "problems": [fact],
                "jobs_to_be_done": [fact], "capabilities": [{"capability_id": "CAP-001", "name": "Note capture",
                    "description": "Capture a note", "target_users": ["User"], "business_value": "Remember information",
                    "source_refs": [".temp/inputs/idea.txt"], "confirmation_status": "Proposed"}],
                "goals": [fact], "scope": [fact], "exclusions": [], "constraints": [], "assumptions": [],
                "open_questions": [], "metrics": [], "change_history": []}
        metadata = {"schema_version": "1.0", "document_type": "brainstorm", "project_id": "example-notes",
                    "status": "draft", "generated_by": "ba-brainstorm", "source_documents": [{"path": ".temp/inputs/idea.txt", "sha256": sha(idea), "kind": "raw"}]}
        document = project / ".temp/brainstorm.md"
        document.write_text(render(metadata, data, {h: "Synthetic smoke check." for h in HEADINGS["brainstorm"]}), encoding="utf-8")
        commands = [
            [sys.executable, "-X", "utf8", str(extracted / "scripts/validate_ba_document.py"), "--project-config", str(config), "--file", str(document), "--check-refs", "--format", "json"],
            [sys.executable, "-X", "utf8", str(extracted / "scripts/install_skills.py"), "--project-root", str(destination / "target"), "--apply"],
            [sys.executable, "-X", "utf8", str(destination / "target/.agents/skills/ba-spec/references/kit/scripts/validate_ba_document.py"), "--project-config", str(config), "--file", str(document), "--check-refs", "--format", "json"],
            [sys.executable, "-X", "utf8", str(destination / "target/.agents/skills/ba-publish/references/kit/scripts/check_ba_layout.py"), "--project-config", str(config), "--check-documents"],
        ]
        for command in commands:
            result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=30)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)
        # Verify the installed helper also discovers the config when no path is passed.
        installed_auditor = destination / "target/.agents/skills/ba-publish/references/kit/scripts/check_ba_layout.py"
        detected = subprocess.run([sys.executable, "-X", "utf8", str(installed_auditor)], cwd=project,
                                  capture_output=True, text=True, encoding="utf-8", timeout=30)
        if detected.returncode or json.loads(detected.stdout)["planning_dir"] != ".temp":
            raise RuntimeError(detected.stdout + detected.stderr)
        if (project / "ba-project.yaml").exists() or (project / ".temp/.temp").exists() or (project / ".temp/.specify").exists():
            raise ValueError("Config discovery created an incorrect nested/root project layout")
        report = {"result": "PASS", "archive_sha256": sha(archive), "manifest_files": len(manifest["files"]),
                  "checks": ["ZIP CRC", "no local tests in package", "user guides included", "per-file SHA-256", "extracted validator", "portable installation", "installed validator with private contracts", "installed output layout auditor", "auto-discovered .temp config without root config"]}
    (KIT / "dist/package-verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
