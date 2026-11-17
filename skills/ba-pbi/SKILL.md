---
name: ba-pbi
description: "Tạo một PBI mới để bổ sung tính năng cho dự án hiện hữu: phân tích thay đổi, cập nhật yêu cầu/backlog tối thiểu, giữ PBI cũ và điều phối business/spec/review sau khi phạm vi được duyệt. Dùng khi người dùng muốn thêm một PBI, không phải khảo sát toàn dự án hay chỉ viết spec cho PBI đã có."
---

# BA-PBI

Điểm vào cho yêu cầu “viết một PBI mới cho tính năng này”. Dùng lại các skill và contracts BA hiện có; không sửa chúng, không lập trình tính năng. Người dùng chỉ cần mô tả nhu cầu, không cần tự chọn Epic/Feature/REQ/PBI ID.

## Input Contract

Bắt buộc: mô tả tính năng/thay đổi và project đang làm việc. Optional: `project_config` (mặc định kiểm tra `./ba-project.yaml`), Epic/Feature/REQ có sẵn, Round mong muốn, tài liệu/mockup/rules và mức đầu ra mong muốn.

Đọc [conventions](../../conventions/BA-CONVENTIONS.md) và [quy trình cập nhật](references/incremental-guide.md). Xác định KIT_ROOT và project root theo conventions. Chỉ đọc nguồn/repository liên quan đến tính năng; khảo sát toàn sản phẩm thuộc ba-explore-project.

## Input Validation

Bố trí file bắt buộc: `planning_dir` phải là `.temp` hoặc thư mục con dưới `.temp` của project. Mọi hồ sơ trung gian/output của bước này (inputs, exploration, backlog, plan, draft, review, request, approvals, state, log/manifest/staging) nằm tại đó. `.specify` chỉ dành cho `Round/PBI-ID-slug/{business.md,spec.md}` do publish tạo. Nếu config/đường dẫn cũ dùng `_planning` hoặc `_planing` trong `.specify`, dừng ghi và xử lý migration theo conventions; không tự xóa hồ sơ cũ.

Load config; nếu chưa có, đề xuất [template](../../templates/ba-project.example.yaml) và xác nhận các giá trị thiết yếu trước khi tạo hồ sơ. Validate brainstorm, requirements, backlog đang có bằng helper BA, gồm expected type, project/version, refs và source hashes.

Thiếu hồ sơ nền: báo chính xác file/skill upstream. Nếu chưa có căn cứ để gắn PBI vào CAP/REQ thì đề xuất ba-explore-project cho hiện trạng hoặc bootstrap bằng ba-workflow với phạm vi tối thiểu; chỉ điều phối bootstrap khi nằm trong yêu cầu hoặc người dùng cho phép. Không tạo baseline giả, không biến “thêm một PBI” thành tái phân tích toàn dự án.

Input stale hoặc có thay đổi đồng thời: xác định ảnh hưởng trước, không đơn thuần thay hash để qua validator. Nguồn invalid → dừng đúng bước, không tiếp tục business/spec từ dữ liệu lỗi.

## Data Extraction

- Lưu nguyên văn yêu cầu vào hồ sơ request riêng, đọc nội dung các REQ/PBI liên quan và source code/docs để phân biệt đang có, còn thiếu và thay đổi mong muốn.
- Xác định actor, nhu cầu/giá trị, điểm bắt đầu/kết quả, As-Is/To-Be, scope/exclusions, quyền, dữ liệu/state, rule/flow/EC và dependency. Không suy intent nghiệp vụ chỉ từ code.
- So yêu cầu với backlog để tìm trùng lặp hoặc PBI hiện tại đã cover. Nếu trùng, chỉ ra ID và đề nghị refinement thay vì tự tạo bản sao. Thiếu thông tin có ảnh hưởng lớn thì hỏi gọn; giả định còn lại ghi Proposed/Open Question.
- Đọc ID đã dùng và history trong các hồ sơ liên quan để cấp ID mới ổn định, gồm prefix cấu hình. Không đoán ID từ tiêu đề hoặc vị trí mảng; không tái sử dụng ID đã retired.

## Processing

