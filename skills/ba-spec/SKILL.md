---
name: ba-spec
description: Tạo đặc tả Dev/QA cho một PBI từ business draft hợp lệ, gồm main/alternative/exception flows, rules, edge cases, Given–When–Then AC và traceability. Không tự tạo business hay quyết định thay PO.
---

# BA-spec

## Input Contract

`pbi_id`, config, `{planning_dir}/drafts/{pbi_id}/business.md`, requirements.md, product-backlog.md bắt buộc. Đọc [conventions](../../conventions/BA-CONVENTIONS.md), [spec schema](../../contracts/spec.schema.json); resolve KIT_ROOT/project paths theo conventions.

## Input Validation

Validate từng nguồn bằng `--check-refs --expected-type <type>`; business thêm `--pbi-id <requested-id>`. Business PBI = requested PBI = backlog PBI; cùng project/version, source hashes fresh. Business thiếu → báo ba-business và exact path, dừng; không tự tạo business thay.

## Data Extraction

Đọc BA-DATA đúng PBI: actor, story, goals, scope/exclusions, requirements, BR/permission, proposed decisions, blockers, data/state, Round. Resolve nguồn của rule. Không lấy mọi requirement trong project vào spec một PBI.

## Processing

1. Viết As a / I want / So that; preconditions và postconditions quan sát được, không áp API/database design khi chưa được yêu cầu.
2. Main Flow MF-xxx có start/end, bước liên tục từ 1, actor_action/system_action/input/result. Alternative AF-xxx có trigger, branch_point, steps, rejoin/termination và expected_outcome. Exception EF-xxx có error trigger, system behavior, data_state, feedback và recovery/retry. Xem [flow guide](references/flow-guide.md).
3. BR nguồn giữ ID và nghĩa; rule mới chưa có nguồn phải Proposed, có evidence về lý do đề xuất. Permissions/data_states có nhãn. Nếu thay rule dùng chung, đề xuất cập nhật requirements và revalidate, không gán cùng BR ID cho nghĩa khác.
4. Chọn EC liên quan theo [checklist](references/edge-case-checklist.md). Mỗi EC có scenario/preconditions, requirement_refs, related_br_refs/related_ac_refs và expected_behavior **hoặc** open_question + Open Question. Không tự đặt min/max hay retry policy. Critical outcome chưa chốt → `blockers`.
5. Viết AC Given/When/Then có thể kiểm chứng, cover success, alternative, error và EC rủi ro cao. Mỗi AC có requirement_refs, flow_refs, edge_case_refs. [GWT guide](references/ac-gwt-guide.md) phân biệt tiêu chí với test steps.
6. Lập REQ ↔ BR/Flow/EC ↔ AC matrix. Không dangling refs, mọi AC nằm trong traceability, mọi requirement của PBI được coverage. Kiểm ngữ nghĩa với business, rules và scope, không chỉ đủ trường YAML.

## Output Contract

`{planning_dir}/drafts/{pbi_id}/spec.md`, metadata spec/ba-spec, đúng identity/requirement_refs và Round từ business nếu đã có. Sources chứa business/backlog/requirements raw-byte hashes. [Template](references/spec-template.md) là ví dụ đủ contract; [folder example](references/folder-example.md) minh họa cách viết hành vi, không chốt quyền mặc định.

## Output Validation

Validator `--project-config <config> --file <spec-path> --expected-type spec --pbi-id <pbi_id> --check-refs --format json`. Kiểm GWT không rỗng, EC outcome/question, local IDs, scope, refs, trace coverage, hash và headings. Sửa format trong phạm vi, không tự sửa business.md.

## Error Handling

Missing/wrong PBI/stale nguồn → dừng, báo code/file/upstream skill. Unconfirmed critical behavior → dừng hoặc draft với blockers rõ; không tự duyệt. Không chạy review/publish trong skill đơn lẻ.

## Traceability

AC/EC/Flow định danh theo PBI; update giữ IDs, history, quyết định Confirmed. Spec đổi → review stale, cần review lại. Hash lấy từ nguồn thực đọc; kiểm lại nếu có thay đổi đồng thời.

## Example Invocation

`$ba-spec pbi_id=PBI-001 project_config=./ba-project.yaml` — “Đọc business đúng PBI và viết flows, edge cases, AC.”

## Completion Criteria

Spec đúng PBI, input/output PASS, mọi REQ/AC trace được, semantic review sơ bộ không mâu thuẫn business; blockers được báo. Acceptance: missing GWT/EC outcome → fail; Open Question EC rõ → draft warning; PBI mismatch → fail-fast.
