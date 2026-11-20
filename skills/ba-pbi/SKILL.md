---
name: ba-pbi
description: Thêm một PBI cho tính năng hoặc thay đổi trong dự án hiện hữu. Tự phân tích phần thay đổi, cập nhật hồ sơ liên quan, viết, kiểm tra và xuất cặp business.md/spec.md.
---

# BA-PBI

## Input Contract

Mô tả tính năng cần thêm hoặc thay đổi và dự án đang mở. Round, PBI liên quan, mockup hoặc tài liệu là thông tin tùy chọn. Đọc [quy ước chung](../../conventions/BA-CONVENTIONS.md) và [hướng dẫn cập nhật](references/incremental-guide.md).

## Input Validation

Đọc .temp/ba-project.yaml hoặc tạo từ mẫu theo quy ước chung. Kiểm hồ sơ trong phạm vi thay đổi. Nếu thiếu hồ sơ nền, khảo sát phần liên quan bằng ba-explore-project rồi tạo brainstorm, requirements và backlog tối thiểu từ bằng chứng thật và yêu cầu mới.

## Data Extraction

Lưu yêu cầu trong {planning_dir}/pbi-requests/. Đọc chức năng hiện có, các yêu cầu và PBI liên quan. Tách hành vi đã thấy khỏi hành vi mới cần đề xuất. Chọn lát cắt nhỏ nhất có kết quả sử dụng và kiểm thử được. Ghi phần còn lại vào ngoài phạm vi hoặc đề xuất tiếp theo.

## Processing

1. Dùng [checklist thay đổi](references/change-checklist.md) để phát hiện trùng lặp. Khi đã có PBI mô tả cùng yêu cầu thì dùng lại ID và bộ tài liệu phù hợp. Với thay đổi có giá trị riêng, cấp một ID mới.
2. Chỉ cập nhật brainstorm, requirements và backlog ở phần bị ảnh hưởng. Giữ quan hệ CAP/REQ/Epic/Feature/PBI, nội dung và các ID khác.
3. Giữ các phân bổ đã có. Nếu chưa chỉ định Round, chọn đợt phù hợp với phụ thuộc hoặc lập đợt đề xuất. Dùng ba-round-plan và kiểm tra kế hoạch trước khi viết.
4. Thực hiện ba-business → ba-spec → ba-review. Chuyển giả định và phần thiếu căn cứ thành Proposed/Open Question. Tạo bản đọc thử, xử lý lỗi có thể sửa từ nguồn, rồi gọi ba-publish để xuất. Luồng chạy trong cùng lượt. Nếu người dùng chỉ muốn backlog hoặc bản nháp, kết thúc ở đầu ra được yêu cầu.

Đọc các SKILL.md tương ứng trong thư mục sibling. Nếu runtime không có cơ chế gọi skill, thực hiện chỉ dẫn trong phiên hiện tại.

## Output Contract

Một PBI có business.md/spec.md trong .specify/Round/PBI-ID-slug. Request, hồ sơ làm việc, bản nháp, preview và review nằm trong .temp. Xem [mẫu nhật ký yêu cầu](references/request-record.md).

## Output Validation

Kiểm nguồn và từng file bằng validator --check-refs. Kiểm ID, phạm vi, phụ thuộc và coverage. So với trạng thái ban đầu để phát hiện ảnh hưởng tới PBI khác. Dùng hậu kiểm của ba-publish cho cặp file xuất.

## Error Handling

Nếu yêu cầu rộng, thực hiện một lát cắt và ghi rõ phần còn lại. Nếu có file đích khác nội dung, giữ file đã xuất và trả preview đã kiểm tra. Nếu thiếu dữ kiện nghiệp vụ, giữ câu hỏi trong tài liệu và tiếp tục phần có thể làm.

## Traceability

Giữ các ID đã cấp và nguồn liên quan. Ghi ảnh hưởng khi upstream thay đổi. Rà soát nội dung trước khi cập nhật hash của nguồn bị ảnh hưởng.

## Example Invocation

“Dùng skill ba-pbi tạo và xuất một PBI cho tính năng cho phép người dùng lưu trữ ghi chú cá nhân.”

## Completion Criteria

Trả ID, tiêu đề, đường dẫn hai file và các giả định hoặc câu hỏi còn mở. Nếu đã có PBI tương đương, trả ID và các file tương ứng. Nêu nơi lưu bản đọc thử nếu file đích bị xung đột.
