---
schema_version: '1.0'
document_type: product-backlog
project_id: example-notes
status: draft
source_documents:
- path: .specify/_planning/brainstorm.md
  sha256: 9cc7e55b05b204677675aa56119f0f2d3aaaf152cf4cfaadd21b9fb33b8540fc
- path: .specify/_planning/requirements.md
  sha256: dc8a87c2b1f7ab245167df29677d5e9227f5886f85af686751aa78e283c73b93
generated_by: ba-product-backlog
---
# product-backlog

<!-- BA-DATA:START -->
```yaml
epics:
- epic_id: EPIC-001
  title: Tri thức theo không gian
  business_value: Tái sử dụng tri thức
features:
- feature_id: FEAT-001
  epic_id: EPIC-001
  title: Vòng đời ghi chú
  requirement_refs:
  - REQ-001
  - REQ-002
pbis:
- pbi_id: PBI-001
  epic_id: EPIC-001
  feature_id: FEAT-001
  title: Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu
  user_story: Là người dùng, tôi muốn tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu để tái sử dụng tri thức.
  business_value: Tạo hoặc tìm lại tri thức trong phạm vi được phép
  scope:
  - Ghi chú được lưu ở không gian đã chọn
  out_of_scope:
  - Cộng tác thời gian thực
  requirement_refs:
  - REQ-001
  dependencies: []
  priority_proposal: Tạo trước, tìm sau để kiểm chứng hành trình
  estimation_status: Unestimated
  confirmation_status: Proposed
  open_questions: []
  invest:
    independent: Nêu dependency rõ
    negotiable: Phạm vi còn thương lượng
    valuable: Có kết quả người dùng nhận được
    estimable: Cần refinement trước ước lượng
    small: Một kết quả đầu cuối
    testable: Có thể quan sát kết quả
- pbi_id: PBI-002
  epic_id: EPIC-001
  feature_id: FEAT-001
  title: Tìm ghi chú được phép xem
  user_story: Là người dùng, tôi muốn tìm ghi chú được phép xem để tái sử dụng tri thức.
  business_value: Tạo hoặc tìm lại tri thức trong phạm vi được phép
  scope:
  - Trả về ghi chú phù hợp trong phạm vi được phép
  out_of_scope:
  - Cộng tác thời gian thực
  requirement_refs:
  - REQ-002
  dependencies:
  - PBI-001
  priority_proposal: Tạo trước, tìm sau để kiểm chứng hành trình
  estimation_status: Unestimated
  confirmation_status: Proposed
  open_questions: []
  invest:
    independent: Nêu dependency rõ
    negotiable: Phạm vi còn thương lượng
    valuable: Có kết quả người dùng nhận được
    estimable: Cần refinement trước ước lượng
    small: Một kết quả đầu cuối
    testable: Có thể quan sát kết quả
unassigned_requirements: []
change_history: []
```
<!-- BA-DATA:END -->

## Product Backlog Overview

Fixture product-backlog: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Epics

Fixture product-backlog: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Features

Fixture product-backlog: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## PBIs

Fixture product-backlog: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## INVEST

Fixture product-backlog: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Requirement Coverage

Fixture product-backlog: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Dependencies

Fixture product-backlog: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Open Questions

Fixture product-backlog: Example Notes. Các nội dung Proposed cần quyết định của người dùng giả lập.

## Contract Summary

| ID | Title | State |
| --- | --- | --- |
| EPIC-001 | Tri thức theo không gian | — |
| FEAT-001 | Vòng đời ghi chú | — |
| PBI-001 | Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu | Proposed |
| PBI-002 | Tìm ghi chú được phép xem | Proposed |
