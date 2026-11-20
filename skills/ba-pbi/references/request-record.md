# Request record raw

File ở `{planning_dir}/pbi-requests/{request-id}.md`, ID ngắn ổn định theo phiên, tránh trùng và giữ đường dẫn trong project root. Record là context/audit của tác vụ, không thuộc canonical BA schema.

Ghi các mục sau, chỉ thông tin thực tế:

1. **Request:** nguyên văn yêu cầu người dùng và phạm vi output (backlog-only / full draft / publish được yêu cầu riêng).
2. **Baseline:** project/config, path + SHA-256 nguồn đã đọc, CAP/REQ/PBI liên quan, trạng thái xác minh hiện trạng.
3. **Delta:** As-Is → To-Be, value/actor, scope/exclusions, rule/permission/data/state, câu hỏi và giả định Proposed.
4. **Proposed PBI:** ID/title/parents/refs/dependencies dự kiến, duplicate/split analysis. Đánh dấu “proposed ID” trước khi thực sự ghi vào backlog.
5. **Quyết định và giả định.** Ghi nguồn của điều đã rõ và câu hỏi cho điều chưa biết.
6. **Changes and impact:** files/objects đã đổi, ID giữ nguyên, downstream stale và conflict cần xử lý.
7. **Kết quả.** Ghi các file đã tạo, kết quả kiểm tra, đường dẫn PBI và lỗi hoặc việc còn lại.

Nếu record được dùng làm raw source của canonical output: chốt record snapshot trước khi lấy hash, ghi tiến độ mới vào record/sidecar khác. Không tạo chu trình “backlog hash request, request liên tục hash backlog mới” rồi cập nhật lẫn nhau. Snapshot cũ cần được giữ để audit, không giả đó là trạng thái mới nhất.

Resume đọc record cùng output thực, không tin completed flag nếu file thiếu/hash lệch. Cùng request đã có PBI thì tiếp tục ID đó; không append một PBI nữa mỗi lần gọi skill.
