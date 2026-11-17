# Recovery / RESUME

Kiểm layout trước: state, artifacts và hồ sơ trung gian thuộc `.temp`. Config cũ chứa planning_dir bên trong `.specify` phải được chuyển theo conventions; không chạy tiếp để tạo `_planning` mới hoặc chỉ đổi config mà bỏ broken refs/hashes.

File bàn giao trong Round/PBI không có metadata. Validator dùng drafts tương ứng trong .temp để kiểm nguồn và so bản render; không tự thêm front matter vào file cuối để chữa MISSING_INPUT. Nếu thiếu drafts thì khôi phục hồ sơ làm việc trước; bản cũ còn metadata phải chuyển định dạng theo conventions, giữ dữ liệu và xử lý conflict.

1. Validate config và state schema. State `artifacts` chứa snapshot path/hash, không dùng metadata.sources để state vẫn mở được khi output thay đổi.
2. Chạy workflow_state.py để đọc từng artifact thật, so hash và validate recursive source chain. MISSING_INPUT/STALE_INPUT/CONTENT_CHANGED tạo invalidated, không tự xóa.
3. Tìm bước sớm nhất ảnh hưởng selected PBI/Round. Đọc lại nguồn, giữ IDs/Confirmed decisions, giải quyết conflict; chỉ thực hiện bước trong scope user yêu cầu.
4. Cập nhật output theo quyết định đã có, validate; review lại khi pair đổi; approval gắn hash cũ phải trình lại checkpoint.
5. Cập nhật state snapshot sau khi hoàn thành thực tế, ghi history và pending/blockers chính xác.

Không sửa hash downstream đơn thuần để bỏ STALE_INPUT. Không reset toàn pipeline hoặc renumber IDs. Nếu không có runtime invocation API, đọc skill và thực hiện trong phiên, ghi `manual in-session execution`; nếu chưa thực hiện phải ghi NOT RUN.
