---
name: ba-product-backlog
description: Phân rã brainstorm và requirements hợp lệ thành Epic, Feature và PBI theo vertical slicing, INVEST và requirement coverage. Dùng khi lập hoặc cập nhật product backlog, không tự estimate hay lập Round.
---

# BA-product-backlog

## Input Contract

Config, `{planning_dir}/brainstorm.md` và `requirements.md`. Đọc [conventions](../../conventions/BA-CONVENTIONS.md), [schema](../../contracts/product-backlog.schema.json); resolve KIT_ROOT/project paths theo conventions.

## Input Validation

Đọc `.temp/ba-project.yaml` bằng `Project.load` theo quy ước chung. Giá trị `repository_root: .` chỉ thư mục dự án chứa `.temp`.

Bố trí file bắt buộc: `planning_dir` phải là `.temp` hoặc thư mục con dưới `.temp` của project. Mọi hồ sơ trung gian/output của bước này (inputs, exploration, backlog, plan, draft, review, request, state, log/manifest/staging) nằm tại đó. `.specify` chỉ dành cho `Round/PBI-ID-slug/{business.md,spec.md}` do publish tạo. Hai file bàn giao chỉ có nội dung đọc được, không có front matter, BA-DATA, Contract Summary hoặc source hashes; metadata giữ trong `.temp`. Nếu config/đường dẫn cũ dùng `_planning` hoặc `_planing` trong `.specify`, dừng ghi và xử lý migration theo conventions; không tự xóa hồ sơ cũ.

Validate từng file với `--project-config <config> --file <path> --expected-type <type> --check-refs`. Cùng project/version, không stale; REQ.capability_refs phải tồn tại. Chưa đạt thì dừng tại nguồn lỗi.

## Data Extraction

Đọc CAP, REQ IDs, actors, outcomes, scope, BR, assumptions/confirmation và dependencies có evidence. Giữ các yêu cầu chưa chốt riêng; không coi việc nằm trong requirements là được duyệt.

## Processing

Nhóm Epic → Feature theo giá trị sản phẩm, không chỉ menu UI. Phân rã thành PBI có kết quả người dùng quan sát được, gồm cả hành trình cần để nghiệm thu. Xem [INVEST](references/invest-checklist.md) và [vertical slices](references/vertical-slicing-examples.md). Không tạo PBI chỉ “frontend”, “backend” hoặc technical task khi người dùng đang yêu cầu backlog nghiệp vụ.

Mỗi PBI có pbi_id, epic_id, feature_id, title, user_story, business_value, scope/out_of_scope, requirement_refs, dependencies, priority_proposal, estimation_status=Unestimated, confirmation_status, open_questions và lý do INVEST. Không tự đặt story points. Feature ghi requirement_refs và đúng Epic parent.

Kiểm tra mục trùng, PBI quá lớn, vòng lặp phụ thuộc và coverage. Mỗi REQ thuộc ít nhất một PBI hoặc nằm trong unassigned_requirements kèm lý do. Dùng một REQ ở nhiều PBI khi các lát cắt khác giá trị. Ghi ưu tiên đề xuất để workflow lập Round từ backlog hợp lệ.

## Output Contract

`{planning_dir}/product-backlog.md`, metadata product-backlog/ba-product-backlog; sources chứa cả brainstorm và requirements. Dùng [template](references/backlog-template.md). Bảng hiển thị phải khớp BA-DATA IDs/title/status.

## Output Validation

Validator `--expected-type product-backlog --check-refs --format json`; kiểm parent, scope, ID, refs, coverage và freshness. Đọc lại nội dung để kiểm INVEST thật, không chỉ presence của field.

## Error Handling

Thiếu brainstorm → ba-brainstorm; thiếu requirements → ba-requirements. Không tái tạo input hoặc tự lập Round. Giả định còn mở → Proposed/draft, ghi câu hỏi ảnh hưởng phạm vi.

## Traceability

CAP → REQ → Feature → PBI. Giữ ID khi cập nhật và ghi lịch sử thay đổi. Kiểm tra tác động tới Round, draft và review khi backlog đổi.

## Example Invocation

`$ba-product-backlog project_config=./.temp/ba-project.yaml` — “Tạo backlog có thể duyệt từ requirements.” Ví dụ 1 CAP → 2 REQ → 1 Epic/Feature → 2 PBI trong template chỉ minh họa, không cố định số lượng.

## Completion Criteria

Output hợp lệ, coverage đầy đủ hoặc ghi lý do cho phần còn thiếu. Báo số PBI, phần Proposed và phần chưa phân bổ. Workflow tiếp tục lập Round từ backlog đã kiểm.
