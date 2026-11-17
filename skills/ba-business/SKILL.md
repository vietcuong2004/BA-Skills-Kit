---
name: ba-business
description: Viết hoặc cập nhật business.md cho đúng một PBI đã có trong backlog, gồm câu chuyện, giá trị và giải pháp phần mềm có nguồn. Dùng trước đặc tả, chỉ ghi draft theo PBI ID được chọn.
---

# BA-business

## Input Contract

`pbi_id` bắt buộc, config, brainstorm.md, requirements.md, product-backlog.md; round-plan.md tùy chọn. Đọc [conventions](../../conventions/BA-CONVENTIONS.md), [business schema](../../contracts/business.schema.json). Resolve KIT_ROOT và project paths theo conventions.

## Input Validation

Cấu hình mới ở `.temp/ba-project.yaml`; `repository_root: .` vẫn là root project. Tìm/đọc bằng `Project.load` theo conventions, tương thích config cũ ở root.

Bố trí file bắt buộc: `planning_dir` phải là `.temp` hoặc thư mục con dưới `.temp` của project. Mọi hồ sơ trung gian/output của bước này (inputs, exploration, backlog, plan, draft, review, request, approvals, state, log/manifest/staging) nằm tại đó. `.specify` chỉ dành cho `Round/PBI-ID-slug/{business.md,spec.md}` do publish tạo. Nếu config/đường dẫn cũ dùng `_planning` hoặc `_planing` trong `.specify`, dừng ghi và xử lý migration theo conventions; không tự xóa hồ sơ cũ.

Validate mọi nguồn với expected type, project ID, version và `--check-refs`; nếu dùng Round phải validate Round. Chọn đúng một PBI khớp pbi_id; không đoán theo title/thứ tự. Backlog scope/Feature/Epic phải thống nhất. Missing source → báo skill upstream, không tự tạo.

## Data Extraction

Trích PBI cùng title, scope/out_of_scope, requirement_refs, dependencies và confirmation. Resolve Feature/Epic, REQ, CAP/BR liên quan; không trộn nội dung từ PBI khác. Lấy Round allocation nếu có.

## Processing

Viết business context, câu chuyện, vấn đề (evidence hay hypothesis), đối tượng, mục tiêu, giá trị, As-Is có chứng cứ và To-Be. Measurable outcome chỉ nêu số khi có nguồn; chưa rõ để Proposed/Open Question.

Mô tả giải pháp chi tiết theo hành trình: entry point, UI components được xác nhận hoặc Proposed, thao tác người dùng, system feedback, data/state, BR, permission, dependencies, scope, exclusions và risks. Xem [quality checklist](references/quality-checklist.md). Không tự quyết UI, quyền hoặc ngưỡng dữ liệu. Quyết định chưa chốt có ảnh hưởng hành vi bắt buộc vào `blockers`, không chỉ giấu trong risk.

Không sao chép toàn bộ spec. PBI identity/title/scope và requirement_refs phải đúng backlog; nếu cần đổi scope thì báo thay đổi upstream, không âm thầm mở rộng tại business.md.

## Output Contract

`{planning_dir}/drafts/{pbi_id}/business.md`, metadata business/ba-business, pbi_id/epic_id/feature_id/requirement_refs, round_id khi có allocation. `source_documents` hash brainstorm/requirements/backlog và Round nếu đã dùng. [Template](references/business-template.md) có các headings tiếng Việt bắt buộc.

## Output Validation

Validator `--project-config <config> --file <business-path> --expected-type business --pbi-id <pbi_id> --check-refs --format json`. Kiểm PBI/source match, refs, scope, headings/projection và freshness. PASS cấu trúc không duyệt nội dung.

## Error Handling

Wrong PBI/missing ref/stale → dừng, nêu code/file/fix. Thiếu thông tin → draft với assumptions/blockers có nhãn. Không ghi vào output Round, không tự chạy spec/publish.

## Traceability

CAP → REQ → PBI → giải pháp/BR có evidence. Update merge có kiểm soát, giữ ID/Confirmed decisions, ghi history và báo conflict. Thay đổi business làm spec/review stale; không tự sửa chúng nếu chưa được yêu cầu.

## Example Invocation

`$ba-business pbi_id=PBI-001 project_config=./.temp/ba-project.yaml` — “Viết câu chuyện và giải pháp nghiệp vụ cho PBI này.” Ví dụ template là PBI tạo ghi chú, không áp business rules của ví dụ cho project khác.

## Completion Criteria

Một draft đúng PBI, validator PASS, giải pháp cụ thể và chưa chốt được gắn nhãn. Báo path/hash, sources, risks/blockers và bước ba-spec. Acceptance: PBI không tồn tại → fail; PBI khác trong nguồn → fail; không tạo PBI mới.
