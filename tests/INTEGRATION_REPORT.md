# Integration report — BA Skills Kit

Ngày kiểm chứng: 2026-11-17 (Asia/Saigon). Kết quả Kit: **READY** trong phạm vi kiểm thử bên dưới.

## Kết quả thực thi

- **42 tests**, 0 failures, 0 errors, 0 skipped. [Log đầy đủ](test-results.txt).
- **9/9 SKILL.md** qua `quick_validate.py` của skill-creator runtime. [Evidence](skill-validation-evidence.json).
- **9/9 skills** được Codex CLI 0.161.0 nhận diện bằng app-server `skills/list` trong project tạm có `.agents/skills`; không mở model turn. [Evidence](discovery-evidence.json).
- **20 tài liệu fixture** gồm draft, state, review và published pair được validate recursive refs/hash; không có ERROR. CAPACITY_UNKNOWN là WARNING có chủ đích.
- JSON Schemas hợp lệ theo Draft 2020-12; các skill có đủ 10 phần contract/workflow và resource links tồn tại.

## Phân biệt các lớp kiểm thử

**Deterministic integration — PASS.** `fixture_pipeline.py` chạy trên Example Notes tối thiểu: 1 CAP, 2 REQ, 1 Epic/Feature, 2 PBI, 1 Round và một pair/review. Mỗi bước đọc file thật đã validate từ bước trước, không thay thế input bằng object tay giữa các bước. Approval là test double. Đây không phải LLM invocation. [Fixture](fixtures/example-notes/).

**Agent execution trong phiên — PASS cho pipeline fixture được chọn.** Agent chính đã áp dụng instructions theo từng bước, đọc output thật và thực hiện qua công cụ; `agent_example.py` lưu phần serialization/replay. Ý tưởng gồm cá nhân, công ty, mẫu, tìm kiếm → 4 CAP/REQ/Feature/PBI. Chỉ PBI-001 có policy đủ rõ để vào R1 Proposed; ba PBI khác unassigned. Không tạo tài liệu sản phẩm thật. Đây là manual in-session execution, không phải sub-agent độc lập hay direct skill invocation API.

Review đầu **FAIL** với hai Major: AC timeout chưa kiểm chứng hiển thị kết quả đã lưu, nhánh đọc trái quyền có input/recovery sai ngữ cảnh. Publish thực sự bị chặn; [evidence review đầu](fixtures/agent-notes/first-review-evidence.json). Sau refinement giữ IDs/rules, review cũ báo STALE_INPUT. Review lại chuyển hai findings thành Resolved, còn Minor UI nên **CONDITIONAL**; chỉ xuất **draft** sau checkpoint mô phỏng. Missing approval trước ghi và idempotent rerun đều được ghi trong [publish evidence](fixtures/agent-notes/publish-evidence.json). RESUME không thay input cho kết quả invalidated rỗng.

**Independent fresh-agent benchmark — NOT RUN.** Không chạy một agent/model độc lập để đo quality hoặc trigger accuracy trên nhiều domain. Bản replay không được coi là một lượt LLM mới. Kit không cam kết rằng schema PASS chứng minh mọi mâu thuẫn văn xuôi đã được phát hiện.

## Matrix handoff của lượt agent trong phiên

| Skill | Input thực | Output thực | Schema | Validator | Test result | Evidence SHA-256 prefix |
| --- | --- | --- | --- | --- | --- | --- |
| ba-brainstorm | idea.txt, scenario.txt | [brainstorm.md](fixtures/agent-notes/.specify/_planning/brainstorm.md) | brainstorm 1.0 | PASS | Thực hiện trong phiên | `938a9a472fe6d3e5`… |
| ba-requirements | brainstorm.md, scenario.txt | [requirements.md](fixtures/agent-notes/.specify/_planning/requirements.md) | requirements 1.0 | PASS | Thực hiện trong phiên | `6b105dd6e09ee90b`… |
| ba-product-backlog | brainstorm.md, requirements.md | [product-backlog.md](fixtures/agent-notes/.specify/_planning/product-backlog.md) | product-backlog 1.0 | PASS | Thực hiện trong phiên | `9d235920a1ea615b`… |
| ba-round-plan | product-backlog.md, requirements.md | [round-plan.md](fixtures/agent-notes/.specify/_planning/round-plan.md) | round-plan 1.0 | PASS | Thực hiện trong phiên | `87b68678977c83f9`… |
| ba-business | brainstorm.md, requirements.md, product-backlog.md, round-plan.md, scenario.txt | [business.md](fixtures/agent-notes/.specify/_planning/drafts/PBI-001/business.md) | business 1.0 | PASS | Thực hiện trong phiên | `b145a0531ccf204e`… |
| ba-spec | business.md, requirements.md, product-backlog.md | [spec.md](fixtures/agent-notes/.specify/_planning/drafts/PBI-001/spec.md) | spec 1.0 | PASS | Thực hiện trong phiên | `8259f2ab88d4657f`… |
| ba-review | business.md, spec.md, requirements.md, product-backlog.md | [PBI-001-review.md](fixtures/agent-notes/.specify/_planning/reviews/PBI-001-review.md) | review 1.0 | PASS | Thực hiện trong phiên | `9fb255ad6f973d46`… |
| ba-workflow | idea/config hoặc state snapshots | [workflow-state.md](fixtures/agent-notes/.specify/_planning/workflow-state.md) | workflow-state 1.0 | PASS | Thực hiện trong phiên | `865cdefe8e29e467`… |
| ba-publish | backlog + Round + pair + review + test approvals | [cặp PBI](fixtures/agent-notes/.specify/R1/PBI-001-tao-ghi-chu-ca-nhan/) | business/spec 1.0 | PASS trước/sau | draft created; rerun skip | [manifest + hashes](fixtures/agent-notes/publish-evidence.json) |

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
