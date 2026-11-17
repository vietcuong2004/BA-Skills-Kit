# Hướng dẫn flows

MF-001 mô tả một hành trình thành công từ trigger đến outcome. Mỗi step có actor_action, system_action, input, result. Number bắt đầu 1 và liên tục. Không dùng “hệ thống xử lý” mà bỏ mất kết quả quan sát được.

AF-001 là nhánh hợp lệ, ví dụ đổi cách tạo hoặc hủy. Nêu branch_point trỏ bước của main, trigger, steps, điểm nhập lại hoặc kết thúc. EF-001 là lỗi/ngoại lệ: ngoài error message cần data_state, feedback, recovery; không tự hứa retry tự động hay rollback nếu chưa có quyết định.

Trong spec, flow_refs trỏ local MF/AF/EF cùng PBI. Requirements cũng có flow IDs nhưng không được mượn ngầm vào spec. Không viết endpoint hoặc DB transaction như quyết định nghiệp vụ đã chốt.
