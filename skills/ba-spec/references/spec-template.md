> Ví dụ đầy đủ từ fixture giả lập. Dùng ID, hash và quy tắc của dự án đang làm. Khi dùng như template, thay dữ liệu bằng nguồn project đích; đọc schema và giữ headings. Đây là mẫu hồ sơ làm việc nội bộ, chỉ lưu dưới .temp.

> Không copy nguyên mẫu có metadata này vào thư mục PBI. Dùng ba_public.py để preview và ba-publish để xuất bản đọc được; metadata/BA-DATA/Contract Summary giữ trong .temp/drafts.

---
schema_version: '1.0'
document_type: spec
project_id: agent-notes
status: draft
source_documents:
- path: .temp/drafts/PBI-001/business.md
  sha256: a2c9717006738f9c2732959a15c9bdd5af57820e0cb56c0e019d8d4dfa7060ed
- path: .temp/requirements.md
  sha256: c947f2712fcce64155b0661af3c3069fc99df6fc05512d965506b40082fb6237
- path: .temp/product-backlog.md
  sha256: 1093307639ac1f18571232aa33c1dce49bce7f7122ec83859139bf1b1ae259cc
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
title: Tạo ghi chú cá nhân
requirement_refs:
- REQ-001
round_id: R1
user_stories:
- as_a: Người dùng đã đăng nhập
  i_want: Tạo và đọc lại ghi chú cá nhân
  so_that: Lưu thông tin riêng để tái sử dụng
preconditions:
- Người dùng đã đăng nhập
postconditions:
- 'Thành công: một ghi chú thuộc chủ sở hữu, đọc lại đúng nội dung'
- 'Hủy/lỗi dữ liệu hoặc phiên: không tạo ghi chú'
flows:
- flow_id: MF-001
  kind: main
  title: Tạo và đọc lại
  trigger: Gửi tiêu đề và nội dung hợp lệ
  branch_point: Bắt đầu
  steps:
  - step: 1
    actor_action: Mở tạo ghi chú cá nhân
    system_action: Hiện chỗ nhập tiêu đề và nội dung
    input: Phiên người dùng
    result: Form sẵn sàng
  - step: 2
    actor_action: Nhập và gửi tạo
    system_action: Kiểm dữ liệu, quyền hiện tại và thao tác đã xử lý
    input: Tiêu đề/nội dung
    result: Đủ điều kiện hoặc nhánh exception
  - step: 3
    actor_action: Chờ kết quả
    system_action: Lưu một ghi chú với chủ sở hữu hiện tại
    input: Dữ liệu hợp lệ
    result: Một ghi chú được tạo
  - step: 4
    actor_action: Đọc lại ghi chú
    system_action: Hiển thị đúng nội dung cho chủ sở hữu
    input: Ghi chú đã lưu
    result: Người dùng đọc lại được
  termination: Kết thúc tại phản hồi được mô tả
  expected_outcome: Một ghi chú thuộc chủ sở hữu được lưu và đọc lại đúng nội dung
  data_state: Một ghi chú thuộc chủ sở hữu được lưu và đọc lại đúng nội dung
  feedback: Một ghi chú thuộc chủ sở hữu được lưu và đọc lại đúng nội dung
  recovery: Không áp dụng khi đã thành công; mất phản hồi đi EF-003
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
  trigger: Chọn hủy trước khi gửi
  branch_point: MF-001 bước 1 trước khi gửi
  steps:
  - step: 1
    actor_action: Chọn hủy trước khi gửi
    system_action: Không tạo ghi chú
    input: Tiêu đề và nội dung đang soạn
    result: Không tạo ghi chú
  termination: Kết thúc tại phản hồi được mô tả
  expected_outcome: Không tạo ghi chú
  data_state: Không tạo ghi chú
  feedback: Không tạo ghi chú
  recovery: Kết thúc; người dùng có thể bắt đầu thao tác tạo mới
  requirement_refs:
  - REQ-001
  related_br_refs: []
  confirmation_status: Confirmed
- flow_id: EF-001
  kind: exception
  title: Dữ liệu trống
  trigger: Gửi tiêu đề hoặc nội dung rỗng/whitespace
  branch_point: MF-001 bước 2
  steps:
  - step: 1
    actor_action: Gửi tiêu đề hoặc nội dung rỗng/whitespace
    system_action: Không lưu; chỉ rõ trường thiếu để sửa
    input: Tiêu đề và nội dung đang soạn
    result: Không lưu; chỉ rõ trường thiếu để sửa
  termination: Kết thúc tại phản hồi được mô tả
  expected_outcome: Không lưu; chỉ rõ trường thiếu để sửa
  data_state: Không lưu; chỉ rõ trường thiếu để sửa
  feedback: Không lưu; chỉ rõ trường thiếu để sửa
  recovery: Sửa trường thiếu trước khi gửi lại
  requirement_refs:
  - REQ-001
  related_br_refs:
  - BR-002
  confirmation_status: Confirmed
