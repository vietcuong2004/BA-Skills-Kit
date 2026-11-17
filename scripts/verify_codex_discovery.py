#!/usr/bin/env python3
"""Install into an isolated temporary project and ask Codex skills/list (no model turn)."""
import argparse
import json
import queue
import shutil
import subprocess
import tempfile
import threading
from pathlib import Path
from install_skills import install
from ba_core import KIT


def verify(executable="codex"):
    executable = shutil.which(executable) or executable
    with tempfile.TemporaryDirectory(prefix="ba-discovery-") as temp:
        project = Path(temp)
        install(project / ".agents" / "skills", apply=True)
        messages = queue.Queue()
        with tempfile.TemporaryFile() as errors:
            process = subprocess.Popen([executable, "app-server", "--stdio"], stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=errors, text=True, encoding="utf-8")
            def receive():
                for line in process.stdout:
                    try:
                        messages.put(json.loads(line))
                    except ValueError:
                        continue
            threading.Thread(target=receive, daemon=True).start()
            def call(identifier, method, params):
                process.stdin.write(json.dumps({"jsonrpc": "2.0", "id": identifier, "method": method, "params": params}) + "\n")
                process.stdin.flush()
                while True:
                    message = messages.get(timeout=30)
                    if message.get("id") == identifier:
                        if "error" in message:
                            raise RuntimeError(message["error"])
                        return message["result"]
            try:
                call(1, "initialize", {"clientInfo": {"name": "ba-kit-discovery-check", "version": "1.0"}, "capabilities": {"experimentalApi": True}})
                process.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "initialized", "params": {}}) + "\n")
                process.stdin.flush()
                response = call(2, "skills/list", {"cwds": [str(project)], "forceReload": True})
                entries = response.get("data", [])
                skills = [s for entry in entries for s in entry.get("skills", []) if s.get("name", "").startswith("ba-")]
                expected = sorted(p.name for p in (KIT / "skills").glob("ba-*"))
                observed = sorted(s["name"] for s in skills if Path(s.get("path", "")).is_relative_to(project))
                diagnostics = [e for entry in entries for e in entry.get("errors", [])]
                return {"result": "PASS" if observed == expected else "FAIL", "method": "Codex app-server skills/list; no model turn",
                        "expected": expected, "discovered": observed, "diagnostics": diagnostics,
                        "runtime_version": subprocess.check_output([executable, "--version"], text=True).strip()}
            finally:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output")
    args = parser.parse_args()
    try:
        result = verify()
    except (OSError, RuntimeError, queue.Empty) as exc:
        result = {"result": "NOT RUN", "reason": str(exc) or "Runtime response timed out"}
    if args.output:
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["result"] == "PASS" else 1)
