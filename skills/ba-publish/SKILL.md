---
name: ba-publish
description: Kiểm tra và xuất business.md cùng spec.md vào thư mục PBI. Tự kiểm nguồn, Round và xung đột. Có chế độ xem trước khi được yêu cầu.
---

# BA-publish

## Input Contract

Cấu hình, backlog, Round, PBI ID, cặp draft và review của đúng hai draft đó. Đọc [quy ước chung](../../conventions/BA-CONVENTIONS.md) và [checklist xuất](references/publish-checklist.md).

## Input Validation

Dùng Project.load với .temp/ba-project.yaml. Kiểm schema, refs, hash, PBI ID và phân bổ Round bằng scripts/publish_ba.py. Hồ sơ nghiệp vụ còn mở được xuất dưới dạng bản nháp khi dữ liệu kỹ thuật hợp lệ.

## Data Extraction

Lấy PBI ID, tiêu đề, Round và đường dẫn đích từ backlog/plan. Đọc kết quả review và các vấn đề được ghi trong draft.

## Processing

- Khi người dùng yêu cầu PBI hoặc xuất tài liệu, chạy python <KIT_ROOT>/scripts/publish_ba.py --project-config <config> --pbi-id <id> --apply. Helper tự kiểm tra trước khi ghi. Với nhiều PBI, xử lý từng cặp theo thứ tự phụ thuộc và tiếp tục những cặp còn lại khi một cặp xung đột.
- Chỉ bỏ --apply nếu người dùng yêu cầu xem trước. Xem [ví dụ lệnh](references/dry-run-example.md).
- Giữ trạng thái nháp cho nội dung mới. Với review CONDITIONAL/FAIL, ghi các giới hạn trong bản nháp và báo kết quả review thực tế khi trả file.

## Output Contract

Hai file đọc được tại .specify/Round/PBI-ID-slug, theo [mẫu business](../../templates/business-handover.md) và [mẫu spec](../../templates/spec-handover.md). Metadata, nguồn và review ở .temp. Business/spec bàn giao chứa nội dung nghiệp vụ, bảng và kịch bản kiểm thử.

## Output Validation

Helper kiểm lại đầu ra, bảo toàn hai file và hash của cặp nguồn. Cùng nội dung thì bỏ qua file đã có.

## Error Handling

Nguồn thiếu hoặc đổi thì sửa và kiểm lại phần ảnh hưởng. Xung đột đường dẫn hay nội dung giữ nguyên file đã có, lưu bản đọc thử dưới .temp/previews và báo chính xác PBI bị ảnh hưởng. Không tạo PBI ID trùng ở Round khác.

## Traceability

Review khớp hash của hai bản làm việc. Báo cáo xuất gắn PBI, Round và đường dẫn review.

## Example Invocation

“Dùng skill ba-publish để xuất tài liệu PBI-001.”

## Completion Criteria

Trả đường dẫn hai file, trạng thái review và điểm còn mở. Phân biệt file đã ghi, file trùng nội dung và xung đột. Chỉ báo đã xuất khi helper hoàn tất hậu kiểm.
