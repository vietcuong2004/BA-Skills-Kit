# Dependency và Round

1. Tất cả dependency PBI tồn tại; tự phụ thuộc hoặc cycle đều chặn.
2. Mỗi PBI ở một Round hoặc unassigned. Unassigned dependency khiến dependent chưa sẵn sàng phân bổ.
3. Dependency PBI phải cùng/trước Round; cùng Round cần nêu thứ tự và rủi ro nếu chưa hoàn thành.
4. Round dependency phải ở trước trong mảng rounds. Không sắp thứ tự bằng so sánh chuỗi R10/R2.
5. Capacity không có → Proposed + capacity_gaps, không suy effort từ số dòng YAML.
6. Chuyển PBI-001 từ R1 sang R2 giữ ID, ghi history; nếu đã publish, hỏi cách lưu bản cũ, không tự nhân đôi.

Ví dụ PBI-002 tìm kiếm phụ thuộc PBI-001 tạo dữ liệu: có thể cùng R1 với thứ tự thực hiện rõ, hoặc R1/R2 theo capacity. Không bắt buộc phải dùng hai Round.
