---
schema_version: '1.0'
document_type: round-plan
project_id: agent-notes
status: draft
source_documents:
- path: .specify/_planning/product-backlog.md
  sha256: 9d235920a1ea615bd6420162e3812b9ae1b382bb4576d5cba6ac04c1887d8726
- path: .specify/_planning/requirements.md
  sha256: 6b105dd6e09ee90b872a66650ed5b2e3df8fe596f2c5e457498b3dad49284556
generated_by: ba-round-plan
---
# round-plan

<!-- BA-DATA:START -->
```yaml
rounds:
- round_id: R1
  goal: Kiểm chứng tạo và đọc lại ghi chú cá nhân
  status: Proposed
  pbi_refs:
  - PBI-001
  dependencies: []
  risks:
  - Chưa có capacity; UI còn Proposed
  capacity_assumptions: []
  capacity_gaps:
  - Chưa có ước lượng hoặc năng lực nhóm
  allocation_rationale: Chọn lát cắt có quy tắc rõ; các PBI mở rộng chưa ready
  approval_status: Pending
unassigned_pbis:
- PBI-002
- PBI-003
- PBI-004
change_history: []
```
<!-- BA-DATA:END -->

## Round Goals

R1 kiểm chứng hành trình cá nhân, không mặc định Sprint.

## Allocations

Chỉ PBI-001 ở R1; ba PBI còn lại unassigned vì policy còn mở.

## Dependencies

PBI-001 không có dependency; mở rộng chưa được phân bổ.

## Capacity Gaps

Thiếu capacity và estimate: allocation Proposed, không cam kết số ngày.

## Approval State

Chưa gắn Approved; test checkpoint cho phép Proposed có evidence riêng.

## Change History

Kế hoạch đầu tiên, chưa chuyển PBI giữa Round.

## Contract Summary

| ID | Title | State |
| --- | --- | --- |
| R1 | Kiểm chứng tạo và đọc lại ghi chú cá nhân | Pending |
