> Ví dụ đầy đủ từ fixture giả lập. Không sao chép IDs, hashes, policy hay approval sang project thật. Khi dùng như template, thay dữ liệu bằng nguồn project đích; đọc schema và giữ headings.

---
schema_version: '1.0'
document_type: business
project_id: agent-notes
status: draft
source_documents:
- path: .specify/_planning/brainstorm.md
  sha256: 938a9a472fe6d3e586528e10b8463a1ddff1e125c3f8b2cc84dd11a9724c941c
- path: .specify/_planning/requirements.md
  sha256: 6b105dd6e09ee90b872a66650ed5b2e3df8fe596f2c5e457498b3dad49284556
- path: .specify/_planning/product-backlog.md
  sha256: 9d235920a1ea615bd6420162e3812b9ae1b382bb4576d5cba6ac04c1887d8726
- path: .specify/_planning/round-plan.md
  sha256: 87b68678977c83f909b4f28b847b0d947bef9f9e9f4365f13f5a07cf45eea7e1
- path: scenario.txt
  sha256: b677361b715a3f5d8f19fb47d15ccbf1bbb6bd362414dcd32daa4966f295f0a8
generated_by: ba-business
pbi_id: PBI-001
epic_id: EPIC-001
feature_id: FEAT-001
round_id: R1
requirement_refs:
- REQ-001
---
# business

<!-- BA-DATA:START -->
```yaml
pbi_id: PBI-001
epic_id: EPIC-001
feature_id: FEAT-001
title: Tạo ghi chú cá nhân
requirement_refs:
- REQ-001
round_id: R1
business_story:
  text: Là người dùng, tôi muốn tạo ghi chú cá nhân để lưu và tái sử dụng thông tin.
  confirmation_status: Confirmed
  source_refs:
  - idea.txt
  - scenario.txt
problems:
- text: Thông tin cá nhân cần lưu lại thay vì nằm rải rác trong các đoạn chat.
  confirmation_status: Proposed
  source_refs:
  - idea.txt
  - scenario.txt
target_users:
- Người dùng đã đăng nhập
goals:
- text: Ghi chú được lưu riêng cho chủ sở hữu và có thể đọc lại
  confirmation_status: Confirmed
  source_refs:
  - idea.txt
  - scenario.txt
business_value:
  text: Ghi chú được lưu riêng cho chủ sở hữu và có thể đọc lại
  confirmation_status: Confirmed
  source_refs:
  - idea.txt
  - scenario.txt
as_is: []
to_be:
- text: Chủ sở hữu tạo ghi chú riêng và mở lại để đọc.
  confirmation_status: Confirmed
  source_refs:
  - idea.txt
  - scenario.txt
solution:
- entry_point: Không gian cá nhân, hành động tạo mới (UI Proposed)
  ui_components:
  - Trường tiêu đề
  - Trường nội dung
  - Lưu
  - Hủy
  actions:
  - Mở form
  - Nhập tiêu đề và nội dung
  - Gửi tạo hoặc hủy
  - Đọc lại ghi chú đã lưu
  data_state: Chỉ tạo khi dữ liệu hợp lệ và phiên có quyền; cùng thao tác không tạo bản sao
  feedback: Thành công mở ghi chú; lỗi trả nguyên nhân; chưa rõ kết quả giữ nội dung và kiểm tra thao tác cũ
  permission: Chỉ chủ sở hữu được đọc; kiểm tra phiên/quyền khi gửi, hết quyền thì không lưu.
  business_rule_refs:
  - BR-001
  - BR-002
  - BR-003
  confirmation_status: Proposed
  source_refs:
  - requirements.md#REQ-001
  - scenario.txt
scope:
- Ghi chú được lưu riêng cho chủ sở hữu và có thể đọc lại
out_of_scope:
- Ghi chú trong không gian công ty
- Tạo tài liệu từ mẫu
- Tìm kiếm tài liệu
business_rule_refs:
- BR-001
- BR-002
- BR-003
dependencies: []
risks:
- Chưa có capacity hoặc chính sách giới hạn độ dài; chưa dùng làm cam kết production
open_questions:
- Nhãn hành động và bố cục UI cần refinement
blockers: []
change_history: []
```
<!-- BA-DATA:END -->

## Thông tin PBI

PBI-001 thuộc FEAT-001/EPIC-001, R1 Proposed; phạm vi là tạo và đọc lại ghi chú cá nhân.

## Câu chuyện nghiệp vụ

Người dùng ghi lại thông tin cho bản thân và mở lại sau; không chia sẻ sang không gian công ty trong PBI này.

## Vấn đề

Phân tán thông tin là giả thuyết, chưa có research xác nhận. Không gán KPI tiết kiệm thời gian.

## Đối tượng

Người dùng đã đăng nhập là chủ sở hữu của ghi chú mới.

## Mục tiêu

Lưu rồi đọc lại đúng nội dung trong phạm vi cá nhân.

## Giá trị

Giá trị là bảo toàn thông tin cá nhân để tái sử dụng.

## As-Is/To-Be

As-Is chưa xác minh. To-Be tạo ghi chú riêng rồi đọc lại.

## Giải pháp phần mềm chi tiết

Đề xuất vào không gian cá nhân và chọn tạo mới, nhập tiêu đề/nội dung, Lưu hoặc Hủy. Khi Lưu, kiểm dữ liệu và phiên hiện tại; thành công mở ghi chú. Lỗi không tạo bản ghi; kết quả chưa rõ giữ nội dung và kiểm tra thao tác cũ trước khi gửi lại. Tên nhãn và bố cục là Proposed.

## Scope

Chỉ tạo/đọc lại cá nhân; công ty, mẫu và search nằm ngoài PBI này.

## Rules

BR-001 kiểm quyền sở hữu/phiên; BR-002 yêu cầu dữ liệu có ký tự không trắng; BR-003 không lặp tác dụng khi retry.

## Dependencies

Không có dependency PBI. Phiên đăng nhập là precondition của fixture, không tự tạo feature authentication.

## Risks

Thiếu capacity/giới hạn độ dài cần refinement trước triển khai production; bản này chỉ draft.

## Open Questions

Nhãn UI chưa chốt, không ảnh hưởng outcome đã được scenario xác định.

## Sources

Nguồn: brainstorm, requirements, backlog, Round và scenario fixture. SHA-256 ở metadata.

## Contract Summary

| ID | Title | State |
| --- | --- | --- |
| PBI-001 | Tạo ghi chú cá nhân | — |
