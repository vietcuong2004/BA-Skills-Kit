# Scenarios kiểm chứng

1. Repository lạ có form tạo tài liệu, handler persistence, search hardcoded và share disabled: lập ba feature đúng mức, không nói search/share hoàn thiện. Không sửa app.
2. Chỉ đọc UI, không thấy API: UI_ONLY và ghi scope/coverage hạn chế; không claim STATIC_IMPLEMENTATION/RUNTIME_VERIFIED.
3. Có test_source nhưng chưa chạy: không được dùng làm runtime_result. Runtime unavailable không chặn khảo sát tĩnh.
4. Hồ sơ BA đã tồn tại: giữ IDs/decisions, báo conflict; không tạo bộ brainstorm mới đè nguồn hiện tại.
5. Chạy helper → brief thật → ba-brainstorm với raw sources → requirements/backlog → business/spec/review bằng contracts cũ. Sửa code sau đó phải thấy STALE_INPUT ở chain cũ.
6. Evidence thiếu file, sai hash, path traversal, duplicate IDs, dangling refs hoặc runtime claim không có log → diagnostic/FAIL rõ ràng; không “sửa” bằng evidence giả.

Automated tests chỉ chứng minh contracts/handoff/freshness và portable installation. Chất lượng khảo sát cần đọc semantic source thực; nếu chưa chạy một fresh-agent eval thì ghi NOT RUN, không suy từ unit tests thành model benchmark.
