> Ví dụ đầy đủ từ fixture giả lập. Dùng ID, hash và quy tắc của dự án đang làm. Khi dùng như template, thay dữ liệu bằng nguồn project đích; đọc schema và giữ headings. Đây là mẫu hồ sơ làm việc nội bộ, chỉ lưu dưới .temp.

---
schema_version: '1.0'
document_type: brainstorm
project_id: agent-notes
status: draft
source_documents:
- path: idea.txt
  sha256: 8958f3b89e4b8ba3001ea88d1a7eb69e06c6e7be7b6bd47146ee6f6b64e09248
- path: scenario.txt
  sha256: b677361b715a3f5d8f19fb47d15ccbf1bbb6bd362414dcd32daa4966f295f0a8
generated_by: ba-brainstorm
---
# brainstorm

<!-- BA-DATA:START -->
```yaml
product_overview:
  text: Tôi muốn website ghi chú cá nhân, ghi chú công ty, tạo tài liệu từ mẫu và tìm kiếm.
  confirmation_status: Confirmed
  source_refs:
  - idea.txt
  - scenario.txt
vision:
  text: Lưu tri thức cá nhân và tổ chức, sau đó tìm lại khi cần.
  confirmation_status: Proposed
  source_refs:
  - idea.txt
  - scenario.txt
target_users:
- Người dùng cá nhân
- Thành viên công ty
problems:
- text: Ghi chú phân tán làm khó tái sử dụng thông tin.
  confirmation_status: Proposed
  source_refs:
  - idea.txt
  - scenario.txt
jobs_to_be_done:
- text: Ghi lại thông tin trong không gian phù hợp rồi tìm lại.
  confirmation_status: Proposed
  source_refs:
  - idea.txt
  - scenario.txt
capabilities:
- capability_id: CAP-001
  name: Tạo ghi chú cá nhân
  description: Tạo ghi chú cá nhân
  target_users:
  - Người dùng đã đăng nhập
  business_value: Lưu và tái sử dụng thông tin theo ngữ cảnh
  source_refs:
  - idea.txt
  confirmation_status: Confirmed
- capability_id: CAP-002
  name: Ghi chú trong không gian công ty
  description: Ghi chú trong không gian công ty
  target_users:
  - Người dùng đã đăng nhập
  business_value: Lưu và tái sử dụng thông tin theo ngữ cảnh
  source_refs:
  - idea.txt
  confirmation_status: Confirmed
- capability_id: CAP-003
  name: Tạo tài liệu từ mẫu
  description: Tạo tài liệu từ mẫu
  target_users:
  - Người dùng đã đăng nhập
  business_value: Lưu và tái sử dụng thông tin theo ngữ cảnh
  source_refs:
  - idea.txt
  confirmation_status: Confirmed
- capability_id: CAP-004
  name: Tìm kiếm tài liệu
  description: Tìm kiếm tài liệu
  target_users:
  - Người dùng đã đăng nhập
  business_value: Lưu và tái sử dụng thông tin theo ngữ cảnh
  source_refs:
  - idea.txt
  confirmation_status: Confirmed
goals:
- text: Kiểm chứng tạo và đọc lại ghi chú cá nhân trước khi mở rộng.
  confirmation_status: Proposed
  source_refs:
  - idea.txt
  - scenario.txt
scope:
- text: Tạo ghi chú cá nhân, Ghi chú trong không gian công ty, Tạo tài liệu từ mẫu, Tìm kiếm tài liệu
  confirmation_status: Confirmed
  source_refs:
  - idea.txt
  - scenario.txt
exclusions:
- text: Cộng tác thời gian thực chưa nằm trong ý tưởng đầu vào.
  confirmation_status: Proposed
  source_refs:
  - idea.txt
  - scenario.txt
constraints:
- text: Quy tắc cá nhân được cung cấp trong scenario.txt.
  confirmation_status: Confirmed
  source_refs:
  - idea.txt
  - scenario.txt
assumptions:
- text: Một tài khoản có thể tham gia không gian công ty, cần xác minh.
  confirmation_status: Proposed
  source_refs:
  - idea.txt
  - scenario.txt
open_questions:
- Ai cấp quyền công ty?
- Ai quản lý mẫu?
- Tìm kiếm hỗ trợ phạm vi nào?
metrics: []
change_history: []
```
<!-- BA-DATA:END -->

## Product Overview

Website ghi chú với bốn nhu cầu được lưu nguyên văn trong idea.txt.

## Vision

Đề xuất một nơi lưu và tái sử dụng tri thức; chưa có nghiên cứu xác nhận mức độ nhu cầu.

## Target Users

Người dùng cá nhân và thành viên công ty. Vai trò quản trị công ty cần làm rõ.

## Problems

Giả thuyết: thông tin phân tán khiến khó tìm lại; không phải kết quả nghiên cứu.

## Capabilities

Bốn capability: cá nhân, công ty, mẫu và tìm kiếm; không bỏ sót nhu cầu.

## Goals

Ưu tiên tạo và đọc lại ghi chú cá nhân là đề xuất dùng để lập backlog.

## Scope

Bao gồm bốn nhu cầu đã nêu. Cộng tác thời gian thực chưa được yêu cầu.

## Assumptions

Chính sách đa không gian cần xác minh; quy tắc fixture cá nhân được cung cấp riêng.

## Open Questions

Cần làm rõ quyền công ty, quản lý mẫu và phạm vi tìm kiếm.

## Metrics

Chưa có baseline hoặc KPI; không tự đặt số.

## Contract Summary

| ID | Title | State |
| --- | --- | --- |
| CAP-001 | Tạo ghi chú cá nhân | Confirmed |
| CAP-002 | Ghi chú trong không gian công ty | Confirmed |
| CAP-003 | Tạo tài liệu từ mẫu | Confirmed |
| CAP-004 | Tìm kiếm tài liệu | Confirmed |
