"""Run the suite, validate retained artifacts, and write reproducible integration evidence."""
import io
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
from jsonschema import Draft202012Validator
from ba_core import HEADINGS, Project, Validator, parse, sha
from workflow_state import resume


def main():
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    (ROOT / "tests/test-results.txt").write_text(stream.getvalue(), encoding="utf-8")
    errors = []
    for schema in (ROOT / "contracts").glob("*.schema.json"):
        Draft202012Validator.check_schema(json.loads(schema.read_text(encoding="utf-8")))
    required = ["Input Contract", "Input Validation", "Data Extraction", "Processing", "Output Contract", "Output Validation", "Error Handling", "Traceability", "Example Invocation", "Completion Criteria"]
    for skill in sorted((ROOT / "skills").glob("ba-*/SKILL.md")):
        content = skill.read_text(encoding="utf-8")
        for heading in required:
            if f"## {heading}\n" not in content:
                errors.append(f"Missing {heading}: {skill}")
        for target in re.findall(r"\]\(([^)]+)\)", content):
            if not target.startswith(("https:", "http:")) and not (skill.parent / target).is_file():
                errors.append(f"Broken resource link: {skill}: {target}")
    artifacts = []
    for config in sorted((ROOT / "tests/fixtures").glob("*/ba-project.yaml")):
        project = Project.load(config)
        for path in sorted(project.root.rglob("*.md")):
            validator = Validator(project)
            doc = validator.validate(path)
            row = {"fixture": project.config["project_id"], "file": path.relative_to(ROOT).as_posix(),
                   "sha256": sha(path), "validation": "PASS" if validator.ok else "FAIL", "diagnostics": validator.diagnostics}
            if doc:
                row.update(schema_version=doc.metadata["schema_version"], document_type=doc.metadata["document_type"],
                           generated_by=doc.metadata["generated_by"], inputs=doc.metadata["source_documents"])
            artifacts.append(row)
            if not validator.ok:
                errors.append(f"Invalid fixture: {path}")
        recovery = resume(project)
        if recovery["invalidated"]:
            errors.append(f"Retained fixture state is stale: {config}")
    discovery = json.loads((ROOT / "tests/discovery-evidence.json").read_text(encoding="utf-8"))
    skills = json.loads((ROOT / "tests/skill-validation-evidence.json").read_text(encoding="utf-8"))
    if discovery["result"] != "PASS" or not all(s["valid"] for s in skills):
        errors.append("Runtime discovery or official skill validation did not PASS")
    passed = result.wasSuccessful() and not errors
    evidence = {"result": "PASS" if passed else "FAIL", "tests_run": result.testsRun,
                "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
                "artifact_checks": artifacts, "package_checks": errors, "runtime_discovery": discovery,
                "skill_validation": skills}
    (ROOT / "tests/integration-evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = []
    for kind in ["brainstorm", "requirements", "product-backlog", "round-plan", "business", "spec", "review", "workflow-state"]:
        artifact = next(a for a in artifacts if a["fixture"] == "agent-notes" and a.get("document_type") == kind and "/_planning/" in a["file"])
        relative = artifact["file"].removeprefix("tests/")
        sources = ", ".join(Path(s["path"]).name for s in artifact["inputs"]) or "idea/config hoặc state snapshots"
        rows.append(f"| {artifact['generated_by']} | {sources} | [{Path(relative).name}]({relative}) | {kind} 1.0 | {artifact['validation']} | Thực hiện trong phiên | `{artifact['sha256'][:16]}`… |")
    rows.append("| ba-publish | backlog + Round + pair + review + test approvals | [cặp PBI](fixtures/agent-notes/.specify/R1/PBI-001-tao-ghi-chu-ca-nhan/) | business/spec 1.0 | PASS trước/sau | draft created; rerun skip | [manifest + hashes](fixtures/agent-notes/publish-evidence.json) |")
    report = f"""# Integration report — BA Skills Kit

Ngày kiểm chứng: 2026-11-17 (Asia/Saigon). Kết quả Kit: **{'READY' if passed else 'NOT READY'}** trong phạm vi kiểm thử bên dưới.

## Kết quả thực thi

- **{result.testsRun} tests**, {len(result.failures)} failures, {len(result.errors)} errors, {len(result.skipped)} skipped. [Log đầy đủ](test-results.txt).
- **9/9 SKILL.md** qua `quick_validate.py` của skill-creator runtime. [Evidence](skill-validation-evidence.json).
- **9/9 skills** được Codex CLI 0.161.0 nhận diện bằng app-server `skills/list` trong project tạm có `.agents/skills`; không mở model turn. [Evidence](discovery-evidence.json).
- **{len(artifacts)} tài liệu fixture** gồm draft, state, review và published pair được validate recursive refs/hash; không có ERROR. CAPACITY_UNKNOWN là WARNING có chủ đích.
- JSON Schemas hợp lệ theo Draft 2020-12; các skill có đủ 10 phần contract/workflow và resource links tồn tại.

## Phân biệt các lớp kiểm thử

**Deterministic integration — PASS.** `fixture_pipeline.py` chạy trên Example Notes tối thiểu: 1 CAP, 2 REQ, 1 Epic/Feature, 2 PBI, 1 Round và một pair/review. Mỗi bước đọc file thật đã validate từ bước trước, không thay thế input bằng object tay giữa các bước. Approval là test double. Đây không phải LLM invocation. [Fixture](fixtures/example-notes/).

**Agent execution trong phiên — PASS cho pipeline fixture được chọn.** Agent chính đã áp dụng instructions theo từng bước, đọc output thật và thực hiện qua công cụ; `agent_example.py` lưu phần serialization/replay. Ý tưởng gồm cá nhân, công ty, mẫu, tìm kiếm → 4 CAP/REQ/Feature/PBI. Chỉ PBI-001 có policy đủ rõ để vào R1 Proposed; ba PBI khác unassigned. Không tạo tài liệu sản phẩm thật. Đây là manual in-session execution, không phải sub-agent độc lập hay direct skill invocation API.

Review đầu **FAIL** với hai Major: AC timeout chưa kiểm chứng hiển thị kết quả đã lưu, nhánh đọc trái quyền có input/recovery sai ngữ cảnh. Publish thực sự bị chặn; [evidence review đầu](fixtures/agent-notes/first-review-evidence.json). Sau refinement giữ IDs/rules, review cũ báo STALE_INPUT. Review lại chuyển hai findings thành Resolved, còn Minor UI nên **CONDITIONAL**; chỉ xuất **draft** sau checkpoint mô phỏng. Missing approval trước ghi và idempotent rerun đều được ghi trong [publish evidence](fixtures/agent-notes/publish-evidence.json). RESUME không thay input cho kết quả invalidated rỗng.

**Independent fresh-agent benchmark — NOT RUN.** Không chạy một agent/model độc lập để đo quality hoặc trigger accuracy trên nhiều domain. Bản replay không được coi là một lượt LLM mới. Kit không cam kết rằng schema PASS chứng minh mọi mâu thuẫn văn xuôi đã được phát hiện.

## Matrix handoff của lượt agent trong phiên

| Skill | Input thực | Output thực | Schema | Validator | Test result | Evidence SHA-256 prefix |
| --- | --- | --- | --- | --- | --- | --- |
{chr(10).join(rows)}

Hash đầy đủ, source path/hash, version và diagnostics từng bước nằm trong [integration-evidence.json](integration-evidence.json). Trong metadata source_documents của mỗi output, hash được tính trên raw bytes, không theo mtime.

## Negative tests và invariants

Missing file/field, wrong type/version/project, duplicate IDs/YAML keys/data blocks, broken refs/parents, wrong PBI, thiếu GWT, EC thiếu outcome/question, source cycle, stale trực tiếp/đệ quy, rule bị đổi dưới cùng ID, requirement chưa coverage, duplicate Round allocation, dependency cycle, capacity chưa có nhưng cố Confirmed, review Major không được PASS, missing/stale approval, FAIL review, path traversal/ADS/reserved name, publish conflict, thay nguồn giữa dry-run/apply, raw evidence không thay BA source. Các ca đều có assertion trên diagnostic/behavior, không chỉ kiểm string trong skill.

RESUME sau sửa REQ invalidates backlog/Round/business/spec/review, giữ brainstorm fresh. Rerun publish giữ bytes và mtime. Final PBI directory có đúng business.md/spec.md. Installer dry-run không ghi; install portable, rerun skip, local modification → conflict giữ nguyên bytes. Prefix ITEM/Cycle được kiểm chứng ở project riêng.

Hai lỗi kỹ thuật được tìm thấy khi chạy agent example đã có regression tests: renderer không được sinh YAML alias khi dùng chung object; approval actor trong workflow-state không phải ACT ref nghiệp vụ. CLI xuất tiếng Việt được xử lý UTF-8 trên Windows.

## Phạm vi bàn giao và giới hạn

READY cho Kit source, contracts, helpers, installer và các pipeline fixtures đã kiểm chứng. Chưa cài global/project thật, chưa publish tài liệu thật, không thay app source hoặc Git state. Human approvals trong tests luôn là **TEST HUMAN DOUBLE**, không có giá trị cho project thật.

Publisher hỗ trợ create/skip và chặn conflict; không tự overwrite hoặc di chuyển PBI đã publish. Mỗi PBI pair được stage/rename, không có transaction toàn Round/distributed lock. Không chạy publisher đồng thời cùng PBI. Approval JSON là audit record, không phải chữ ký xác thực; agent phải đối chiếu quyết định người dùng. Structural prose check áp dụng Contract Summary; semantic review vẫn cần BA.

## Chạy lại

```powershell
python -X utf8 -m unittest discover -s tests -v
python -X utf8 tests/run_checks.py
python -X utf8 scripts/verify_codex_discovery.py --output tests/discovery-evidence.json
```

`run_checks.py` dùng discovery/skill-validation evidence của lần kiểm chứng gần nhất. Muốn kiểm chứng runtime mới, chạy discovery lại và official quick_validate theo INSTALL trước; không đổi NOT RUN thành PASS nếu chưa thực thi.
"""
    (ROOT / "tests/INTEGRATION_REPORT.md").write_text(report, encoding="utf-8")
    print(json.dumps({"result": evidence["result"], "tests": result.testsRun, "artifacts": len(artifacts), "package_checks": errors}, ensure_ascii=False))
    if not passed:
        print(stream.getvalue())
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
