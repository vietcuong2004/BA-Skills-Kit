# Checkpoint policy

Backlog gate: con người xác nhận scope/PBI và quyết định ảnh hưởng lớn trước Round. Round gate: Approved hoặc cho phép Proposed allocation rõ ràng trước khi workflow đi tiếp. Publish gate: cho phép xuất selected PBI trên phiên bản tài liệu hiện tại, các critical decisions đã giải quyết.

DRAFT không mặc nhiên bỏ checkpoint. Có thể tiếp tục draft khi người dùng đã cho phép scope/proposed plan phù hợp; ghi đúng evidence và hashes. Không có quyết định → lưu state chờ, không tạo approval giả.

INTERACTIVE dừng ở gate còn thiếu; RESUME không hỏi lại nếu quyết định trong phiên còn đúng scope/hash. Approval cũ hết hiệu lực khi tài liệu được duyệt đổi bytes; cần trình thay đổi. Ba approval decisions không phải các trạng thái schema PASS, review PASS hoặc document approved.

Ghi audit theo approvals.schema.json vào planning/approvals.json; state giữ bản tóm tắt records nhưng publish đọc lại record hiện tại. Danh tính/evidence phải đối chiếu phiên người dùng, không được coi một JSON bất kỳ là chữ ký tin cậy.
