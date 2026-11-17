# Ví dụ vertical slicing

Ý tưởng “ghi chú cá nhân, công ty, mẫu, tìm kiếm” có thể chia theo hành trình:

- Tạo và đọc lại ghi chú cá nhân từ trắng.
- Tạo ghi chú trong không gian công ty với quyền đã được xác định.
- Khởi tạo ghi chú từ một mẫu được phép dùng.
- Tìm lại ghi chú trong phạm vi được xem.

Mỗi lát cắt gồm tương tác, xử lý và dữ liệu cần cho kết quả người dùng; “xây frontend”, “tạo bảng DB” chỉ là task triển khai nếu sau này được yêu cầu. Đây là phương án Proposed, không mặc định là backlog đã duyệt.

Fixture contract tối thiểu gộp create modes vào REQ-001/PBI-001 và search vào REQ-002/PBI-002 để test 1 CAP → 2 REQ → 1 Epic/Feature → 2 PBI. Khi dùng thật cần kiểm lại độ lớn, không coi kích thước fixture là lời khuyên phân rã.
