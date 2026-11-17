---
name: ba-requirements
description: Chuyển brainstorm đã validate thành requirements có CAP–REQ traceability, rules, flows và edge cases. Dùng để phân tích yêu cầu nghiệp vụ; chưa phân rã PBI.
---

# BA-requirements

## Input Contract

Bắt buộc `{planning_dir}/brainstorm.md`, config. Đọc [conventions](../../conventions/BA-CONVENTIONS.md), [input schema](../../contracts/brainstorm.schema.json), [output schema](../../contracts/requirements.schema.json). Resolve KIT_ROOT và đường dẫn theo conventions.

## Input Validation

Cấu hình mới ở `.temp/ba-project.yaml`; `repository_root: .` vẫn là root project. Tìm/đọc bằng `Project.load` theo conventions, tương thích config cũ ở root.

Bố trí file bắt buộc: `planning_dir` phải là `.temp` hoặc thư mục con dưới `.temp` của project. Mọi hồ sơ trung gian/output của bước này (inputs, exploration, backlog, plan, draft, review, request, approvals, state, log/manifest/staging) nằm tại đó. `.specify` chỉ dành cho `Round/PBI-ID-slug/{business.md,spec.md}` do publish tạo. Hai file bàn giao chỉ có nội dung đọc được, không có front matter, BA-DATA, Contract Summary hoặc source hashes; metadata giữ trong `.temp`. Nếu config/đường dẫn cũ dùng `_planning` hoặc `_planing` trong `.specify`, dừng ghi và xử lý migration theo conventions; không tự xóa hồ sơ cũ.

Load config; chạy validator với `--file <brainstorm-path> --expected-type brainstorm --check-refs --project-config <config>`. Chỉ tiếp tục khi đúng project/version và không ERROR/STALE_INPUT. Thiếu input thì nêu ba-brainstorm và đường dẫn cần tạo, không tự chạy nó.

## Data Extraction

Đọc BA-DATA.capabilities, target_users, problems, scope, goals, assumptions, open_questions cùng văn xuôi/evidence. Không suy dữ liệu chỉ từ heading. Liệt kê CAP ID và phạm vi cần được coverage.

## Processing

Phân tích actors/roles, triggers, preconditions, outcomes, data entities/states. Tạo REQ IDs ổn định; mỗi REQ có actor ID, title/description, trigger, preconditions, expected_outcome, capability_refs, source_refs, confirmation_status, business_rule_refs. Một REQ có thể phục vụ nhiều CAP.

As-Is chỉ ghi khi có chứng cứ; To-Be là đề xuất có nhãn. Phân tích BR nguồn, permissions, validation/data/state, main/alternative/exception flows cấp feature và NFR có căn cứ. Dùng [taxonomy](references/edge-case-taxonomy.md) chọn edge case liên quan. EC chưa có outcome phải có open_question và trạng thái Open Question; requirements chưa có AC thì related_ac_refs để rỗng, không trỏ AC tương lai.

Đối chiếu CAP → REQ: không orphan REQ; CAP chưa phân tích phải có giải thích ở Coverage/Open Questions. Không tự chốt quyền, timeout hay giới hạn dữ liệu. Tách Proposed với Confirmed.

## Output Contract

`{planning_dir}/requirements.md`, metadata requirements/ba-requirements, sources có brainstorm path + SHA-256. Dùng [template](references/requirements-template.md), đầy đủ headings theo conventions và Contract Summary khớp dữ liệu.

## Output Validation

Chạy validator `--expected-type requirements --check-refs --format json`. Kiểm tra ID uniqueness, actor/CAP/BR refs, flow kinds/steps, EC outcomes, source freshness. Chỉ sửa lỗi kỹ thuật trong phạm vi, không nâng confirmation để qua test.

## Error Handling

Input invalid → dừng, báo code/file/location và skill upstream. Thiếu thông tin nghiệp vụ → draft với nhãn/câu hỏi; critical decision đưa rõ vào phần Open Questions. Không tự tạo backlog.

## Traceability

Giữ REQ/BR/Flow/EC IDs qua update; ghi added/changed/deprecated trong change_history, không renumber. Source thay đổi làm downstream stale; đọc và xác nhận tác động trước khi refresh.

## Example Invocation

`$ba-requirements project_config=./.temp/ba-project.yaml` — “Phân tích CAP trong brainstorm thành requirements.” Ví dụ cấu trúc: CAP-001 → REQ-001 tạo tài liệu, REQ-002 tìm lại; quan hệ thực tế theo input.

## Completion Criteria

Output PASS, không dangling refs, coverage có giải thích, assumptions rõ. Báo số REQ/rules/EC, nguồn/hash và các quyết định còn chờ. Acceptance: thiếu brainstorm → fail-fast; CAP không tồn tại → BROKEN_REF; không tạo PBI.
