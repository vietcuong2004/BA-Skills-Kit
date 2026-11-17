#!/usr/bin/env python3
"""Create an installable ZIP with a SHA-256 manifest, excluding local tests and caches."""
import json
import zipfile
from pathlib import Path
from ba_core import KIT, sha


def main():
    files = [KIT / name for name in ("README.md", "GUIDE_EXISTING_PROJECT.md", "GUIDE_NEW_PROJECT.md", "AGENTS.md", "CLAUDE.md", "SKILL.md", "INSTALL.md", "requirements-kit.txt", ".gitignore")]
    for folder in ("templates", "conventions", "contracts", "scripts", "skills"):
        files.extend(p for p in (KIT / folder).rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
    manifest = {p.relative_to(KIT).as_posix(): sha(p) for p in sorted(files)}
    destination = KIT / "dist"
    destination.mkdir(exist_ok=True)
    archive = destination / "BA-Skills-Kit.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(files):
            z.write(path, "BA-Skills-Kit/" + path.relative_to(KIT).as_posix())
        z.writestr("BA-Skills-Kit/KIT-MANIFEST.json", json.dumps({"kit_version": "1.0", "files": manifest}, ensure_ascii=False, indent=2))
    digest = sha(archive)
    (destination / "BA-Skills-Kit.zip.sha256").write_text(digest + "  BA-Skills-Kit.zip\n", encoding="utf-8")
    print(json.dumps({"archive": str(archive), "files": len(files), "sha256": digest, "bytes": archive.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
