---
name: ba-workflow
description: Điều phối toàn bộ pipeline BA từ ý tưởng đến backlog, Round, business/spec, review và publish có checkpoint; hỗ trợ INTERACTIVE, DRAFT, RESUME, SINGLE-PBI, SINGLE-ROUND. Dùng khi người dùng yêu cầu nhiều bước hoặc tiếp tục workflow.
---

# BA-workflow

## Input Contract

Ý tưởng mới hoặc workflow state, project_config, mode; selected PBI/round cho mode tương ứng. Đọc [conventions](../../conventions/BA-CONVENTIONS.md), [workflow map](references/workflow-map.md), [checkpoint policy](references/checkpoint-policy.md), [state schema](../../contracts/workflow-state.schema.json). Resolve KIT_ROOT/project paths theo conventions.

## Input Validation

Cấu hình mới ở `.temp/ba-project.yaml`; `repository_root: .` vẫn là root project. Tìm/đọc bằng `Project.load` theo conventions, tương thích config cũ ở root.

Bố trí file bắt buộc: `planning_dir` phải là `.temp` hoặc thư mục con dưới `.temp` của project. Mọi hồ sơ trung gian/output của bước này (inputs, exploration, backlog, plan, draft, review, request, approvals, state, log/manifest/staging) nằm tại đó. `.specify` chỉ dành cho `Round/PBI-ID-slug/{business.md,spec.md}` do publish tạo. Nếu config/đường dẫn cũ dùng `_planning` hoặc `_planing` trong `.specify`, dừng ghi và xử lý migration theo conventions; không tự xóa hồ sơ cũ.

Load config (chưa có → đề xuất template và xác nhận giá trị thiết yếu). Đọc files/state đang có, validate trước dùng; không chạy lại bước còn fresh. SINGLE-PBI cần exact ID; SINGLE-ROUND cần exact Round ID rồi resolve pbi_refs, không đoán. RESUME dùng `python <KIT_ROOT>/scripts/workflow_state.py --project-config <config>` và đọc [recovery guide](references/recovery-guide.md).

## Data Extraction

Đọc current_phase/completed/pending/blockers, artifacts paths/hashes, approvals và selected IDs. State là sổ theo dõi, không chứng minh output hợp lệ; validate file thực và kiểm approval hash lại. Không chỉ tin completed flag.

## Processing

Chạy từng skill bằng cơ chế runtime sẵn có. Nếu không có direct invocation API, đọc SKILL.md của skill tương ứng trong Kit (bản cài có sibling skill folders) và thực hiện đúng instructions bằng công cụ đang có; ghi rõ “manual in-session execution”, không giả vờ gọi thành công một API. Workflow điều phối, không thay hợp đồng từng skill và không mặc định tạo sub-agent.

1. Ý tưởng → ba-brainstorm → validate → ba-requirements → validate → ba-product-backlog → validate.
2. Checkpoint duyệt backlog/scope và quyết định ảnh hưởng lớn. Chưa có quyết định → lưu state, dừng bước phụ thuộc.
3. ba-round-plan → validate → checkpoint Approved hoặc Proposed Allowed. Thiếu capacity giữ Proposed.
4. Với mỗi selected PBI: ba-business → validate → ba-spec → validate → ba-review → validate. FAIL thì báo findings. Chỉ sửa lỗi kỹ thuật trong phạm vi được phép hoặc thay đổi nghiệp vụ đã có quyết định; chỉ retry sau thay đổi có ý nghĩa, không vòng lặp vô hạn.
5. Checkpoint publish cho các bytes/PBI cụ thể. ba-publish dry-run → quyết định còn thiếu → apply → post-validate. Không bypass review freshness hoặc human approval.

Mode INTERACTIVE chạy đến checkpoint tiếp theo. DRAFT tạo draft đến checkpoint chưa được cho phép, không ngầm bypass backlog/Round gate; nếu người dùng đã cho phép tiếp tục draft với Proposed allocation, ghi đúng quyết định đó và không publish. RESUME giữ IDs/decisions, tái kiểm bước bị ảnh hưởng. SINGLE-PBI chỉ xử lý ID đã chọn với nguồn đủ; SINGLE-ROUND dùng allocations đã có, không tự đổi Round.

## Output Contract

`{planning_dir}/workflow-state.md` theo schema state và metadata workflow-state/ba-workflow. Gồm mode, current_phase, completed, pending, blockers, artifacts (path/hash), approvals, last_updated (ISO 8601 có timezone), selected_pbis, selected_round khi cần, change_history. `artifacts` giữ snapshot riêng, metadata.source_documents rỗng để state vẫn đọc được khi output stale. Không sửa app source.

## Output Validation

Sau mỗi handoff, dùng validator `--check-refs --expected-type <type>`; ghi path/schema/hash/result vào state hoặc report. State cũng validate. Chỉ completed khi output tồn tại và PASS; recorded approval không thay review. Check kết quả helper, không coi gọi lệnh là đã thành công.

## Error Handling

Input thiếu khi chạy **toàn pipeline**: được điều phối upstream tương ứng trong phạm vi user yêu cầu, theo đúng thứ tự/checkpoints. Skill đơn lẻ vẫn fail-fast. Missing business trong SINGLE-PBI chỉ điều phối ba-business nếu yêu cầu bao gồm tạo bộ tài liệu, không tự mở rộng yêu cầu “chỉ review”. Invalid nguồn → dừng đúng phase, báo code/path/next action, lưu blockers.

## Traceability

RESUME so hash toàn chain và invalidated downstream; không tự refresh hash để bỏ stale. Giữ Confirmed decisions và IDs; approved sources đổi phải re-checkpoint theo bytes mới. History ghi Round transfer và các bước đã sửa; approval có scope/hashes cụ thể.

## Example Invocation

- `$ba-workflow mode=INTERACTIVE project_config=./.temp/ba-project.yaml` — “Tôi muốn website ghi chú; dừng để duyệt backlog và Round.”
- `$ba-workflow mode=RESUME project_config=./.temp/ba-project.yaml` — “Tiếp tục từ state.”
- `$ba-workflow mode=SINGLE-PBI pbi_id=PBI-001 project_config=./.temp/ba-project.yaml` — “Làm bộ tài liệu draft cho PBI này.”
- `$ba-workflow mode=SINGLE-ROUND round_id=R1 project_config=./.temp/ba-project.yaml` — “Review các PBI trong Round đã chọn.”

## Completion Criteria

State phản ánh việc đã làm và checkpoint còn chờ, output thật PASS và hash recorded. Chỉ hoàn tất toàn pipeline khi selected PBI được publish hợp lệ; dừng checkpoint phải báo là đang chờ, không giả thành completed. Acceptance: unchanged resume → không viết lại; source REQ đổi → invalidate downstream; review FAIL/approval thiếu → không publish.