1. **Phân tích delta:** dùng [change checklist](references/change-checklist.md). Mặc định một lát cắt có giá trị người dùng và có thể nghiệm thu. Nếu quá lớn hoặc chứa nhiều outcome độc lập, trình phương án tách và chờ chọn; không âm thầm tạo nhiều PBI chỉ để hết scope. Không tự đặt story points.
2. **Chuẩn bị nguồn tối thiểu:** đọc SKILL.md của ba-brainstorm/ba-requirements khi CAP/REQ thực sự phải thêm hoặc đổi. Nếu nhu cầu đã được REQ mô tả đủ, dùng lại REQ, không tạo duplicate requirement. Không đổi Confirmed decisions của nội dung cũ nếu chưa có quyết định mới. Chỉ sửa phạm vi liên quan, ghi history/evidence và validate sau từng bước.
3. **Thêm backlog:** đọc ba-product-backlog/SKILL.md và [backlog schema](../../contracts/product-backlog.schema.json). Dùng Epic/Feature phù hợp hoặc đề xuất parent mới khi cần. Thêm đúng một PBI với đầy đủ user_story/value/scope/out_of_scope/requirement_refs/dependencies/priority_proposal/INVEST; Unestimated, confirmation theo evidence. Các PBI cũ giữ nguyên ID, nội dung và phân bổ trừ thay đổi liên quan được cho phép rõ ràng. Kiểm coverage và dependency graph toàn backlog.
4. **Checkpoint phạm vi:** trình PBI mới, thay đổi upstream, dependency và tác động nguồn. Dừng để người dùng duyệt backlog delta nếu chưa có quyết định còn hiệu lực cho chính phạm vi này. “Hãy tạo PBI” cho phép soạn đề xuất, không tự gán nội dung AI là đã được duyệt. Nếu người dùng chỉ yêu cầu backlog, hoàn thành tại đây và báo proposal chờ duyệt, không tự sinh spec.
5. **Round khi cần:** nếu người dùng chọn Round/đợt, đọc ba-round-plan/SKILL.md, kiểm nguồn rồi đề xuất allocation cho PBI mới; giữ phân bổ cũ. Duyệt/Proposed Allowed như pipeline hiện có. Không có Round: có thể viết business/spec draft sau duyệt scope vì business contract cho phép thiếu round_id. Nếu Round plan cũ bị stale, báo rõ; không dùng nó làm nguồn cho draft cho tới khi được revalidate. Muốn publish sau này cần Round hợp lệ.
6. **Bộ tài liệu một PBI:** khi phạm vi đã được duyệt và yêu cầu bao gồm tài liệu chi tiết, lần lượt đọc và thực hiện ba-business → ba-spec → ba-review cho đúng ID mới, validate giữa các bước. Không tái sinh tài liệu của các PBI khác. Lỗi nghiệp vụ/critical unknown đưa vào blockers; review FAIL trả findings và chỉ sửa/review lại sau thay đổi có ý nghĩa, không tự quyết policy còn mở.
7. **Dừng trước publish:** mặc định kết thúc ở draft + review. Chỉ gọi ba-publish nếu người dùng yêu cầu và đủ Round/review/approvals/freshness theo skill đó. Không ghi trực tiếp vào R{n} hoặc bypass helper publish.

Đọc skill tương ứng trong **các thư mục sibling** của ba-pbi (Kit nguồn hay bản cài đều có). Nếu runtime không gọi skill trực tiếp được, thực hiện instructions trong phiên và báo đúng cách thực hiện; không giả vờ đã chạy API/subagent. Không sửa file SKILL.md của skill khác để điều phối.

## Output Contract

Theo project config:

- `{planning_dir}/pbi-requests/{request-id}.md`: request raw, ghi nguyên văn, phân tích delta, baseline path/hash, PBI ID được đề xuất/thực tế, decisions, ảnh hưởng và next action; cấu trúc ở [request record](references/request-record.md).
- `brainstorm.md` / `requirements.md`: chỉ cập nhật khi cần, đúng schema/generator của bước chịu trách nhiệm.
- `product-backlog.md`: thêm đúng PBI mới với parents/refs hợp lệ, giữ các PBI cũ.
- `round-plan.md`: chỉ cập nhật khi đang làm phần Round được yêu cầu hoặc xử lý ảnh hưởng đã được cho phép.
- Khi đã qua checkpoint và yêu cầu gồm tài liệu: `drafts/{PBI-ID}/business.md`, `spec.md`, `reviews/{PBI-ID}-review.md`.

