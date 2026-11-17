# Chọn edge cases cho spec

Xét input boundaries (min/max chỉ từ nguồn), empty/null/whitespace/Unicode, duplicate/rapid click, cancel, permission changes, concurrency, deleted parent/stale state, timeout sau server success, retry, partial save, integrity. Giải thích nhóm không áp dụng trong phần Edge Cases nếu dễ bị hiểu là bỏ sót.

Mỗi EC ghi scenario + preconditions và kết quả quan sát được: dữ liệu nào tồn tại/thay đổi, ai thấy gì, recovery thế nào. Chưa biết → open_question cùng Open Question; critical unknown → blockers, không hợp thức hóa bằng câu “hiển thị lỗi phù hợp”.

`related_br_refs` phải tồn tại ở nguồn hoặc local rules. `related_ac_refs` thuộc cùng spec; AC link ngược về EC khi kiểm chứng nó. Không dùng AC-001 của PBI khác.
