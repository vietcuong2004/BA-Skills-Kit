---
schema_version: '1.0'
document_type: spec
project_id: example-notes
status: draft
source_documents:
- path: .specify/_planning/drafts/PBI-001/business.md
  sha256: eca2c7fa554c750247306edc9902e7cfeb0fe0e744a3d2f8640b48ca4288af15
- path: .specify/_planning/requirements.md
  sha256: dc8a87c2b1f7ab245167df29677d5e9227f5886f85af686751aa78e283c73b93
- path: .specify/_planning/product-backlog.md
  sha256: 1d39e6d7a3d0f4f939b3b33a265e9d0342aad908d6c45cda609551f9fa01b5da
generated_by: ba-spec
pbi_id: PBI-001
epic_id: EPIC-001
feature_id: FEAT-001
round_id: R1
requirement_refs:
- REQ-001
---
# spec

<!-- BA-DATA:START -->
```yaml
pbi_id: PBI-001
epic_id: EPIC-001
feature_id: FEAT-001
title: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu
requirement_refs:
- REQ-001
round_id: R1
user_stories:
- as_a: Cá nhân
  i_want: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu
  so_that: Tạo hoặc tìm lại tri thức trong phạm vi được phép
preconditions:
- Đã đăng nhập
postconditions:
- Ghi chú được lưu ở không gian đã chọn
flows:
- flow_id: MF-001
  kind: main
  title: Hoàn thành thao tác
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
- flow_id: AF-001
  kind: alternative
  title: Hủy thao tác
  trigger: Người dùng chọn hủy
  branch_point: MF-001 bước 1
  steps:
  - step: 1
    actor_action: Người dùng chọn hủy
    system_action: Không thay đổi dữ liệu
    input: Nội dung hoặc từ khóa người dùng nhập
    result: Không thay đổi dữ liệu
  termination: Kết thúc với phản hồi rõ ràng
  expected_outcome: Không thay đổi dữ liệu
  data_state: Chỉ cập nhật khi thao tác thành công
  feedback: Không thay đổi dữ liệu
  recovery: Giữ nội dung để thử lại khi lỗi
  requirement_refs:
  - REQ-001
  related_br_refs:
  - BR-001
  confirmation_status: Proposed
- flow_id: EF-001
  kind: exception
  title: Quyền thay đổi
  trigger: Quyền không còn hợp lệ lúc thực hiện
  branch_point: MF-001 bước 1
  steps:
  - step: 1
    actor_action: Quyền không còn hợp lệ lúc thực hiện
    system_action: Từ chối và không lộ nội dung không được phép
    input: Nội dung hoặc từ khóa người dùng nhập
    result: Từ chối và không lộ nội dung không được phép
  termination: Kết thúc với phản hồi rõ ràng
  expected_outcome: Từ chối và không lộ nội dung không được phép
  data_state: Chỉ cập nhật khi thao tác thành công
  feedback: Từ chối và không lộ nội dung không được phép
  recovery: Giữ nội dung để thử lại khi lỗi
  requirement_refs:
  - REQ-001
  related_br_refs:
  - BR-001
  confirmation_status: Proposed
business_rules:
- br_id: BR-001
  title: Giới hạn theo quyền không gian
  rule: Chỉ truy cập tài liệu trong phạm vi được cấp quyền
  requirement_refs:
  - REQ-001
  source_refs:
  - brainstorm.md#CAP-001
  confirmation_status: Proposed
permissions:
- text: Chỉ truy cập tài liệu trong phạm vi được cấp quyền
  confirmation_status: Proposed
  source_refs:
  - 'idea.txt: yêu cầu người dùng giả lập'
data_states:
- text: Không thay đổi dữ liệu khi hủy hoặc bị từ chối
  confirmation_status: Proposed
  source_refs:
  - 'idea.txt: yêu cầu người dùng giả lập'
edge_cases:
- ec_id: EC-001
  title: Quyền bị thu hồi
  scenario: Quyền thay đổi sau khi mở màn hình
  preconditions:
  - Đã mở màn hình với quyền hợp lệ
  expected_behavior: Từ chối và không lộ nội dung không được phép
  requirement_refs:
  - REQ-001
  related_br_refs:
  - BR-001
  related_ac_refs:
  - AC-003
  confirmation_status: Proposed
acceptance_criteria:
- ac_id: AC-001
  title: Hoàn thành thao tác
  given: Đã chọn không gian và đăng nhập
  when: Chọn không gian và cách tạo
  then: Ghi chú được lưu ở không gian đã chọn
  requirement_refs:
  - REQ-001
  flow_refs:
  - MF-001
  edge_case_refs: []
  confirmation_status: Proposed
- ac_id: AC-002
  title: Hủy thao tác
  given: Đã chọn không gian và đăng nhập
  when: Người dùng chọn hủy
  then: Không thay đổi dữ liệu
  requirement_refs:
  - REQ-001
  flow_refs:
  - AF-001
  edge_case_refs: []
  confirmation_status: Proposed
- ac_id: AC-003
  title: Quyền thay đổi
  given: Đã chọn không gian và đăng nhập
  when: Quyền không còn hợp lệ lúc thực hiện
  then: Từ chối và không lộ nội dung không được phép
  requirement_refs:
  - REQ-001
  flow_refs:
  - EF-001
  edge_case_refs:
  - EC-001
  confirmation_status: Proposed
traceability:
- requirement_id: REQ-001
  br_refs:
  - BR-001
  flow_refs:
  - MF-001
  - AF-001
  - EF-001
  ec_refs:
  - EC-001
  ac_refs:
  - AC-001
  - AC-002
  - AC-003
scope:
- Ghi chú được lưu ở không gian đã chọn
out_of_scope:
- Cộng tác thời gian thực
open_questions: []
blockers: []
change_history: []
```
<!-- BA-DATA:END -->

## PBI Information

Fixture spec: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu. Các nội dung Proposed cần quyết định của người dùng giả lập.

## User Stories

Fixture spec: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Preconditions

Fixture spec: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Postconditions

Fixture spec: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Main Flow

Fixture spec: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Alternative Flows

Fixture spec: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Exception Flows

Fixture spec: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Business Rules

Fixture spec: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Permissions

Fixture spec: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Data and States

Fixture spec: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Edge Cases

Fixture spec: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Acceptance Criteria

Fixture spec: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Traceability

Fixture spec: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Scope

Fixture spec: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Open Questions

Fixture spec: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Contract Summary

| ID | Title | State |
| --- | --- | --- |
| PBI-001 | Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu | — |
| BR-001 | Giới hạn theo quyền không gian | Proposed |
| MF-001 | Hoàn thành thao tác | Proposed |
| AF-001 | Hủy thao tác | Proposed |
| EF-001 | Quyền thay đổi | Proposed |
| EC-001 | Quyền bị thu hồi | Proposed |
| AC-001 | Hoàn thành thao tác | Proposed |
| AC-002 | Hủy thao tác | Proposed |
| AC-003 | Quyền thay đổi | Proposed |
