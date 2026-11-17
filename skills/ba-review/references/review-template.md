> Ví dụ đầy đủ từ fixture giả lập. Không sao chép IDs, hashes, policy hay approval sang project thật. Khi dùng như template, thay dữ liệu bằng nguồn project đích; đọc schema và giữ headings.

---
schema_version: '1.0'
document_type: review
project_id: agent-notes
status: draft
source_documents:
- path: .specify/_planning/drafts/PBI-001/business.md
  sha256: b145a0531ccf204e1ae02e21f2ffdaa70caf962bcebe7a54dbdd7bbdf0853eb7
- path: .specify/_planning/drafts/PBI-001/spec.md
  sha256: 8259f2ab88d4657f0d2b554496a99f09f5e5f1ab927747800de15b10f66652f1
- path: .specify/_planning/requirements.md
  sha256: 6b105dd6e09ee90b872a66650ed5b2e3df8fe596f2c5e457498b3dad49284556
- path: .specify/_planning/product-backlog.md
  sha256: 9d235920a1ea615bd6420162e3812b9ae1b382bb4576d5cba6ac04c1887d8726
generated_by: ba-review
pbi_id: PBI-001
epic_id: EPIC-001
feature_id: FEAT-001
round_id: R1
requirement_refs:
- REQ-001
---
# review

<!-- BA-DATA:START -->
```yaml
pbi_id: PBI-001
epic_id: EPIC-001
feature_id: FEAT-001
title: Tạo ghi chú cá nhân
requirement_refs:
- REQ-001
round_id: R1
result: CONDITIONAL
readiness: Needs Refinement
blockers: []
findings:
- finding_id: FIND-001
  severity: Major
  file: .specify/_planning/drafts/PBI-001/spec.md
  section: Acceptance Criteria / AC-005
  evidence: Sau khi kiểm tra thao tác cũ, hiển thị đúng ghi chú đã lưu cho chủ sở hữu và không tạo bản sao
  impact: AC chưa chứng minh hiển thị lại kết quả server đã lưu như EC-003 yêu cầu.
  recommendation: Nêu Given thao tác đã lưu nhưng mất phản hồi, Then trả đúng ghi chú đã lưu và không tạo bản sao.
  status: Resolved
- finding_id: FIND-002
  severity: Major
  file: .specify/_planning/drafts/PBI-001/spec.md
  section: Exception Flows / EF-004
  evidence: Tham chiếu ghi chú và phiên tài khoản đọc / Kết thúc nhánh đọc bị từ chối; không cung cấp nội dung hoặc
    thử đọc lại dưới quyền khác
  impact: Nhánh đọc trái quyền dùng input/recovery của form tạo; chưa mô tả đúng trạng thái dữ liệu cần bảo vệ.
  recommendation: Đổi input thành tham chiếu ghi chú và phiên tài khoản đọc; không trả nội dung, ghi chú nguồn không
    đổi, kết thúc nhánh.
  status: Resolved
- finding_id: FIND-003
  severity: Minor
  file: .specify/_planning/drafts/PBI-001/business.md
  section: Giải pháp phần mềm chi tiết
  evidence: Không gian cá nhân, hành động tạo mới (UI Proposed)
  impact: Nhãn hành động/bố cục UI chưa được refinement; không thay outcome đã xác định.
  recommendation: Giữ Proposed trong draft; chốt nhãn khi thiết kế giao diện.
  status: Open
coverage_notes:
- So business goal/scope với REQ-001, ba BR, sáu flows, bốn EC và bảy AC; không lẫn công ty/mẫu/search.
- Kiểm whitespace, ownership, phiên thay đổi, cancel, timeout sau success và duplicate submission; không tự đặt
  SLA/length cap.
change_history:
- at: '2026-11-17T00:00:00+07:00'
  change: FIND-001 và FIND-002 được giải quyết sau refinement spec; giữ FIND-003 mở.
  affected_ids:
  - FIND-001
  - FIND-002
  reason: Đã kiểm chứng lại AC-005 và EF-004 theo cùng rule nguồn.
```
<!-- BA-DATA:END -->

## Review Result

CONDITIONAL: structural PASS không thay review ngữ nghĩa hoặc human approval.

## Findings

FIND-001 — Major / Resolved: Sau khi kiểm tra thao tác cũ, hiển thị đúng ghi chú đã lưu cho chủ sở hữu và không tạo bản sao → Nêu Given thao tác đã lưu nhưng mất phản hồi, Then trả đúng ghi chú đã lưu và không tạo bản sao.

FIND-002 — Major / Resolved: Tham chiếu ghi chú và phiên tài khoản đọc / Kết thúc nhánh đọc bị từ chối; không cung cấp nội dung hoặc thử đọc lại dưới quyền khác → Đổi input thành tham chiếu ghi chú và phiên tài khoản đọc; không trả nội dung, ghi chú nguồn không đổi, kết thúc nhánh.

FIND-003 — Minor / Open: Không gian cá nhân, hành động tạo mới (UI Proposed) → Giữ Proposed trong draft; chốt nhãn khi thiết kế giao diện.

## Coverage

REQ-001 trace đầy đủ. Đã đọc nội dung business/spec, không chỉ kiểm Contract Summary.

## Readiness

Needs Refinement

## Blockers

Không còn Major/Critical; còn Minor về UI, chỉ phù hợp draft publication nếu được cho phép.

## Sources

Review hash đúng business/spec hiện tại; không sửa hai nguồn trong bước review.

## Contract Summary

| ID | Title | State |
| --- | --- | --- |
| PBI-001 | Tạo ghi chú cá nhân | CONDITIONAL |
| FIND-001 | Sau khi kiểm tra thao tác cũ, hiển thị đúng ghi chú đã lưu cho chủ sở hữu và không tạo bản sao | Resolved |
| FIND-002 | Tham chiếu ghi chú và phiên tài khoản đọc / Kết thúc nhánh đọc bị từ chối; không cung cấp nội dung hoặc thử đọc lại dưới quyền khác | Resolved |
| FIND-003 | Không gian cá nhân, hành động tạo mới (UI Proposed) | Open |
