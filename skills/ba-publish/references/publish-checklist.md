# Checklist publish

- Layout: `.specify` chỉ có Round/PBI/{business.md,spec.md}; planning_dir dưới `.temp`. Audit toàn output trước và sau publish, staging/log/manifest ở `.temp`, không tạo `_planning` trong output.

- Đúng config/root/project và PBI được chọn; Round allocation duy nhất, dependency hợp lệ.
- Nguồn backlog/requirements/brainstorm/business/spec/round/review không stale; review bao phủ đúng draft bytes.
- Review PASS hoặc CONDITIONAL + explicit Draft Publication; không blocker.
- Human backlog và Round checkpoint hợp lệ; publish checkpoint gắn exact document hashes và selected PBI IDs.
- Manifest đã cho người dùng thấy khi cần approval; existing user authorization được tái sử dụng đúng phạm vi, không hỏi lại vô ích.
- Không target ngoài root, không duplicate PBI path; conflict không overwrite.
- Final pair đúng bytes của bản render, post-validate theo drafts/nguồn trong .temp; chính xác hai file, report stdout.
- Hai file bàn giao không có front matter, BA-DATA, Contract Summary hay source hashes; business có các nhóm xử lý và bảng phù hợp, spec có kịch bản Given–When–Then theo từng story và FR/NFR. Metadata chỉ ở .temp, không có sidecar trong PBI.
- Nếu lỗi hậu kiểm, nêu rõ file nào đã được ghi; không tự xóa dữ liệu.