- flow_id: EF-002
  kind: exception
  title: Phiên không hợp lệ
  trigger: Phiên hết hiệu lực trước khi gửi
  branch_point: MF-001 bước 2
  steps:
  - step: 1
    actor_action: Phiên hết hiệu lực trước khi gửi
    system_action: Không lưu và không lộ nội dung
    input: Tiêu đề và nội dung đang soạn
    result: Không lưu và không lộ nội dung
  termination: Kết thúc tại phản hồi được mô tả
  expected_outcome: Không lưu và không lộ nội dung
  data_state: Không lưu và không lộ nội dung
  feedback: Không lưu và không lộ nội dung
  recovery: Xác lập phiên hợp lệ trước thao tác mới; không retry tự động
  requirement_refs:
  - REQ-001
  related_br_refs:
  - BR-001
  confirmation_status: Confirmed
- flow_id: EF-003
  kind: exception
  title: Kết quả chưa rõ
  trigger: Mất phản hồi sau thao tác gửi
  branch_point: MF-001 bước 3 hoặc 4 sau khi gửi, chưa biết kết quả
  steps:
  - step: 1
    actor_action: Mất phản hồi sau thao tác gửi
    system_action: Giữ nội dung; kiểm tra thao tác cũ trước khi gửi lại, không tạo bản sao
    input: Tiêu đề và nội dung đang soạn
    result: Giữ nội dung; kiểm tra thao tác cũ trước khi gửi lại, không tạo bản sao
  termination: Kết thúc tại phản hồi được mô tả
  expected_outcome: Giữ nội dung; kiểm tra thao tác cũ trước khi gửi lại, không tạo bản sao
  data_state: Giữ nội dung; kiểm tra thao tác cũ trước khi gửi lại, không tạo bản sao
  feedback: Giữ nội dung; kiểm tra thao tác cũ trước khi gửi lại, không tạo bản sao
  recovery: Giữ nội dung nếu kết quả chưa rõ; kiểm tra thao tác cũ trước khi gửi lại
  requirement_refs:
  - REQ-001
  related_br_refs:
  - BR-003
  confirmation_status: Confirmed
- flow_id: EF-004
  kind: exception
  title: Người khác đọc
  trigger: Tài khoản khác mở ghi chú cá nhân
  branch_point: MF-001 bước 4
  steps:
  - step: 1
    actor_action: Tài khoản khác mở ghi chú cá nhân
    system_action: Không hiển thị nội dung của chủ sở hữu khác
    input: Tham chiếu ghi chú và phiên tài khoản đọc
    result: Không hiển thị nội dung của chủ sở hữu khác
  termination: Kết thúc tại phản hồi được mô tả
  expected_outcome: Không hiển thị nội dung của chủ sở hữu khác
  data_state: Ghi chú của chủ sở hữu không thay đổi; không trả nội dung cho tài khoản khác
  feedback: Không hiển thị nội dung của chủ sở hữu khác
  recovery: Kết thúc nhánh đọc bị từ chối; không cung cấp nội dung hoặc thử đọc lại dưới quyền khác
  requirement_refs:
  - REQ-001
  related_br_refs:
  - BR-001
  confirmation_status: Confirmed
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
permissions:
- text: Chỉ chủ sở hữu được đọc; kiểm tra phiên/quyền khi gửi, hết quyền thì không lưu.
  confirmation_status: Confirmed
  source_refs:
  - idea.txt
  - scenario.txt
data_states:
- text: Đang soạn → đã lưu khi thành công; lỗi dữ liệu/phiên không tạo ghi chú; chưa rõ kết quả giữ nội dung để
    đối soát.
  confirmation_status: Confirmed
  source_refs:
  - idea.txt
  - scenario.txt
edge_cases:
- ec_id: EC-001
  title: Trống hoặc whitespace
  scenario: Tiêu đề/nội dung không có ký tự hữu ích
  preconditions:
  - Form tạo cá nhân đã mở
  expected_behavior: Không lưu, nêu trường thiếu
  requirement_refs:
  - REQ-001
  related_br_refs:
  - BR-002
  related_ac_refs:
  - AC-003
  confirmation_status: Confirmed
