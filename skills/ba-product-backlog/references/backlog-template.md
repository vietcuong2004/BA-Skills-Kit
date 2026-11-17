> Ví dụ đầy đủ từ fixture giả lập. Không sao chép IDs, hashes, policy hay approval sang project thật. Khi dùng như template, thay dữ liệu bằng nguồn project đích; đọc schema và giữ headings. Đây là mẫu hồ sơ làm việc nội bộ, chỉ lưu dưới .temp.

---
schema_version: '1.0'
document_type: product-backlog
project_id: agent-notes
status: draft
source_documents:
- path: .temp/brainstorm.md
  sha256: 938a9a472fe6d3e586528e10b8463a1ddff1e125c3f8b2cc84dd11a9724c941c
- path: .temp/requirements.md
  sha256: c947f2712fcce64155b0661af3c3069fc99df6fc05512d965506b40082fb6237
generated_by: ba-product-backlog
---
# product-backlog

<!-- BA-DATA:START -->
```yaml
epics:
- epic_id: EPIC-001
  title: Lưu và tái sử dụng tri thức
  business_value: Lưu và tái sử dụng thông tin theo ngữ cảnh
features:
- feature_id: FEAT-001
  epic_id: EPIC-001
  title: Tạo ghi chú cá nhân
  requirement_refs:
  - REQ-001
- feature_id: FEAT-002
  epic_id: EPIC-001
  title: Ghi chú trong không gian công ty
  requirement_refs:
  - REQ-002
- feature_id: FEAT-003
  epic_id: EPIC-001
  title: Tạo tài liệu từ mẫu
  requirement_refs:
  - REQ-003
- feature_id: FEAT-004
  epic_id: EPIC-001
  title: Tìm kiếm tài liệu
  requirement_refs:
  - REQ-004
pbis:
- pbi_id: PBI-001
  epic_id: EPIC-001
  feature_id: FEAT-001
  title: Tạo ghi chú cá nhân
  user_story: Là người dùng, tôi muốn tạo ghi chú cá nhân để lưu và tái sử dụng thông tin.
  business_value: Ghi chú được lưu riêng cho chủ sở hữu và có thể đọc lại
  scope:
  - Ghi chú được lưu riêng cho chủ sở hữu và có thể đọc lại
  out_of_scope:
  - Ghi chú trong không gian công ty
  - Tạo tài liệu từ mẫu
  - Tìm kiếm tài liệu
  requirement_refs:
  - REQ-001
  dependencies: []
  priority_proposal: Lát cắt cá nhân trước; mở rộng sau khi chốt policy
  estimation_status: Unestimated
  confirmation_status: Proposed
  open_questions: []
  invest:
    independent: Lát cắt cá nhân chạy độc lập; các mở rộng phụ thuộc tạo tài liệu.
    negotiable: UI chưa chốt; outcome đã mô tả.
    valuable: Ghi chú được lưu riêng cho chủ sở hữu và có thể đọc lại
    estimable: Cần team refinement, chưa gán story point.
    small: Một kết quả người dùng, tách theo không gian/cách tạo/tìm lại.
    testable: Quan sát tài liệu/kết quả và phạm vi được phép.
- pbi_id: PBI-002
  epic_id: EPIC-001
  feature_id: FEAT-002
  title: Ghi chú trong không gian công ty
  user_story: Là người dùng, tôi muốn ghi chú trong không gian công ty để lưu và tái sử dụng thông tin.
  business_value: Ghi chú thuộc đúng không gian được phép
  scope:
  - Ghi chú thuộc đúng không gian được phép
  out_of_scope:
  - Tạo ghi chú cá nhân
  - Tạo tài liệu từ mẫu
  - Tìm kiếm tài liệu
  requirement_refs:
  - REQ-002
  dependencies:
  - PBI-001
  priority_proposal: Lát cắt cá nhân trước; mở rộng sau khi chốt policy
  estimation_status: Unestimated
  confirmation_status: Proposed
  open_questions:
  - Cần refinement chính sách trước triển khai
  invest:
    independent: Lát cắt cá nhân chạy độc lập; các mở rộng phụ thuộc tạo tài liệu.
    negotiable: UI chưa chốt; outcome đã mô tả.
    valuable: Ghi chú thuộc đúng không gian được phép
    estimable: Cần team refinement, chưa gán story point.
    small: Một kết quả người dùng, tách theo không gian/cách tạo/tìm lại.
    testable: Quan sát tài liệu/kết quả và phạm vi được phép.
- pbi_id: PBI-003
  epic_id: EPIC-001
  feature_id: FEAT-003
  title: Tạo tài liệu từ mẫu
  user_story: Là người dùng, tôi muốn tạo tài liệu từ mẫu để lưu và tái sử dụng thông tin.
  business_value: Tài liệu khởi tạo từ mẫu được phép
  scope:
  - Tài liệu khởi tạo từ mẫu được phép
  out_of_scope:
  - Tạo ghi chú cá nhân
  - Ghi chú trong không gian công ty
  - Tìm kiếm tài liệu
  requirement_refs:
  - REQ-003
  dependencies:
  - PBI-001
  priority_proposal: Lát cắt cá nhân trước; mở rộng sau khi chốt policy
  estimation_status: Unestimated
  confirmation_status: Proposed
  open_questions:
  - Cần refinement chính sách trước triển khai
  invest:
    independent: Lát cắt cá nhân chạy độc lập; các mở rộng phụ thuộc tạo tài liệu.
    negotiable: UI chưa chốt; outcome đã mô tả.
    valuable: Tài liệu khởi tạo từ mẫu được phép
    estimable: Cần team refinement, chưa gán story point.
    small: Một kết quả người dùng, tách theo không gian/cách tạo/tìm lại.
    testable: Quan sát tài liệu/kết quả và phạm vi được phép.
- pbi_id: PBI-004
  epic_id: EPIC-001
  feature_id: FEAT-004
  title: Tìm kiếm tài liệu
  user_story: Là người dùng, tôi muốn tìm kiếm tài liệu để lưu và tái sử dụng thông tin.
  business_value: Hiển thị tài liệu phù hợp trong phạm vi được phép
  scope:
  - Hiển thị tài liệu phù hợp trong phạm vi được phép
  out_of_scope:
  - Tạo ghi chú cá nhân
  - Ghi chú trong không gian công ty
  - Tạo tài liệu từ mẫu
  requirement_refs:
  - REQ-004
  dependencies:
  - PBI-001
  priority_proposal: Lát cắt cá nhân trước; mở rộng sau khi chốt policy
  estimation_status: Unestimated
  confirmation_status: Proposed
  open_questions:
  - Cần refinement chính sách trước triển khai
  invest:
    independent: Lát cắt cá nhân chạy độc lập; các mở rộng phụ thuộc tạo tài liệu.
    negotiable: UI chưa chốt; outcome đã mô tả.
    valuable: Hiển thị tài liệu phù hợp trong phạm vi được phép
    estimable: Cần team refinement, chưa gán story point.
    small: Một kết quả người dùng, tách theo không gian/cách tạo/tìm lại.
    testable: Quan sát tài liệu/kết quả và phạm vi được phép.
unassigned_requirements: []
change_history: []
```
<!-- BA-DATA:END -->

