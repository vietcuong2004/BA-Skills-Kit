#!/usr/bin/env python3
"""Read-only check that published output contains only Round/PBI pairs; no moving/deleting."""
import argparse
import json
from ba_core import BAError, Project, Validator, check_output_layout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-config", required=True)
    parser.add_argument("--check-documents", action="store_true", help="Also validate published metadata, refs and source freshness")
    args = parser.parse_args()
    try:
        project = Project.load(args.project_config)
        check_output_layout(project)
        validator = Validator(project)
        if args.check_documents and project.output.exists():
            for file in sorted(project.output.glob("*/*/*.md")):
                validator.validate(file, expected_type=file.stem)
        result = {"result": "PASS" if validator.ok else "FAIL", "planning_dir": project.relative(project.planning),
                  "output_root": project.relative(project.output), "diagnostics": validator.diagnostics}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if validator.ok else 1
    except (BAError, OSError) as exc:
        issue = exc.diagnostic if isinstance(exc, BAError) else BAError("IO_ERROR", str(exc)).diagnostic
        print(json.dumps({"result": "FAIL", "diagnostics": [issue]}, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
