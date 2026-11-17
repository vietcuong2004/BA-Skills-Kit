# Taxonomy lựa chọn edge case

| Nhóm | Câu hỏi phân tích | Chỉ giữ khi |
| --- | --- | --- |
| Input | Empty/null/whitespace; Unicode; giới hạn từ nguồn nào? | Có nhập hoặc import dữ liệu |
| Trùng lặp | Hai thao tác giống nhau có tạo hai kết quả? | Có create/submit/retry |
| Quyền | Quyền thay đổi giữa đọc và ghi? | Có nhiều actor/không gian |
| Concurrency | Hai người sửa cùng tài liệu, stale parent? | Có shared mutable data |
| Timeout | Server thành công nhưng client chưa biết? | Có kết nối hoặc tác vụ bất đồng bộ |
| Cancel | Dữ liệu nháp có được giữ, rollback đến đâu? | Có thao tác nhiều bước |
| Partial success | Phần nào hoàn thành, retry có lặp tác dụng? | Batch hoặc side effects nhiều phần |
| Integrity | Parent bị xóa, tham chiếu còn dùng được? | Có quan hệ entity |

Không tự sinh mọi case cho mọi project. Nếu outcome chưa có quyết định, dùng `open_question` và Open Question; đừng lấy “hiển thị lỗi” làm expected behavior cho mọi trường hợp. Nêu rõ dữ liệu cuối cùng, feedback và recovery cần được quyết định.
