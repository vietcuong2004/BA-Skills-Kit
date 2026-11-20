# Dùng kết quả khảo sát để xuất PBI

1. Chạy prepare_handoff.py để kiểm inventory và sinh báo cáo cùng brief.
2. Dùng phạm vi người dùng nêu. Nếu yêu cầu bao quát dự án, chọn các tính năng tìm thấy có bằng chứng và báo phần chưa xác minh.
3. Đưa brief và toàn bộ source_documents do helper cung cấp vào ba-brainstorm với kind: raw. Giữ liên kết EXF/EVD, các mức xác minh và câu hỏi còn mở ở các bước sau.
4. Chạy ba-requirements và ba-product-backlog từ hồ sơ thực tế. Mô tả hành vi hiện có. Đánh dấu rõ phần chỉ có giao diện, dùng dữ liệu mẫu hoặc chưa kiểm chứng.
5. Mặc định tiếp tục qua ba-round-plan, ba-business, ba-spec, ba-review và ba-publish trong cùng lượt. Dùng Round Proposed và PBI nháp cho phần chưa đủ căn cứ.

Nếu chỉ được yêu cầu khảo sát, trả báo cáo và các giới hạn tìm thấy. Khi chạy bên trong một workflow, giao lại hồ sơ khảo sát để workflow đó tiếp tục.
