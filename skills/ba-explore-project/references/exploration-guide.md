# Khảo sát sản phẩm hiện có

## Evidence và mức xác minh

| verification | Dùng khi | Không được suy ra |
| --- | --- | --- |
| UNKNOWN | Chỉ có tên/mô tả hoặc bằng chứng chưa đủ | Đã có chức năng |
| UI_ONLY | Tìm thấy giao diện nhưng chưa lần được xử lý thực | Backend hoạt động |
| MOCK | Có fixture/hardcoded response/stub thay xử lý thật | Có persistence/API thật |
| PARTIAL | Có một phần đường xử lý nhưng đứt/mâu thuẫn/incomplete | End-to-end hoàn thiện |
| STATIC_IMPLEMENTATION | Lần được đường UI/API/domain/data liên quan qua source; với backend-only xác định entrypoint thực | Đã chạy thành công |
| RUNTIME_VERIFIED | Đã chạy hành trình cụ thể, có evidence kết quả và môi trường | Production luôn đúng, mọi nhánh đều tested |

availability là chiều độc lập: enabled, disabled, unknown. Feature flag tắt không xóa sự tồn tại của implementation. Backend policy và UI gate mâu thuẫn: ghi conflict, không tự chọn “đúng” theo UI.

EVD kind gồm ui, implementation, test_source, documentation, runtime_result. Test source có assertion chưa phải test PASS. Runtime result có file log/artifact an toàn nằm trong root, môi trường, hành động và kết quả quan sát được; không tự bịa log. Chỉ hash file không có secret hoặc dữ liệu cá nhân.

## Quy trình đọc repository

Đầu tiên liệt kê file bằng rg --files (hoặc tương đương), xem README/manifest/entrypoints an toàn để chọn vùng liên quan. Tránh node_modules/vendor/generated/dist/.git, secrets và datasets. Không đọc tràn toàn repo. Ghi cả những vùng bỏ qua và lý do; scope hẹp phải hiện rõ ở báo cáo.

Sau đó lập routes/actions inventory, đọc imports/call sites/registration thay vì chỉ regex tên hàm. Chọn từng hành trình rồi truy nguồn hai chiều: UI gọi gì, API được gọi bởi đâu, quyền nằm ở client hay server, thao tác nào ảnh hưởng dữ liệu, response/error nào thể hiện ra người dùng. Không tạo “feature” cho mọi helper kỹ thuật.

Nhóm tính năng theo outcome người dùng, giữ cả backend-only job/API có giá trị nghiệp vụ. Authentication, background jobs, export/import, search filters, permission boundaries và feature flags dễ bị bỏ sót nếu chỉ xem menu. Chủ động tìm nhưng chỉ ghi feature có evidence, không tự áp checklist thành yêu cầu phải có.

Không khởi động dự án bằng lệnh phỏng đoán. Đọc scripts/run instructions trước; dùng runtime nếu có sẵn và việc chạy nằm trong scope được phép. Thiếu dependency/runtime/data → ghi limitation, tiếp tục static survey. Không gọi môi trường live hoặc thực hiện thay đổi dữ liệu ngoài authorization.

## Content claims

Một behavior/rule/data/permission là object text + evidence_refs + confirmation_status. Confirmed ở đây xác nhận **đã quan sát trong source/hành vi**, không phải stakeholder đã duyệt policy. Inference là Proposed hoặc Open Question. Nếu thiếu rule outcome thì viết câu hỏi, không “suy diễn cho đủ spec”.

Technical design hiện tại có thể dẫn evidence nhưng không biến thành business requirement tương lai bắt buộc. Phân biệt lỗi có sẵn với hành vi được mong muốn; ghi discrepancy để người dùng quyết định giữ/document hay đề nghị thay đổi ở công việc riêng.