Request record là **raw context**, không thêm ba-pbi vào enum generated_by/document_type của contracts cũ. Canonical docs được tạo/cập nhật theo bước ba-brainstorm/ba-requirements/ba-product-backlog/ba-business/ba-spec/ba-review tương ứng, metadata giữ đúng generator của bước đó; record ghi rõ ba-pbi điều phối. Không tự đánh dấu approved.

## Output Validation

Chạy helper BA với Python có dependencies:

```text
python <KIT_ROOT>/scripts/validate_ba_document.py --project-config <config> --file <backlog-path> --expected-type product-backlog --check-refs --format json
python <KIT_ROOT>/scripts/validate_ba_document.py --project-config <config> --file <business-path> --expected-type business --pbi-id <new-id> --check-refs --format json
python <KIT_ROOT>/scripts/validate_ba_document.py --project-config <config> --file <spec-path> --expected-type spec --pbi-id <new-id> --check-refs --format json
python <KIT_ROOT>/scripts/validate_ba_document.py --project-config <config> --file <review-path> --expected-type review --pbi-id <new-id> --check-refs --format json
```

Chỉ chạy lệnh cho output thực sự đã tạo; input/upstream cũng phải validate. So baseline để chứng minh không đổi PBI ngoài scope, không mất REQ coverage, không duplicate ID, không cycle và không hứa phần chưa xác nhận. Schema PASS không thay semantic review hoặc approval. Request record không đưa vào validator BA canonical.

## Error Handling

- Trùng PBI: báo candidate IDs và lý do; chờ chọn tạo delta/refine, không tự gộp hoặc tạo bản sao.
- Yêu cầu quá lớn: đề xuất split, dừng để chọn lát cắt; không gọi nhiều PBI là “một PBI”.
- Parent/dependency không tồn tại: chỉ ra nguồn cần sửa, không tạo ref giả.
- Missing/stale/invalid baseline: báo code/path/upstream và next action. Không ghi đè nguồn có xung đột hoặc tự cập nhật toàn backlog.
- Chỉ có mã nguồn mà không có hồ sơ nền: route theo Input Validation, không claim PBI canonical đã hoàn thành.

## Traceability

Request → CAP/REQ → Epic/Feature → PBI mới → BR/Flow/EC/AC. Source_refs giữ evidence quyết định; source_documents lưu file nguồn đúng bytes, `kind: raw` cho request/context không theo BA schema. File request được hash làm nguồn thì phải chốt snapshot: cập nhật tiến độ ở record mới/sidecar, không sửa ngược nguồn đã hash mà bỏ qua stale.

Thay đổi upstream làm Round/drafts/reviews/approvals hiện hữu có thể stale ngay cả khi nội dung PBI cũ giữ nguyên; báo danh sách ảnh hưởng. Không refresh hash hàng loạt để che stale, không đổi approved thành draft âm thầm, không tự sửa các PBI đã publish. Hướng dẫn xử lý freshness chi tiết ở incremental guide.

## Example Invocation

```text
$ba-pbi
Tạo một PBI mới cho tính năng: cho phép chủ sở hữu lưu trữ ghi chú
và khôi phục lại khi cần. Đọc hiện trạng và hồ sơ BA liên quan.
Phân tích phần thay đổi, đề xuất PBI và dừng để tôi duyệt scope.
Sau khi tôi duyệt, viết business.md, spec.md và review cho PBI đó.
```

Ngắn gọn: “Dùng skill BA-PBI để thêm PBI cho tính năng [mô tả] vào dự án hiện tại.” Claude Code gọi `/ba-pbi`; Codex gọi `$ba-pbi`. Dùng ID đã tạo để tiếp tục: “Dùng BA-PBI tiếp tục request [path], tôi duyệt delta của PBI-xxx vừa trình bày; viết bộ tài liệu draft, chưa publish.”

## Completion Criteria

Với proposal: báo ID/title, file backlog/request, scope/dependencies/questions, input/output validation và checkpoint đang chờ. Với bộ draft sau duyệt: PBI mới + business/spec/review cùng ID hợp lệ; báo result, blockers và trạng thái chưa publish. Tách rõ những bước NOT RUN hoặc còn chờ. Không báo hoàn tất full draft nếu mới có backlog.

Các tình huống kiểm chứng/giới hạn: [evaluation](references/evaluation.md).