- ec_id: EC-002
  title: Phiên thay đổi
  scenario: Phiên hết hiệu lực sau khi form mở
  preconditions:
  - Form tạo cá nhân đã mở
  expected_behavior: Không lưu và không lộ nội dung
  requirement_refs:
  - REQ-001
  related_br_refs:
  - BR-001
  related_ac_refs:
  - AC-004
  confirmation_status: Confirmed
- ec_id: EC-003
  title: Timeout sau thành công
  scenario: Server lưu nhưng phản hồi bị mất
  preconditions:
  - Form tạo cá nhân đã mở
  expected_behavior: Kiểm tra thao tác cũ; hiển thị kết quả đã lưu và không tạo bản sao
  requirement_refs:
  - REQ-001
  related_br_refs:
  - BR-003
  related_ac_refs:
  - AC-005
  confirmation_status: Confirmed
- ec_id: EC-004
  title: Rapid click
  scenario: Cùng thao tác được gửi nhiều lần liên tiếp
  preconditions:
  - Form tạo cá nhân đã mở
  expected_behavior: Chỉ một ghi chú cho cùng thao tác
  requirement_refs:
  - REQ-001
  related_br_refs:
  - BR-003
  related_ac_refs:
  - AC-007
  confirmation_status: Confirmed
acceptance_criteria:
- ac_id: AC-001
  title: Tạo và đọc lại
  given: Người dùng đã mở form tạo cá nhân với dữ liệu đang nhập
  when: Gửi tiêu đề và nội dung hợp lệ
  then: Một ghi chú thuộc chủ sở hữu được lưu và đọc lại đúng nội dung
  requirement_refs:
  - REQ-001
  flow_refs:
  - MF-001
  edge_case_refs: []
  confirmation_status: Confirmed
- ac_id: AC-002
  title: Hủy tạo
  given: Người dùng đã mở form tạo cá nhân với dữ liệu đang nhập
  when: Chọn hủy trước khi gửi
  then: Không tạo ghi chú
  requirement_refs:
  - REQ-001
  flow_refs:
  - AF-001
  edge_case_refs: []
  confirmation_status: Confirmed
- ac_id: AC-003
  title: Dữ liệu trống
  given: Người dùng đã mở form tạo cá nhân với dữ liệu đang nhập
  when: Gửi tiêu đề hoặc nội dung rỗng/whitespace
  then: Không lưu; chỉ rõ trường thiếu để sửa
  requirement_refs:
  - REQ-001
  flow_refs:
  - EF-001
  edge_case_refs:
  - EC-001
  confirmation_status: Confirmed
- ac_id: AC-004
  title: Phiên không hợp lệ
  given: Người dùng đã mở form tạo cá nhân với dữ liệu đang nhập
  when: Phiên hết hiệu lực trước khi gửi
  then: Không lưu và không lộ nội dung
  requirement_refs:
  - REQ-001
  flow_refs:
  - EF-002
  edge_case_refs:
  - EC-002
  confirmation_status: Confirmed
- ac_id: AC-005
  title: Kết quả chưa rõ
  given: Server đã lưu một ghi chú cho thao tác của chủ sở hữu nhưng client mất phản hồi
  when: Mất phản hồi sau thao tác gửi
  then: Sau khi kiểm tra thao tác cũ, hiển thị đúng ghi chú đã lưu cho chủ sở hữu và không tạo bản sao
  requirement_refs:
  - REQ-001
  flow_refs:
  - EF-003
  edge_case_refs:
  - EC-003
  confirmation_status: Confirmed
- ac_id: AC-006
  title: Người khác đọc
  given: Một ghi chú cá nhân đã được tài khoản A tạo; tài khoản B không phải chủ sở hữu
  when: Tài khoản khác mở ghi chú cá nhân
  then: Không hiển thị nội dung của chủ sở hữu khác
  requirement_refs:
  - REQ-001
  flow_refs:
  - EF-004
  edge_case_refs: []
  confirmation_status: Confirmed
- ac_id: AC-007
  title: Gửi lặp cùng thao tác
  given: Một thao tác tạo với dữ liệu hợp lệ
  when: Gửi lặp cùng thao tác khi chưa nhận phản hồi
  then: Chỉ một ghi chú được tạo cho thao tác đó
  requirement_refs:
  - REQ-001
  flow_refs:
  - MF-001
  - EF-003
  edge_case_refs:
  - EC-004
  confirmation_status: Confirmed
traceability:
- requirement_id: REQ-001
  br_refs:
  - BR-001
  - BR-002
  - BR-003
  flow_refs:
  - MF-001
  - AF-001
  - EF-001
  - EF-002
  - EF-003
  - EF-004
  ec_refs:
  - EC-001
  - EC-002
  - EC-003
  - EC-004
  ac_refs:
  - AC-001
  - AC-002
  - AC-003
  - AC-004
  - AC-005
  - AC-006
  - AC-007
