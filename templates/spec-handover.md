# [PBI ID] — [Tên PBI]

## 1. Thông tin PBI

| Trường | Giá trị |
| --- | --- |
| PBI ID | [ID] |
| Tên | [Tên tính năng] |
| Epic / Feature | [ID liên quan] |
| Requirement | [Các REQ thuộc PBI] |
| Round | [Round đã phân bổ hoặc chưa phân bổ] |
| Actor | [Người sử dụng] |
| Trạng thái | [Bản nháp / Đang review / Đã phê duyệt theo nguồn] |
| Mức độ ưu tiên (đề xuất) | [Theo backlog] |

## 2. Mục tiêu

[Mục tiêu và giá trị lấy từ business của PBI.]

## 3. Phạm vi

### 3.1. In Scope

[Các hành vi nằm trong PBI.]

### 3.2. Out of Scope

[Các hành vi không nằm trong PBI.]

## 4. User Story

Là [người dùng], tôi muốn [hành động] để [giá trị].

## 5. Actor, Trigger và điều kiện

[Actor, trigger, preconditions và postconditions khi thành công/thất bại.]

## 6. Main Flow — Luồng chính

### [MF ID] — [Tên luồng]

| Bước | Người dùng | Hệ thống | Dữ liệu vào | Kết quả |
| --- | --- | --- | --- | --- |
| 1 | [Thao tác] | [Xử lý] | [Dữ liệu] | [Kết quả] |

[Kết thúc, trạng thái dữ liệu, phản hồi, phục hồi và các rule/REQ liên quan.]

## 7. Alternative Flows — Luồng thay thế

[Từng AF: điểm rẽ, điều kiện, các bước, kết quả, trạng thái xác nhận.]

## 8. Exception Flows — Luồng ngoại lệ

[Từng EF: điểm rẽ, lỗi, phản hồi, dữ liệu còn lại và cách phục hồi.]

## 9. Business Rules

| ID | Quy tắc | Yêu cầu | Trạng thái |
| --- | --- | --- | --- |
| [BR ID] | [Nội dung đầy đủ] | [REQ] | [Đã xác nhận / Đề xuất / Cần làm rõ] |

## 10. Validation, dữ liệu và trạng thái

[Quy tắc nhập liệu, quyền thực hiện, dữ liệu và chuyển trạng thái có căn cứ.]

## 11. Edge Cases — Tình huống đặc biệt

[Từng EC, điều kiện, hành vi mong đợi/câu hỏi, AC/rule liên quan và trạng thái.]

## 12. Acceptance Criteria — Given / When / Then

### [AC ID] — [Tên điều kiện nghiệm thu]

- **Given:** [Điều kiện ban đầu]
- **When:** [Thao tác hoặc sự kiện]
- **Then:** [Kết quả quan sát được]

[Trạng thái xác nhận và liên kết REQ/flow/EC.]

## 13. Dependencies

[Phụ thuộc đã được ghi nhận cho PBI.]

## 14. Non-functional Considerations

[Yêu cầu phi chức năng từ nguồn; không tự đặt ngưỡng.]

## 15. Open Questions

[Câu hỏi chưa có quyết định và ảnh hưởng của chúng.]

## 16. Traceability Matrix

| Requirement | Business Rule | Flow | Edge Case | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| [REQ] | [BR] | [MF/AF/EF] | [EC] | [AC] |

## 17. Change Log

[Thời điểm, thay đổi, ID ảnh hưởng và lý do theo lịch sử có thật.]

## 18. Readiness Checklist

[Checklist dựa trên dữ liệu và trạng thái thực tế; nêu các quyết định còn chờ. Không suy phê duyệt từ việc có đủ mục.]
