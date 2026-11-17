---
schema_version: '1.0'
document_type: requirements
project_id: example-notes
status: draft
source_documents:
- path: .specify/_planning/brainstorm.md
  sha256: 9cc7e55b05b204677675aa56119f0f2d3aaaf152cf4cfaadd21b9fb33b8540fc
generated_by: ba-requirements
---
# requirements

<!-- BA-DATA:START -->
```yaml
actors:
- actor_id: ACT-001
  name: Cá nhân
  role: Người soạn/tìm tài liệu
requirements:
- requirement_id: REQ-001
  title: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu
  description: Ghi chú được lưu ở không gian đã chọn
  actor: ACT-001
  trigger: Chọn không gian và cách tạo
  preconditions:
  - Đã đăng nhập
  expected_outcome: Ghi chú được lưu ở không gian đã chọn
  capability_refs:
  - CAP-001
  source_refs:
  - brainstorm.md#CAP-001
  confirmation_status: Proposed
  business_rule_refs:
  - BR-001
- requirement_id: REQ-002
  title: Tìm ghi chú được phép xem
  description: Trả về ghi chú phù hợp trong phạm vi được phép
  actor: ACT-001
  trigger: Nhập từ khóa
  preconditions:
  - Đã đăng nhập
  expected_outcome: Trả về ghi chú phù hợp trong phạm vi được phép
  capability_refs:
  - CAP-001
  source_refs:
  - brainstorm.md#CAP-001
  confirmation_status: Proposed
  business_rule_refs:
  - BR-001
business_rules:
- br_id: BR-001
  title: Giới hạn theo quyền không gian
  rule: Chỉ truy cập tài liệu trong phạm vi được cấp quyền
  requirement_refs:
  - REQ-001
  - REQ-002
  source_refs:
  - brainstorm.md#CAP-001
  confirmation_status: Proposed
data:
- text: Ghi chú có nội dung và không gian sở hữu
  confirmation_status: Proposed
  source_refs:
  - 'idea.txt: yêu cầu người dùng giả lập'
permissions:
- text: Chỉ truy cập tài liệu trong phạm vi được cấp quyền
  confirmation_status: Proposed
  source_refs:
  - 'idea.txt: yêu cầu người dùng giả lập'
as_is: []
flows:
- flow_id: MF-001
  kind: main
  title: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu
  trigger: Chọn không gian và cách tạo
  branch_point: Bắt đầu
  steps:
  - step: 1
    actor_action: Chọn không gian và cách tạo
    system_action: Ghi chú được lưu ở không gian đã chọn
    input: Nội dung hoặc từ khóa người dùng nhập
    result: Ghi chú được lưu ở không gian đã chọn
  termination: Kết thúc với phản hồi rõ ràng
  expected_outcome: Ghi chú được lưu ở không gian đã chọn
  data_state: Chỉ cập nhật khi thao tác thành công
  feedback: Ghi chú được lưu ở không gian đã chọn
  recovery: Giữ nội dung để thử lại khi lỗi
  requirement_refs:
  - REQ-001
  related_br_refs:
  - BR-001
  confirmation_status: Proposed
edge_cases: []
nonfunctional:
- text: Chưa xác định tải và mục tiêu độ trễ; cần đo trước khi chốt
  confirmation_status: Proposed
  source_refs:
  - 'idea.txt: yêu cầu người dùng giả lập'
open_questions:
- Ai quản lý mẫu của công ty?
change_history: []
```
<!-- BA-DATA:END -->

## Actors

Fixture requirements: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Functional Requirements

Fixture requirements: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Business Rules

Fixture requirements: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Data

Fixture requirements: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Permissions

Fixture requirements: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## As-Is / To-Be

Fixture requirements: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Flows

Fixture requirements: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Edge Cases

Fixture requirements: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Nonfunctional Considerations

Fixture requirements: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Coverage

Fixture requirements: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Open Questions

Fixture requirements: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Contract Summary

| ID | Title | State |
| --- | --- | --- |
| ACT-001 | Cá nhân | — |
| REQ-001 | Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu | Proposed |
| REQ-002 | Tìm ghi chú được phép xem | Proposed |
| BR-001 | Giới hạn theo quyền không gian | Proposed |
| MF-001 | Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu | Proposed |
