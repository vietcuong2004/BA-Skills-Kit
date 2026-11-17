---
schema_version: '1.0'
document_type: requirements
project_id: agent-notes
status: draft
source_documents:
- path: .specify/_planning/brainstorm.md
  sha256: 938a9a472fe6d3e586528e10b8463a1ddff1e125c3f8b2cc84dd11a9724c941c
- path: scenario.txt
  sha256: b677361b715a3f5d8f19fb47d15ccbf1bbb6bd362414dcd32daa4966f295f0a8
generated_by: ba-requirements
---
# requirements

<!-- BA-DATA:START -->
```yaml
actors:
- actor_id: ACT-001
  name: Người dùng đã đăng nhập
  role: Chủ sở hữu ghi chú cá nhân hoặc thành viên công ty
requirements:
- requirement_id: REQ-001
  title: Tạo ghi chú cá nhân
  description: Tạo ghi chú cá nhân
  actor: ACT-001
  trigger: Chọn tạo ghi chú cá nhân
  preconditions:
  - Người dùng đã đăng nhập
  expected_outcome: Ghi chú được lưu riêng cho chủ sở hữu và có thể đọc lại
  capability_refs:
  - CAP-001
  source_refs:
  - brainstorm.md#CAP-001
  - scenario.txt
  confirmation_status: Confirmed
  business_rule_refs:
  - BR-001
  - BR-002
  - BR-003
- requirement_id: REQ-002
  title: Ghi chú trong không gian công ty
  description: Ghi chú trong không gian công ty
  actor: ACT-001
  trigger: Chọn không gian công ty
  preconditions:
  - Người dùng đã đăng nhập
  expected_outcome: Ghi chú thuộc đúng không gian được phép
  capability_refs:
  - CAP-002
  source_refs:
  - brainstorm.md#CAP-002
  - scenario.txt
  confirmation_status: Proposed
  business_rule_refs: []
- requirement_id: REQ-003
  title: Tạo tài liệu từ mẫu
  description: Tạo tài liệu từ mẫu
  actor: ACT-001
  trigger: Chọn mẫu
  preconditions:
  - Người dùng đã đăng nhập
  expected_outcome: Tài liệu khởi tạo từ mẫu được phép
  capability_refs:
  - CAP-003
  source_refs:
  - brainstorm.md#CAP-003
  - scenario.txt
  confirmation_status: Proposed
  business_rule_refs: []
- requirement_id: REQ-004
  title: Tìm kiếm tài liệu
  description: Tìm kiếm tài liệu
  actor: ACT-001
  trigger: Nhập từ khóa
  preconditions:
  - Người dùng đã đăng nhập
  expected_outcome: Hiển thị tài liệu phù hợp trong phạm vi được phép
  capability_refs:
  - CAP-004
  source_refs:
  - brainstorm.md#CAP-004
  - scenario.txt
  confirmation_status: Proposed
  business_rule_refs: []
business_rules:
- br_id: BR-001
  title: Sở hữu cá nhân
  rule: Chỉ chủ sở hữu được đọc; kiểm tra phiên/quyền khi gửi, hết quyền thì không lưu.
  requirement_refs:
  - REQ-001
  source_refs:
  - scenario.txt
  confirmation_status: Confirmed
- br_id: BR-002
  title: Thông tin bắt buộc
  rule: Tiêu đề và nội dung đều có ít nhất một ký tự không phải khoảng trắng; chưa chốt giới hạn độ dài.
  requirement_refs:
  - REQ-001
  source_refs:
  - scenario.txt
  confirmation_status: Confirmed
- br_id: BR-003
  title: Không lặp tác dụng
  rule: Gửi lại cùng thao tác không tạo bản sao; kết quả chưa rõ thì giữ nội dung và kiểm tra thao tác cũ trước
    khi gửi lại.
  requirement_refs:
  - REQ-001
  source_refs:
  - scenario.txt
  confirmation_status: Confirmed
data:
- text: Ghi chú cá nhân có tiêu đề, nội dung và chủ sở hữu.
  confirmation_status: Confirmed
  source_refs:
  - idea.txt
  - scenario.txt
permissions:
- text: Chỉ chủ sở hữu được đọc; kiểm tra phiên/quyền khi gửi, hết quyền thì không lưu.
  confirmation_status: Confirmed
  source_refs:
  - idea.txt
  - scenario.txt
as_is: []
flows:
- flow_id: MF-001
  kind: main
  title: Tạo và đọc lại ghi chú
  trigger: Gửi nội dung hợp lệ
  branch_point: Bắt đầu
  steps:
  - step: 1
    actor_action: Gửi nội dung hợp lệ
    system_action: Một ghi chú được lưu cho chủ sở hữu và đọc lại được
    input: Tiêu đề và nội dung đang soạn
    result: Một ghi chú được lưu cho chủ sở hữu và đọc lại được
  termination: Kết thúc tại phản hồi được mô tả
  expected_outcome: Một ghi chú được lưu cho chủ sở hữu và đọc lại được
  data_state: Một ghi chú được lưu cho chủ sở hữu và đọc lại được
  feedback: Một ghi chú được lưu cho chủ sở hữu và đọc lại được
  recovery: Giữ nội dung nếu kết quả chưa rõ; kiểm tra thao tác cũ trước khi gửi lại
  requirement_refs:
  - REQ-001
  related_br_refs:
  - BR-001
  - BR-002
  - BR-003
  confirmation_status: Confirmed
- flow_id: AF-001
  kind: alternative
  title: Hủy tạo
  trigger: Hủy trước khi gửi
  branch_point: MF-001 tại bước gửi
  steps:
  - step: 1
    actor_action: Hủy trước khi gửi
    system_action: Không tạo ghi chú
    input: Tiêu đề và nội dung đang soạn
    result: Không tạo ghi chú
  termination: Kết thúc tại phản hồi được mô tả
  expected_outcome: Không tạo ghi chú
  data_state: Không tạo ghi chú
  feedback: Không tạo ghi chú
  recovery: Giữ nội dung nếu kết quả chưa rõ; kiểm tra thao tác cũ trước khi gửi lại
  requirement_refs:
  - REQ-001
  related_br_refs: []
  confirmation_status: Confirmed
- flow_id: EF-001
  kind: exception
  title: Phiên hết hiệu lực
  trigger: Gửi sau khi phiên hết hiệu lực
  branch_point: MF-001 tại bước gửi
  steps:
  - step: 1
    actor_action: Gửi sau khi phiên hết hiệu lực
    system_action: Không lưu và không lộ nội dung
    input: Tiêu đề và nội dung đang soạn
    result: Không lưu và không lộ nội dung
  termination: Kết thúc tại phản hồi được mô tả
  expected_outcome: Không lưu và không lộ nội dung
  data_state: Không lưu và không lộ nội dung
  feedback: Không lưu và không lộ nội dung
  recovery: Giữ nội dung nếu kết quả chưa rõ; kiểm tra thao tác cũ trước khi gửi lại
  requirement_refs:
  - REQ-001
  related_br_refs:
  - BR-001
  confirmation_status: Confirmed
edge_cases:
- ec_id: EC-001
  title: Gửi lại khi chưa rõ kết quả
  scenario: Mất phản hồi sau khi server đã nhận thao tác
  preconditions:
  - Đã gửi thao tác tạo
  expected_behavior: Gửi lại cùng thao tác không tạo bản sao; kết quả chưa rõ thì giữ nội dung và kiểm tra thao
    tác cũ trước khi gửi lại.
  requirement_refs:
  - REQ-001
  related_br_refs:
  - BR-003
  related_ac_refs: []
  confirmation_status: Confirmed
nonfunctional:
- text: Cần đo nhu cầu tải và thời gian phản hồi trước khi chốt chỉ tiêu.
  confirmation_status: Proposed
  source_refs:
  - idea.txt
  - scenario.txt
open_questions:
- Ai cấp quyền công ty?
- Ai quản lý mẫu?
- Tìm kiếm hỗ trợ phạm vi nào?
change_history: []
```
<!-- BA-DATA:END -->