scope:
- Ghi chú được lưu riêng cho chủ sở hữu và có thể đọc lại
out_of_scope:
- Ghi chú trong không gian công ty
- Tạo tài liệu từ mẫu
- Tìm kiếm tài liệu
open_questions:
- Nhãn hành động và bố cục UI cần refinement
blockers: []
change_history:
- at: '2026-11-17T00:00:00+07:00'
  change: Làm rõ AC-005 và EF-004; recovery riêng cho từng nhánh, giữ toàn bộ IDs và BR nguồn.
  affected_ids:
  - AC-005
  - EF-004
  - EF-003
  reason: Giải quyết FIND-001/FIND-002, không thay quyết định nghiệp vụ.
```
<!-- BA-DATA:END -->

## PBI Information

PBI-001 / REQ-001, R1 Proposed; chỉ tạo/đọc lại ghi chú cá nhân.

## User Stories

Là người dùng đã đăng nhập, tôi muốn lưu ghi chú riêng để đọc lại.

## Preconditions

Đã đăng nhập trước khi mở form; phiên vẫn phải được kiểm lại khi ghi.

## Postconditions

Thành công có một ghi chú đúng chủ sở hữu; hủy/lỗi không tạo.

## Main Flow

Mở form → nhập/gửi → kiểm quyền/dữ liệu/thao tác trùng → lưu → đọc lại. Steps chi tiết nằm trong BA-DATA.

## Alternative Flows

Hủy trước khi gửi kết thúc mà không tạo ghi chú.

## Exception Flows

Dữ liệu trống, phiên hết hiệu lực, mất phản hồi và người khác đọc đều có outcome riêng; không gom thành lỗi chung. Nhánh đọc trái quyền không trả dữ liệu và không đổi ghi chú nguồn; timeout kiểm tra kết quả đã lưu trước retry.

## Business Rules

Giữ nguyên BR-001..003 từ requirements, không chốt API/DB hoặc thuật toán chống trùng.

## Permissions

Chỉ chủ sở hữu được đọc. Người khác không thấy nội dung.

## Data and States

Đang soạn, đã lưu hoặc chưa rõ kết quả; không tự coi timeout là thất bại lưu.

## Edge Cases

EC bao phủ whitespace, phiên thay đổi, timeout sau success và rapid click. Không xét parent deletion vì PBI này không tạo trong thư mục/công ty.

## Acceptance Criteria

Bảy AC Given/When/Then bao phủ success, cancel, invalid input, auth, timeout, ownership và duplicate submission. AC-005 xác định server đã lưu và buộc hiển thị đúng kết quả sau đối soát.

## Traceability

REQ-001 → ba BR, sáu Flow, bốn EC → bảy AC, tất cả thuộc cùng PBI.

## Scope

Công ty, mẫu và tìm kiếm nằm ngoài scope PBI cá nhân.

## Open Questions

Nhãn/bố cục UI còn Proposed; giới hạn độ dài và performance chưa chốt cho production. Đây là bản draft kiểm chứng hành vi.

## Contract Summary

| ID | Title | State |
| --- | --- | --- |
| PBI-001 | Tạo ghi chú cá nhân | — |
| BR-001 | Sở hữu cá nhân | Confirmed |
| BR-002 | Thông tin bắt buộc | Confirmed |
| BR-003 | Không lặp tác dụng | Confirmed |
| MF-001 | Tạo và đọc lại | Confirmed |
| AF-001 | Hủy tạo | Confirmed |
| EF-001 | Dữ liệu trống | Confirmed |
| EF-002 | Phiên không hợp lệ | Confirmed |
| EF-003 | Kết quả chưa rõ | Confirmed |
| EF-004 | Người khác đọc | Confirmed |
| EC-001 | Trống hoặc whitespace | Confirmed |
| EC-002 | Phiên thay đổi | Confirmed |
| EC-003 | Timeout sau thành công | Confirmed |
| EC-004 | Rapid click | Confirmed |
| AC-001 | Tạo và đọc lại | Confirmed |
| AC-002 | Hủy tạo | Confirmed |
| AC-003 | Dữ liệu trống | Confirmed |
| AC-004 | Phiên không hợp lệ | Confirmed |
| AC-005 | Kết quả chưa rõ | Confirmed |
| AC-006 | Người khác đọc | Confirmed |
| AC-007 | Gửi lặp cùng thao tác | Confirmed |
