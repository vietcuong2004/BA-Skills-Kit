> Ví dụ đầy đủ từ fixture giả lập. Không sao chép IDs, hashes, policy hay approval sang project thật. Khi dùng như template, thay dữ liệu bằng nguồn project đích; đọc schema và giữ headings. Đây là mẫu hồ sơ làm việc nội bộ, chỉ lưu dưới .temp.

---
schema_version: '1.0'
document_type: round-plan
project_id: agent-notes
status: draft
source_documents:
- path: .temp/product-backlog.md
  sha256: 1093307639ac1f18571232aa33c1dce49bce7f7122ec83859139bf1b1ae259cc
- path: .temp/requirements.md
  sha256: c947f2712fcce64155b0661af3c3069fc99df6fc05512d965506b40082fb6237
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