## Actors

Actor là người dùng đã đăng nhập; vai trò công ty chưa xác định chi tiết.

## Functional Requirements

Bốn REQ tương ứng bốn CAP. Tạo ghi chú cá nhân có hành vi fixture xác nhận; ba nhu cầu còn lại Proposed.

## Business Rules

Ba rule cá nhân từ scenario: quyền sở hữu, nội dung bắt buộc và không lặp tác dụng khi gửi lại.

## Data

Ghi chú có tiêu đề/nội dung/chủ sở hữu. Không quyết định bảng DB hay API.

## Permissions

Chỉ chủ sở hữu đọc ghi chú cá nhân; kiểm tra lại phiên khi ghi. Quyền công ty còn mở.

## As-Is / To-Be

Chưa có evidence hệ thống As-Is. To-Be cho phép lưu rồi đọc lại ghi chú của mình.

## Flows

Main flow tạo/đọc lại, alternative hủy và exception phiên hết hiệu lực. Các feature còn lại cần refinement trước triển khai.

## Edge Cases

Inventory có timeout/retry không lặp tác dụng; spec cần thêm whitespace, phiên hết hiệu lực và rapid click. Không tự chọn ngưỡng độ dài.

## Nonfunctional Considerations

Chưa có capacity/SLA được cung cấp, để Proposed.

## Coverage

Mỗi CAP có một REQ; các requirement công ty/mẫu/tìm kiếm được giữ, không bỏ vì chưa chốt policy.

## Open Questions

Ai cấp quyền công ty, quản lý mẫu và xác định phạm vi search? Những câu này chặn PBI tương ứng, không chặn lát cắt cá nhân đã xác định.

## Contract Summary

| ID | Title | State |
| --- | --- | --- |
| ACT-001 | Người dùng đã đăng nhập | — |
| REQ-001 | Tạo ghi chú cá nhân | Confirmed |
| REQ-002 | Ghi chú trong không gian công ty | Proposed |
| REQ-003 | Tạo tài liệu từ mẫu | Proposed |
| REQ-004 | Tìm kiếm tài liệu | Proposed |
| BR-001 | Sở hữu cá nhân | Confirmed |
| BR-002 | Thông tin bắt buộc | Confirmed |
| BR-003 | Không lặp tác dụng | Confirmed |
| MF-001 | Tạo và đọc lại ghi chú | Confirmed |
| AF-001 | Hủy tạo | Confirmed |
| EF-001 | Phiên hết hiệu lực | Confirmed |
| EC-001 | Gửi lại khi chưa rõ kết quả | Confirmed |