## Product Backlog Overview

Một Epic, bốn Feature/PBI theo kết quả người dùng. Scope/ưu tiên chưa phải cam kết triển khai.

## Epics

Epic lưu và tái sử dụng tri thức bao gồm cả cá nhân và tổ chức.

## Features

Tách bốn Feature theo nhu cầu; không chia frontend/backend.

## PBIs

PBI-001 tạo/đọc lại cá nhân là lát cắt nhỏ đầu tiên; các PBI còn lại cần refinement policy.

## INVEST

Mỗi PBI có phân tích INVEST; chưa estimate, không gán story points.

## Requirement Coverage

Bốn REQ được bao phủ; không unassigned requirement. Một REQ vẫn có thể được nhiều PBI nếu sau này split.

## Dependencies

Các mở rộng dựa trên khả năng tạo tài liệu; không có vòng lặp.

## Open Questions

Công ty/mẫu/search cần chốt policy trước triển khai. Backlog sẽ qua checkpoint test riêng.

## Contract Summary

| ID | Title | State |
| --- | --- | --- |
| EPIC-001 | Lưu và tái sử dụng tri thức | — |
| FEAT-001 | Tạo ghi chú cá nhân | — |
| FEAT-002 | Ghi chú trong không gian công ty | — |
| FEAT-003 | Tạo tài liệu từ mẫu | — |
| FEAT-004 | Tìm kiếm tài liệu | — |
| PBI-001 | Tạo ghi chú cá nhân | Proposed |
| PBI-002 | Ghi chú trong không gian công ty | Proposed |
| PBI-003 | Tạo tài liệu từ mẫu | Proposed |
| PBI-004 | Tìm kiếm tài liệu | Proposed |
