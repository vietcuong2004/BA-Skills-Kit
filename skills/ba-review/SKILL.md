---
name: ba-review
description: Kiểm tra business/spec của một PBI về phạm vi, hành vi và khả năng kiểm thử. Ghi phát hiện có bằng chứng và kết quả PASS, CONDITIONAL hoặc FAIL.
---

# BA-review

## Input Contract

`pbi_id`, config, draft business.md/spec.md, requirements.md, product-backlog.md; Round nếu liên quan. Đọc [conventions](../../conventions/BA-CONVENTIONS.md), [review schema](../../contracts/review.schema.json); resolve KIT_ROOT/project paths theo conventions.

## Input Validation

Đọc `.temp/ba-project.yaml` bằng `Project.load` theo quy ước chung. Giá trị `repository_root: .` chỉ thư mục dự án chứa `.temp`.

Bố trí file bắt buộc: `planning_dir` phải là `.temp` hoặc thư mục con dưới `.temp` của project. Mọi hồ sơ trung gian/output của bước này (inputs, exploration, backlog, plan, draft, review, request, state, log/manifest/staging) nằm tại đó. `.specify` chỉ dành cho `Round/PBI-ID-slug/{business.md,spec.md}` do publish tạo. Hai file bàn giao chỉ có nội dung đọc được, không có front matter, BA-DATA, Contract Summary hoặc source hashes; metadata giữ trong `.temp`. Nếu config/đường dẫn cũ dùng `_planning` hoặc `_planing` trong `.specify`, dừng ghi và xử lý migration theo conventions; không tự xóa hồ sơ cũ.

Validate từng input với `--check-refs --expected-type <type>` và requested PBI cho business/spec. Cùng project/version/identity; nguồn fresh. Nếu lỗi schema, dừng và xuất diagnostic ra báo cáo trả lời, không làm giả review PASS. File review cuối phải đủ contract, không ghi lỗi parser thành verdict nghiệp vụ.

## Data Extraction

Đọc văn xuôi lẫn BA-DATA, requirements của PBI, business goals/value/scope, proposed decisions/blockers, flows/BR/permissions/data-state, EC, AC và matrix. Ghi exact file + section + trích bằng chứng cần thiết cho finding.

## Processing

So mục tiêu ↔ user story ↔ scope ↔ requirement ↔ flow/rule ↔ EC/AC. Tự tìm thiếu case có liên quan: permission changes, concurrency, stale object, cancel, timeout sau success, retry, partial save, integrity. Không coi danh sách EC có sẵn là đủ.

Kiểm Given/When/Then cụ thể, quan sát được, không mâu thuẫn hoặc duplicate; mỗi flow quan trọng có AC. Kiểm solution đã quá chung chung hay vô tình chốt API/UI/quyền/ngưỡng không có nguồn. Đọc semantic prose; Contract Summary khớp không chứng minh mọi câu đúng.

Chạy scripts/ba_public.py --project-config <config> --file <draft> --write-preview cho business và spec, đọc cả preview trong .temp/previews/PBI-ID. Đối chiếu [mẫu business](../../templates/business-handover.md) và [mẫu spec](../../templates/spec-handover.md). Kiểm tra mục đích, khó khăn, nhu cầu, từng trường/biến thể trong giải pháp và phạm vi ảnh hưởng. Với spec, kiểm từng story có Independent Test và Acceptance Scenarios tương ứng, FR/NFR có mã và căn cứ, Success Criteria kiểm được, Assumptions và Dependencies có tác động rõ. Dùng liên kết AC/FR trong bản nháp để phát hiện hành vi bị mất hoặc ghép sai khi render. Preview không chứa front matter, BA-DATA, Contract Summary hay source hashes. Nội dung quan trọng chỉ có trong văn xuôi nội bộ mà chưa có ở dữ liệu/preview là finding cần sửa trước bàn giao.

Mỗi finding có FIND ID, mức độ, file, mục, bằng chứng, ảnh hưởng, đề xuất và trạng thái. Dùng [rubric](references/severity-rubric.md) để ghi kết quả thật. Trả kết quả cho workflow để sửa dựa trên nguồn và ghi phần còn mở trong bản nháp.

## Output Contract

`{planning_dir}/reviews/{pbi_id}-review.md`; metadata review/ba-review, identity đúng backlog. Sources hash chính xác business/spec đang review và requirements/backlog, Round nếu dùng. [Template](references/review-template.md).

## Output Validation

Validator `--project-config <config> --file <review-path> --expected-type review --pbi-id <pbi_id> --check-refs --format json`. Kiểm kết quả, mức độ, trạng thái và nguồn. CONDITIONAL/FAIL nêu giới hạn của bản nháp để workflow bàn giao cùng tài liệu.

## Error Handling

Input invalid → nêu diagnostic/upstream cần sửa, không chế nội dung thay thế. Sources thay đổi trong review → đọc lại và review lại trước khi lưu hash. FAIL → trả findings, chỉ review lại khi có thay đổi hợp lệ; không retry vô hạn.

## Traceability

Giữ finding ID/history qua vòng review; finding đã giải quyết chuyển Resolved kèm evidence trong history, không âm thầm xóa. Review cũ stale khi business/spec đổi, publish phải chặn.

## Example Invocation

`$ba-review pbi_id=PBI-001 project_config=./.temp/ba-project.yaml` — “Review tài liệu, chỉ báo findings và readiness.”

## Completion Criteria

Review file PASS validator, mọi finding có evidence và recommendation; nguồn được hash, không thay business/spec. Acceptance: wrong PBI/stale → fail; thiếu AC → input fail; blocker nghiệp vụ → FAIL dù schema PASS.
