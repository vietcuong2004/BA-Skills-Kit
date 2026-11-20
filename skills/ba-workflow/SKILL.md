---
name: ba-workflow
description: Chạy từ ý tưởng hoặc dự án hiện có đến các cặp business.md và spec.md trong .specify. Tự khảo sát, lập backlog và Round, kiểm tra rồi xuất PBI trong cùng lượt. Dùng để viết bộ tài liệu BA hoặc tiếp tục việc còn dở.
---

# BA-workflow

## Input Contract

Yêu cầu của người dùng và thư mục dự án đang mở. Với dự án có sẵn, dùng code/tài liệu và hồ sơ BA hiện có. Với dự án mới, dùng ý tưởng người dùng đưa. Đọc [quy ước chung](../../conventions/BA-CONVENTIONS.md), [luồng xử lý](references/workflow-map.md) và [schema state](../../contracts/workflow-state.schema.json).

## Input Validation

Đọc cấu hình tại .temp/ba-project.yaml. Nếu thiếu, tạo từ mẫu dùng tên thư mục và các giá trị mặc định theo quy ước chung. Kiểm tra hồ sơ thật trước khi tái sử dụng. Chỉ hỏi khi không xác định được dự án hoặc không có ý tưởng, mã nguồn hay tài liệu để suy ra tính năng có nghĩa.

## Data Extraction

Dùng phạm vi từ câu nhắn, tên tính năng, module hoặc PBI ID. Khi yêu cầu viết tài liệu cho cả dự án, chọn các tính năng có bằng chứng và báo các vùng chưa khảo sát. Khi tiếp tục, đọc state và đối chiếu file thật bằng workflow_state.py để biết phần còn thiếu hoặc đã đổi.

## Processing

Mặc định mode AUTO chạy đến cặp PBI trong .specify trong cùng lượt. Thực hiện các skill tại các thư mục sibling. Nếu runtime không có cơ chế gọi skill, đọc và làm theo chỉ dẫn ngay trong phiên.

1. Dự án hiện có mà thiếu hồ sơ hiện trạng: thực hiện phần khảo sát của ba-explore-project. Kiểm dữ liệu khảo sát và dùng brief, báo cáo, nguồn code/docs làm đầu vào theo handoff guide. Ý tưởng dự án mới đi thẳng vào ba-brainstorm.
2. Thực hiện ba-brainstorm → ba-requirements → ba-product-backlog, validate sau mỗi bước. Tạo các hồ sơ thiếu và giữ các ID, nội dung còn hiệu lực. Ghi giả định ở trạng thái Proposed và phần thiếu căn cứ vào Open Questions. Tự tiếp tục từ backlog hợp lệ.
3. Dùng ba-round-plan phân bổ PBI trong phạm vi. Tái sử dụng phân bổ còn hợp lệ. Khi chưa có kế hoạch, lập đợt đề xuất theo prefix của dự án và thứ tự phụ thuộc. Thiếu ước lượng vẫn dùng Proposed để nhóm tài liệu.
4. Với từng PBI, chạy ba-business → ba-spec → ba-review. Validate nguồn, tạo hai bản đọc thử và đối chiếu ở bước review. Sửa các lỗi có thể giải quyết từ bằng chứng rồi review lại. Ghi nhận các câu hỏi nghiệp vụ và vấn đề còn mở vào bản nháp và review.
5. Dùng ba-publish xuất cặp business.md/spec.md vào Round tương ứng. Tự thực hiện kiểm tra và ghi file. PBI có vấn đề nghiệp vụ còn mở được bàn giao dạng nháp với các vấn đề nêu rõ. Xử lý tiếp các PBI khác nếu một cặp gặp lỗi kỹ thuật hoặc xung đột đích.

DRAFT hoặc yêu cầu chỉ viết nháp kết thúc ở bản làm việc và preview. Yêu cầu một bước giữ đúng phạm vi bước đó. SINGLE-PBI và SINGLE-ROUND dùng mã tương ứng. RESUME khôi phục phần đang làm theo [hướng dẫn tiếp tục](references/recovery-guide.md) và đi tiếp đến kết quả trong phạm vi. INTERACTIVE trong state cũ được tiếp tục theo luồng AUTO.

## Output Contract

- Mỗi PBI đã xuất có đúng business.md và spec.md trong .specify/Round/PBI-ID-slug.
- Hồ sơ khảo sát, backlog, kế hoạch, draft, preview và review nằm dưới .temp.
- Ghi {planning_dir}/workflow-state.md gồm mode, current_phase, completed, pending, blockers, artifacts (đường dẫn và hash), last_updated có múi giờ, selected_pbis, selected_round nếu có và change_history. Metadata.source_documents của state để rỗng.

## Output Validation

Kiểm schema, refs và hash của hồ sơ. Kiểm từng cặp file xuất theo ba-publish. Báo riêng PBI đã xuất, PBI gắn nhãn bản nháp và PBI gặp lỗi kỹ thuật.

## Error Handling

Tạo upstream còn thiếu trong phạm vi. Nguồn đổi thì đọc và kiểm lại phần ảnh hưởng. Khi gặp xung đột file, giữ cặp đã có, để bản mới ở preview và báo đường dẫn. Khi thiếu một dữ kiện mà vẫn có thể viết tài liệu có ích, ghi câu hỏi ngay trong tài liệu và tiếp tục.

## Traceability

Giữ ID và evidence refs qua các bước. State lưu file đã thực sự tạo và phần cần tiếp tục.

## Example Invocation

“Dùng skill ba-workflow để khảo sát dự án đang mở và xuất tài liệu PBI cho các tính năng hiện có.”

“Dùng skill ba-workflow để viết và xuất PBI cho ứng dụng đặt lịch học theo mô tả sau: [ý tưởng].”

## Completion Criteria

Trả danh sách PBI cùng đường dẫn business.md/spec.md và các điểm cần làm rõ. Kết thúc ở backlog hoặc preview khi người dùng yêu cầu đầu ra đó. Chỉ báo đã xuất khi helper đã ghi và kiểm tra cặp file.
