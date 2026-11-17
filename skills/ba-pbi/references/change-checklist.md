# Checklist phân tích tính năng mới

- Ai muốn thay đổi, vấn đề hiện tại và kết quả mong muốn? Phần nào là evidence, phần nào là giả thuyết?
- Hành vi hiện tại có thực sự chưa có không? Đọc code/docs/call sites liên quan; nếu đã có, phân biệt thay đổi behavior với chỉ bổ sung tài liệu.
- Có PBI đã cover đầy đủ không? Nếu có, chỉ ra overlap và đề nghị refinement. Nếu cần mở rộng, giữ phạm vi mới riêng, không tự sửa PBI cũ.
- Một outcome đầu cuối có thể nghiệm thu riêng chưa? “UI + API + permission” cho cùng outcome có thể vẫn là một PBI; nhiều mục tiêu độc lập có thể cần split.
- Actor, trigger, pre/postconditions, main/alternative/error flows là gì? Khác biệt với hiện trạng nằm ở đâu?
- Dữ liệu/state chuyển thế nào? Ai được làm, xử lý thao tác lặp/concurrency/cancel/stale object thế nào? Chỉ giữ cases liên quan; chưa rõ policy thì câu hỏi.
- Phạm vi loại trừ đủ ngăn creep chưa? Parent Epic/Feature hợp lý theo giá trị, không chỉ menu UI?
- Requirement refs có thật và đầy đủ? Dependencies tồn tại, không cycle, chưa tự cam kết priority/effort?
- Nội dung PBI cũ giữ nguyên không? Những file nào stale do source hash thay đổi, cần thông báo cho user?
- Các unknown quan trọng có trong blockers của draft, không bị biến thành Confirmed hoặc giấu trong câu “xử lý lỗi phù hợp”?
