---
name: ba-round-plan
description: Đề xuất mục tiêu và phân bổ PBI vào Round từ backlog/requirements hợp lệ, có dependency, capacity gaps và trạng thái phê duyệt. Round là chu kỳ tùy biến, không mặc định Sprint.
---

# BA-round-plan

## Input Contract

Config, `{planning_dir}/product-backlog.md`, `requirements.md`; goals/capacity/velocity/team constraints tùy chọn. Đọc [conventions](../../conventions/BA-CONVENTIONS.md), [schema](../../contracts/round-plan.schema.json). Resolve KIT_ROOT và project paths theo conventions.

## Input Validation

Cấu hình mới ở `.temp/ba-project.yaml`; `repository_root: .` vẫn là root project. Tìm/đọc bằng `Project.load` theo conventions, tương thích config cũ ở root.

Bố trí file bắt buộc: `planning_dir` phải là `.temp` hoặc thư mục con dưới `.temp` của project. Mọi hồ sơ trung gian/output của bước này (inputs, exploration, backlog, plan, draft, review, request, approvals, state, log/manifest/staging) nằm tại đó. `.specify` chỉ dành cho `Round/PBI-ID-slug/{business.md,spec.md}` do publish tạo. Hai file bàn giao chỉ có nội dung đọc được, không có front matter, BA-DATA, Contract Summary hoặc source hashes; metadata giữ trong `.temp`. Nếu config/đường dẫn cũ dùng `_planning` hoặc `_planing` trong `.specify`, dừng ghi và xử lý migration theo conventions; không tự xóa hồ sơ cũ.

Validate hai nguồn bằng `--project-config <config> --file <path> --expected-type <type> --check-refs`. Resolve dependency graph, phát hiện missing node/cycle. Trong workflow phải đã qua backlog checkpoint. Khi chạy độc lập, chưa duyệt backlog chỉ được tạo bản đề xuất nếu user yêu cầu, không ghi approval thay họ.

## Data Extraction

Đọc PBI IDs, giá trị, readiness, dependencies, priorities, estimation_status và requirement scope. Đọc evidence capacity nếu có; không suy ra velocity từ số PBI.

## Processing

Xác định Round goals theo các lát cắt dùng được. Xếp theo value, risk, dependency và readiness, giải thích allocation_rationale. Số Round theo nhu cầu/capacity, không hardcode. `round_prefix` từ config; thứ tự mảng rounds là thứ tự thực hiện, nhãn không ngầm mang nghĩa Scrum.

Thiếu capacity/estimate: `status: Proposed`, nêu capacity_gaps/assumptions, không cam kết thời lượng/khối lượng. Cho phép `unassigned_pbis`. Mỗi Round có goal, status, pbi_refs, dependencies, risks, capacity_assumptions, capacity_gaps, allocation_rationale, approval_status mặc định Pending.

Mỗi PBI chỉ một active allocation hoặc unassigned. Dependency ở cùng/trước Round; nếu cùng Round thì nêu thứ tự thực hiện. Xem [dependency checklist](references/dependency-checklist.md). Không tạo mới PBI và không đổi ID. Chuyển Round ghi from/to/reason vào history; đã publish thì cần quyết định migration/history trước.

## Output Contract

`{planning_dir}/round-plan.md`, metadata round-plan/ba-round-plan; sources hash backlog/requirements và optional source thực dùng. [Template](references/round-plan-template.md) minh họa, không phải fixed Round count.

## Output Validation

Validator `--expected-type round-plan --check-refs --format json`; kiểm allocation uniqueness, dependency order, PBI coverage, IDs, freshness. CAPACITY_UNKNOWN là warning, không tự thêm estimate để hết warning.

## Error Handling

Thiếu nguồn báo ba-product-backlog/ba-requirements và exact path. Cycle/missing dependency → dừng. Chưa được duyệt → giữ Proposed/Pending; không tự gọi ba-business.

## Traceability

Round tham chiếu đúng PBI backlog; không sao chép PBI thành ID mới. Giữ Round ID có lịch sử, không đổi nhãn đã publish âm thầm. Approved/Proposed Allowed chỉ ghi khi có quyết định thật, kèm record hash theo conventions.

## Example Invocation

`$ba-round-plan project_config=./.temp/ba-project.yaml` — “Đề xuất các Round, chưa có capacity; giữ allocation Proposed.”

## Completion Criteria

Output PASS; tất cả PBI allocated/unassigned rõ; không duplicate/cycle; capacity gap công khai. Báo Round goals, assumptions, hash và checkpoint duyệt/cho phép Proposed. Acceptance: cùng PBI hai Round → fail; thiếu capacity → warning và Proposed.
