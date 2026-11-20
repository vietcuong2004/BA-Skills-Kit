#!/usr/bin/env python3
"""Validate a BA Markdown contract without modifying files."""
import argparse
import json
from ba_core import BAError, Project, Validator


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-config", help="Path to .temp/ba-project.yaml (defaults to this path in the working directory)")
    parser.add_argument("--file", required=True)
    parser.add_argument("--check-refs", action="store_true")
    parser.add_argument("--expected-type")
    parser.add_argument("--pbi-id")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    try:
        validator = Validator(Project.load(args.project_config), args.check_refs)
        validator.validate(args.file, args.expected_type, args.pbi_id)
        diagnostics = validator.diagnostics
    except (BAError, OSError) as exc:
        diagnostics = [exc.diagnostic if isinstance(exc, BAError) else BAError("IO_ERROR", str(exc), args.file).diagnostic]
    passed = not any(d["severity"] == "ERROR" for d in diagnostics)
    result = {"result": "PASS" if passed else "FAIL", "diagnostics": diagnostics}
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["result"])
        for d in diagnostics:
            print(f"{d['severity']} {d['code']} {d['file']}:{d['location']} {d['message']} | {d['suggested_fix']}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
