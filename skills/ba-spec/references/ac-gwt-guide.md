# Given–When–Then

Given mô tả trạng thái trước, When là sự kiện/thao tác, Then là kết quả kiểm chứng được và data state. Tránh “hoạt động bình thường”, “nhanh”, “thân thiện”. Không cần viết test script click từng pixel.

Ví dụ Proposed: Given người dùng mở form trong không gian từng có quyền tạo; When quyền đã bị thu hồi trước lúc gửi; Then không tạo tài liệu và không hiển thị nội dung ngoài quyền. Đưa chính sách thông báo/giữ nháp còn mở vào EC question thay vì tự đoán.

Mỗi AC có requirement_refs và flow_refs. Bao phủ main success, nhánh quan trọng, lỗi và EC rủi ro cao. AC giữ ID qua refinement; thay wording không cấp ID mới nếu vẫn cùng ý nghiệm thu. Quyết định thay đổi nghĩa phải có history và review.
