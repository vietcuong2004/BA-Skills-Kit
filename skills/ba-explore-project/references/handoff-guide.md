# Bàn giao sang chín skill cũ mà không sửa chúng

## Vì sao không ghi thẳng brainstorm/requirements/backlog?

Ba file exploration là evidence/brief, không phải document_type mới trong contract BA. Skill mới không mạo danh generated_by của skill khác. ba-brainstorm đã nhận ý tưởng ngôn ngữ tự nhiên + optional repo/docs context, nên brief là đầu vào hợp lệ. Các bước cũ tiếp tục đúng trách nhiệm.

## Chuỗi bàn giao

1. Chạy prepare_handoff.py validate, sinh report và brief. Người dùng xem danh mục/chọn scope; đây chưa là approval backlog hay publish.
2. Dùng **ba-brainstorm** với yêu cầu “Tài liệu hóa hiện trạng trong exploration-brief.md” và đính kèm report/inventory; đọc source_refs khi cần. Mục tiêu/giá trị chưa có nguồn vẫn Proposed. Với report/docs Markdown thêm kind: raw để validator không coi chúng là BA document.
3. CLI helper trả `source_documents` chứa inventory/report/brief và toàn bộ file evidence. Đưa các entry này vào metadata brainstorm (đúng raw-byte hash, kind: raw); source_refs CAP/fact giữ EXF/EVD liên quan. Không bỏ nguồn code chỉ vì đã có hash report — raw sources không được validator cũ parse đệ quy.
4. Validate brainstorm bằng helper BA cũ với --check-refs. **ba-requirements** đọc brainstorm, **ba-product-backlog** đọc cả hai. Khi lập REQ/PBI cần đọc lại evidence liên quan và giữ refs/existing labels trong text hợp schema. Không thêm field `implementation_status`/`origin` vào schema cũ vì additionalProperties=false.
5. Đặt title/description/scope rõ “tài liệu hóa hành vi hiện có”, không ghi “chưa làm” hay suy PBI hiện hữu là development todo. PBI confirmation là quyết định phạm vi, không phải runtime verification. UI_ONLY/MOCK/PARTIAL phải giữ giới hạn trong description/open_questions, không viết AC ngụ ý phần chưa có đã hoạt động.
6. Duyệt backlog trước Round. **ba-round-plan** lập đợt tài liệu hóa, không giả là lịch sử release/Sprint hoặc cam kết effort. Chọn PBI → **ba-business** → **ba-spec** → **ba-review**, rồi gate publish như hiện tại. Critical unknowns vào blockers; bịa outcome để bỏ blocker là sai.

Nếu dùng ba-workflow để điều phối bước 2 trở đi, chỉ định rõ brief và scope hiện trạng trong lời nhắn; không cần thêm mode mới. Không tạo workflow-state Completed cho các bước chưa thực hiện. Refresh report sau khi chỉnh code phải xem ảnh hưởng và review lại, không chỉ đổi hash nguồn.

## Câu nhắn sau khi nhận báo cáo

```text
$ba-workflow
Tôi chọn tài liệu hóa các tính năng [EXF IDs/phân hệ] từ hồ sơ
{planning_dir}/exploration/exploration-brief.md.
Đọc inventory và report cùng thư mục; dùng chúng làm input cho ba-brainstorm.
Thực hiện brainstorm → requirements → product backlog mô tả hiện trạng.
Giữ mức xác minh, EXF/EVD evidence refs và câu hỏi còn mở trong tài liệu.
Đưa tất cả source_documents do helper explore cung cấp vào brainstorm dạng raw
để validator hiện tại phát hiện thay đổi ở code/docs nguồn.
Không diễn giải các PBI này thành tính năng cần xây mới. Dừng để tôi duyệt backlog.
```

`{planning_dir}` phải thay bằng path config thật, thường `.temp`. Nếu hồ sơ BA đã có, đề nghị merge có kiểm soát, giữ CAP/REQ/PBI IDs và confirmed decisions thay vì overwrite. Không tự chuyển cả project sang scope mới chỉ vì quét thêm một module.
