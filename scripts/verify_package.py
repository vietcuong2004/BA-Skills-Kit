#!/usr/bin/env python3
"""Smoke-check an extracted package and its installed private runtime resources."""
import json
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from ba_core import KIT, sha


def main():
    archive = KIT / "dist/BA-Skills-Kit.zip"
    with tempfile.TemporaryDirectory(prefix="ba-package-") as temp:
        destination = Path(temp)
        with zipfile.ZipFile(archive) as z:
            if z.testzip():
                raise ValueError("ZIP CRC failure")
            for name in z.namelist():
                if not (destination / name).resolve().is_relative_to(destination):
                    raise ValueError("Unsafe ZIP member")
            z.extractall(destination)
        extracted = destination / "BA-Skills-Kit"
        manifest = json.loads((extracted / "KIT-MANIFEST.json").read_text(encoding="utf-8"))
        for name, expected in manifest["files"].items():
            if sha(extracted / name) != expected:
                raise ValueError(f"Manifest mismatch: {name}")
        config = extracted / "tests/fixtures/agent-notes/ba-project.yaml"
        spec = extracted / "tests/fixtures/agent-notes/.specify/_planning/drafts/PBI-001/spec.md"
        commands = [
            [sys.executable, "-X", "utf8", str(extracted / "scripts/validate_ba_document.py"), "--project-config", str(config), "--file", str(spec), "--check-refs", "--format", "json"],
            [sys.executable, "-X", "utf8", str(extracted / "scripts/install_skills.py"), "--project-root", str(destination / "target"), "--apply"],
            [sys.executable, "-X", "utf8", str(destination / "target/.agents/skills/ba-spec/references/kit/scripts/validate_ba_document.py"), "--project-config", str(config), "--file", str(spec), "--check-refs", "--format", "json"],
        ]
        for command in commands:
            result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=30)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)
        report = {"result": "PASS", "archive_sha256": sha(archive), "manifest_files": len(manifest["files"]),
                  "checks": ["ZIP CRC", "per-file SHA-256", "extracted validator", "portable installation", "installed validator with private contracts"]}
    (KIT / "dist/package-verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
