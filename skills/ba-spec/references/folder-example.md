# Ví dụ hành vi PBI tạo thư mục — Proposed

Đây là ví dụ sư phạm, không phải fixture đủ schema hay policy cho mọi dự án.

User story: Là người sắp xếp tài liệu, tôi muốn tạo thư mục trong không gian được phép để nhóm tài liệu theo công việc. Scope: tạo một thư mục rỗng dưới parent đã chọn; ngoài scope: di chuyển cây hoặc chia sẻ.

- Preconditions: đã chọn parent hiện hữu; quyền tạo phải được xác định từ requirements.
- MF-001: mở form → nhập tên → gửi → kiểm tra quyền/parent/rule tên từ nguồn → tạo → hiển thị thư mục mới. Postcondition: một thư mục thuộc đúng parent.
- AF-001: hủy tại form; Proposed outcome: không tạo thư mục. Việc giữ draft tên là câu hỏi nếu chưa chốt.
- EF-001: parent không còn tồn tại khi gửi; Proposed outcome: không tạo dangling child, thông báo trạng thái parent và cho chọn lại.
- BR-001: chỉ tạo dưới parent tồn tại và được phép, Proposed cho tới khi có nguồn xác nhận.
- EC-001: parent bị xóa đồng thời → expected_behavior như EF-001.
- EC-002: tên trùng → Open Question: cho trùng, cảnh báo hay từ chối? Không tự chọn chính sách.
- AC-001: Given parent tồn tại và actor có quyền; When gửi tên hợp lệ theo rule đã duyệt; Then tạo đúng một thư mục dưới parent, hiển thị thành công.
- AC-002: Given form đã mở; When hủy; Then không tạo thư mục.
- AC-003: Given parent bị xóa trước khi gửi; When gửi tạo; Then không tạo child và phản hồi parent không còn tồn tại.

Trace: requirement tạo thư mục → BR-001, MF/AF/EF, EC-001 → AC-001..003. EC-002 ảnh hưởng hành vi create, phải làm rõ hoặc ghi blocker trước publish. Không tự đặt giới hạn 255 ký tự hay constraint DB.
