#!/usr/bin/env python3
"""Inspect saved state and invalidate changed outputs; does not invoke an LLM or approve work."""
import argparse
import json
from ba_core import BAError, Project, Validator, sha


def resume(project, state_path=None):
    state_path = project.temporary_path(state_path or project.planning / "workflow-state.md")
    # State snapshots are deliberately checked separately: stale artifacts are recoverable blockers.
    validator = Validator(project)
    state = validator.require_valid(state_path, "workflow-state")
    current, invalid = [], []
    for artifact in state.data["artifacts"]:
        path = project.path(artifact["path"])
        check = Validator(project)
        check.validate(path)
        changed = not path.is_file() or sha(path) != artifact["sha256"]
        if changed or not check.ok:
            invalid.append({"path": artifact["path"], "reason": "CONTENT_CHANGED" if changed else "INVALID_DEPENDENCY",
                            "diagnostics": check.diagnostics})
        else:
            current.append(artifact["path"])
    return {"mode": "RESUME", "current": current, "invalidated": invalid,
            "next_action": "Revalidate/revise affected artifacts and refresh human checkpoints" if invalid else "Continue at saved pending checkpoint",
            "saved_pending": state.data["pending"], "approvals_reused": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-config", required=True)
    parser.add_argument("--state")
    args = parser.parse_args()
    try:
        result = resume(Project.load(args.project_config), args.state)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result["invalidated"] else 0
    except (BAError, OSError) as exc:
        print(json.dumps({"diagnostics": [exc.diagnostic if isinstance(exc, BAError) else BAError("IO_ERROR", str(exc)).diagnostic]}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
