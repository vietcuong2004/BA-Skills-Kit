---
name: ba-review
description: Review độc lập business/spec của một PBI về scope, hành vi, traceability và readiness; xuất findings có bằng chứng và PASS/CONDITIONAL/FAIL. Không tự sửa tài liệu hay phê duyệt thay con người.
---

# BA-review

## Input Contract

`pbi_id`, config, draft business.md/spec.md, requirements.md, product-backlog.md; Round nếu liên quan. Đọc [conventions](../../conventions/BA-CONVENTIONS.md), [review schema](../../contracts/review.schema.json); resolve KIT_ROOT/project paths theo conventions.

## Input Validation

Cấu hình mới ở `.temp/ba-project.yaml`; `repository_root: .` vẫn là root project. Tìm/đọc bằng `Project.load` theo conventions, tương thích config cũ ở root.

Bố trí file bắt buộc: `planning_dir` phải là `.temp` hoặc thư mục con dưới `.temp` của project. Mọi hồ sơ trung gian/output của bước này (inputs, exploration, backlog, plan, draft, review, request, approvals, state, log/manifest/staging) nằm tại đó. `.specify` chỉ dành cho `Round/PBI-ID-slug/{business.md,spec.md}` do publish tạo. Nếu config/đường dẫn cũ dùng `_planning` hoặc `_planing` trong `.specify`, dừng ghi và xử lý migration theo conventions; không tự xóa hồ sơ cũ.

Validate từng input với `--check-refs --expected-type <type>` và requested PBI cho business/spec. Cùng project/version/identity; nguồn fresh. Nếu lỗi schema, dừng và xuất diagnostic ra báo cáo trả lời, không làm giả review PASS. File review cuối phải đủ contract, không ghi lỗi parser thành verdict nghiệp vụ.

## Data Extraction

Đọc văn xuôi lẫn BA-DATA, requirements của PBI, business goals/value/scope, proposed decisions/blockers, flows/BR/permissions/data-state, EC, AC và matrix. Ghi exact file + section + trích bằng chứng cần thiết cho finding.

## Processing

So mục tiêu ↔ user story ↔ scope ↔ requirement ↔ flow/rule ↔ EC/AC. Tự tìm thiếu case có liên quan: permission changes, concurrency, stale object, cancel, timeout sau success, retry, partial save, integrity. Không coi danh sách EC có sẵn là đủ.

Kiểm Given/When/Then cụ thể, quan sát được, không mâu thuẫn hoặc duplicate; mỗi flow quan trọng có AC. Kiểm solution đã quá chung chung hay vô tình chốt API/UI/quyền/ngưỡng không có nguồn. Đọc semantic prose; Contract Summary khớp không chứng minh mọi câu đúng.

Mỗi finding có FIND ID, severity, file, section, evidence, impact, recommendation, status. Theo [severity rubric](references/severity-rubric.md): Critical/Major mở hoặc business blocker → FAIL/Blocked; Minor refinement mở → CONDITIONAL/Needs Refinement; không finding mở/blocker → PASS/Ready. Không tự sửa business/spec trong lúc review; không tự ghi approval.

## Output Contract

`{planning_dir}/reviews/{pbi_id}-review.md`; metadata review/ba-review, identity đúng backlog. Sources hash chính xác business/spec đang review và requirements/backlog, Round nếu dùng. [Template](references/review-template.md).

## Output Validation

Validator `--project-config <config> --file <review-path> --expected-type review --pbi-id <pbi_id> --check-refs --format json`. So kết quả với severity/readiness/blockers, refs/identity và freshness. PASS review không tương đương human approval.

## Error Handling

Input invalid → nêu diagnostic/upstream cần sửa, không chế nội dung thay thế. Sources thay đổi trong review → đọc lại và review lại trước khi lưu hash. FAIL → trả findings, chỉ review lại khi có thay đổi hợp lệ; không retry vô hạn.

## Traceability

Giữ finding ID/history qua vòng review; finding đã giải quyết chuyển Resolved kèm evidence trong history, không âm thầm xóa. Review cũ stale khi business/spec đổi, publish phải chặn.

## Example Invocation

`$ba-review pbi_id=PBI-001 project_config=./.temp/ba-project.yaml` — “Review tài liệu, chỉ báo findings và readiness.”

## Completion Criteria

Review file PASS validator, mọi finding có evidence và recommendation; nguồn được hash, không thay business/spec. Acceptance: wrong PBI/stale → fail; thiếu AC → input fail; blocker nghiệp vụ → FAIL dù schema PASS.
