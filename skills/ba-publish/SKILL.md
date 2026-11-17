---
name: ba-publish
description: Kiểm tra và xuất đúng cặp business.md/spec.md của PBI vào Round sau review và phê duyệt con người. Có dry-run, kiểm hash, idempotence và chặn xung đột; không tự duyệt hoặc ghi đè.
---

# BA-publish

## Input Contract

Config, selected PBI IDs rõ ràng, backlog, Round plan, draft business/spec, review, quyết định publish thực tế của người dùng. Đọc [conventions](../../conventions/BA-CONVENTIONS.md), [checklist](references/publish-checklist.md), [approval schema](../../contracts/approvals.schema.json). Resolve KIT_ROOT/project paths theo conventions.

## Input Validation

Cấu hình mới ở `.temp/ba-project.yaml`; `repository_root: .` vẫn là root project. Tìm/đọc bằng `Project.load` theo conventions, tương thích config cũ ở root.

Bố trí file bắt buộc: `planning_dir` phải là `.temp` hoặc thư mục con dưới `.temp` của project. Mọi hồ sơ trung gian/output của bước này (inputs, exploration, backlog, plan, draft, review, request, approvals, state, log/manifest/staging) nằm tại đó. `.specify` chỉ dành cho `Round/PBI-ID-slug/{business.md,spec.md}` do publish tạo. Nếu config/đường dẫn cũ dùng `_planning` hoặc `_planing` trong `.specify`, dừng ghi và xử lý migration theo conventions; không tự xóa hồ sơ cũ.

Dùng `scripts/publish_ba.py` để kiểm tất cả inputs/recursive source hashes/đúng project-PBI-Round. Review FAIL hoặc business/spec blockers → chặn. CONDITIONAL chỉ cho draft khi có quyết định Draft Publication. Kiểm backlog checkpoint và Round Approved/Proposed Allowed gắn đúng bytes; không suy approval từ PASS hoặc front matter approved.

## Data Extraction

Lấy PBI title/ID đúng backlog, Round duy nhất từ allocation, draft/review hashes và human record. Target = output_root/round_id/PBI-ID-slug. Slug theo helper, không lấy path từ nội dung user tự do. Bằng chứng approval phải từ quyết định thật, không sao chép fixture.

## Processing

1. Chạy dry-run: `python <KIT_ROOT>/scripts/publish_ba.py --project-config <config> --pbi-id <id>` (optional `--approvals <path>`). Trình manifest paths/action/hash và blockers; xem [ví dụ](references/dry-run-example.md).
2. Hoàn thành toàn bộ kiểm tra trước khi hỏi quyền còn thiếu. Nếu đã có authorization đúng selected IDs và bytes trong phiên, ghi audit record, không hỏi lại. Nếu thiếu, xin quyết định checkpoint, giải thích theo quy ước Kit; không tự approve.
3. Ghi `{planning_dir}/approvals.json` đúng schema sau quyết định thật. Publish record bao phủ backlog, Round, business, spec và review hiện tại. Quyết định critical chưa chốt phải được xử lý trong nguồn và review lại; ghi tên quyết định ở resolved_decisions.
4. Chạy lại dry-run để đảm bảo approvals/hash current rồi `--apply`. Helper stage cặp file, kiểm hash trước/sau và refs. Không tự copy thủ công để bỏ qua gate.
5. Với nhiều PBI, xử lý từng cặp theo dependency order, báo partial completion trung thực. Đây không phải transaction toàn Round. Không chạy nhiều publisher đồng thời cùng PBI.

## Output Contract

`{output_root}/{round_id}/{pbi_id}-{slug}/business.md` và `spec.md`, chính xác hai file. Giữ nguyên IDs/metadata/bytes; refs được resolve từ root, không phụ thuộc vị trí file mới. Không nhét review/report/history vào thư mục PBI. Report stdout gồm created/updated/skipped/blocked/conflicts.

## Output Validation

Helper post-validates với refs và so SHA-256; xác nhận chỉ hai file. Cùng inputs chạy lại → skip, không đổi mtime. Không đánh dấu approved nếu đang draft publication; phê duyệt status thay đổi bytes đòi review mới.

## Error Handling

Conflict hoặc file thứ ba → dừng, giữ dữ liệu cũ. Helper không hỗ trợ tự overwrite/update, dù manifest có thể báo conflict; cần so bản cũ/mới và quyết định lưu lịch sử trước. PBI đã ở Round/path khác → ROUND_TRANSFER_CONFLICT; giữ ID, hỏi phương án migration/history/link, không tự xóa hoặc tạo duplicate. Lỗi sau ghi → báo path và trạng thái thực tế, không tự xóa để che lỗi.

## Traceability

Review phải hash đúng hai drafts; approval gắn bytes hiện tại. Recompute input hash ngay trước ghi. Approval record không phải cơ chế chứng thực danh tính; agent chịu trách nhiệm đối chiếu quyết định người dùng.

## Example Invocation

`$ba-publish pbi_id=PBI-001 project_config=./.temp/ba-project.yaml` — “Kiểm tra và cho tôi xem dry-run trước publish.”

## Completion Criteria

Chỉ báo published khi helper apply và post-validation thành công. Báo created/skipped/blocked/conflicts, target và hash; không claim publish nếu chỉ dry-run. Acceptance: FAIL/stale/missing approval/path escape → chặn; rerun → skip; user edits → preserve conflict.
