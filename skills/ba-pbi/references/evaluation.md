# Tình huống cần kiểm chứng

| Yêu cầu / bối cảnh | Kết quả mong muốn |
| --- | --- |
| Một tính năng nhỏ, REQ đã tồn tại nhưng chưa có PBI | Thêm một PBI, dùng lại nguồn; giữ PBI cũ; điều chỉnh unassigned coverage nếu cần |
| Tính năng ngoài CAP/REQ hiện tại | Điều phối cập nhật upstream tối thiểu; giữ IDs/decisions, không tái tạo toàn project |
| Đã có PBI cùng behavior | Báo overlap, không tự append duplicate |
| User đưa nhiều outcome độc lập nhưng yêu cầu “một PBI” | Trình phương án thu nhỏ/tách và hỏi chọn; không âm thầm làm nhiều PBI |
| Có code nhưng không baseline BA | Nêu missing inputs và đề nghị explore/bootstrap theo scope; không tạo PBI với refs giả |
| Scope được duyệt, không Round | Business/spec draft được phép omit round_id; không tạo Round giả, chưa publish |
| Backlog/requirements đổi hash | PBI khác có thể stale; không sửa nội dung/approval của chúng để che tác động |
| Resume request đã thêm PBI | Tiếp tục đúng ID, không tạo bản sao |
| Publish được yêu cầu nhưng review FAIL/thiếu approval | Giữ gate ba-publish, không copy trực tiếp cặp file |

Kiểm front matter, local links, portable installation và contracts handoff bằng công cụ Kit. Test fixture tự động không phải independent model evaluation. Nếu chưa có agent độc lập chạy các scenario này thì ghi NOT RUN cho đánh giá đó.
