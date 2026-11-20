---
name: ba-round-plan
description: Phân bổ PBI vào các đợt từ backlog và requirements, theo phụ thuộc và thông tin ước lượng hiện có.
---

# BA-round-plan

## Input Contract

Config, `{planning_dir}/product-backlog.md`, `requirements.md`; goals/capacity/velocity/team constraints tùy chọn. Đọc [conventions](../../conventions/BA-CONVENTIONS.md), [schema](../../contracts/round-plan.schema.json). Resolve KIT_ROOT và project paths theo conventions.

## Input Validation

Đọc `.temp/ba-project.yaml` bằng `Project.load` theo quy ước chung. Giá trị `repository_root: .` chỉ thư mục dự án chứa `.temp`.

Bố trí file bắt buộc: `planning_dir` phải là `.temp` hoặc thư mục con dưới `.temp` của project. Mọi hồ sơ trung gian/output của bước này (inputs, exploration, backlog, plan, draft, review, request, state, log/manifest/staging) nằm tại đó. `.specify` chỉ dành cho `Round/PBI-ID-slug/{business.md,spec.md}` do publish tạo. Hai file bàn giao chỉ có nội dung đọc được, không có front matter, BA-DATA, Contract Summary hoặc source hashes; metadata giữ trong `.temp`. Nếu config/đường dẫn cũ dùng `_planning` hoặc `_planing` trong `.specify`, dừng ghi và xử lý migration theo conventions; không tự xóa hồ sơ cũ.

Validate hai nguồn bằng `--project-config <config> --file <path> --expected-type <type> --check-refs`. Kiểm tra phụ thuộc trước khi phân bổ. Dùng backlog hợp lệ để tiếp tục lập Round.

## Data Extraction

Đọc PBI IDs, giá trị, readiness, dependencies, priorities, estimation_status và requirement scope. Đọc evidence capacity nếu có; không suy ra velocity từ số PBI.

## Processing

Xác định Round goals theo các lát cắt dùng được. Xếp theo value, risk, dependency và readiness, giải thích allocation_rationale. Số Round theo nhu cầu/capacity, không hardcode. `round_prefix` từ config; thứ tự mảng rounds là thứ tự thực hiện, nhãn không ngầm mang nghĩa Scrum.

Thiếu capacity/ước lượng thì dùng `status: Proposed` và nêu khoảng trống. Phân bổ các PBI trong phạm vi cần xuất. Dùng `unassigned_pbis` cho mục ngoài phạm vi hoặc thiếu phụ thuộc. Mỗi Round có goal, status, pbi_refs, dependencies, risks, capacity_assumptions, capacity_gaps và allocation_rationale.

Mỗi PBI chỉ một active allocation hoặc unassigned. Dependency ở cùng/trước Round; nếu cùng Round thì nêu thứ tự thực hiện. Xem [dependency checklist](references/dependency-checklist.md). Không tạo mới PBI và không đổi ID. Chuyển Round ghi from/to/reason vào history; đã publish thì cần quyết định migration/history trước.

## Output Contract

`{planning_dir}/round-plan.md`, metadata round-plan/ba-round-plan; sources hash backlog/requirements và optional source thực dùng. [Template](references/round-plan-template.md) minh họa, không phải fixed Round count.

## Output Validation

Validator `--expected-type round-plan --check-refs --format json`; kiểm allocation uniqueness, dependency order, PBI coverage, IDs, freshness. CAPACITY_UNKNOWN là warning, không tự thêm estimate để hết warning.

## Error Handling

Thiếu nguồn thì báo đường dẫn và skill tạo nguồn. Sửa chu trình hoặc phụ thuộc sai từ nguồn trước khi bàn giao. Phân bổ Proposed hợp lệ có thể được workflow dùng để viết và xuất PBI.

## Traceability

Round tham chiếu đúng PBI backlog; không sao chép PBI thành ID mới. Giữ Round ID có lịch sử, không đổi nhãn đã publish âm thầm. Approved/Proposed Allowed chỉ ghi khi có quyết định thật, kèm record hash theo conventions.

## Example Invocation

`$ba-round-plan project_config=./.temp/ba-project.yaml` — “Đề xuất các Round, chưa có capacity; giữ allocation Proposed.”

## Completion Criteria

Output hợp lệ, mỗi PBI có đúng một Round hoặc được ghi là chưa phân bổ. Báo phân bổ và khoảng trống capacity. Một PBI xuất hiện ở hai Round hoặc có vòng lặp là lỗi kỹ thuật.
