# Thêm PBI và giữ hồ sơ hiện có

Đọc CAP, REQ, backlog, Round, PBI đã xuất và yêu cầu mới trong phạm vi liên quan. Tái sử dụng ID cho nhu cầu đã có. Cấp ID chưa dùng cho một lát cắt mới có giá trị riêng.

- Dùng lại CAP và REQ khi chúng đã bao phủ nhu cầu. Khi thiếu, cập nhật đúng phần liên quan từ yêu cầu và bằng chứng. Giữ nguyên những quyết định còn hiệu lực.
- Khi PBI mới bao phủ một REQ đang chưa được phân bổ, chuyển REQ đó sang phần coverage. Rà quan hệ với Epic và Feature.
- Giữ Round của các PBI khác. Chọn nơi phù hợp theo phụ thuộc cho PBI mới hoặc tạo Round đề xuất khi chưa có đợt phù hợp.
- Kiểm hồ sơ thay đổi theo thứ tự phụ thuộc. Khi nguồn thay đổi, đọc lại nội dung trước khi cập nhật hash. Báo ảnh hưởng tới các PBI ngoài phạm vi.
- Làm business, spec, preview, review và xuất trong cùng lượt. Ghi điều chưa rõ vào bản nháp. Khi thư mục đích có nội dung khác, giữ file đã xuất và trả đường dẫn preview.

Metadata và nguồn kiểm tra nằm ở .temp. Dùng ba-publish để xuất hai bản đọc được.
