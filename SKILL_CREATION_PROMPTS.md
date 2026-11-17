# Bộ prompt tạo BA Skills Kit bằng Codex

> **Dành cho Codex chưa có bất kỳ context nào.** Trước khi thực hiện các prompt, đọc `README.md` cùng thư mục. Mỗi prompt là một nhiệm vụ độc lập; chỉ chuyển bước khi đã kiểm tra output bước trước. Các đường dẫn là tương đối với **thư mục gốc BA-Skills-Kit** trừ khi ghi rõ là project đích.

## Hướng dẫn sử dụng

1. Sao chép nguyên thư mục `BA-Skills-Kit/` vào workspace (hoặc dùng làm repo riêng).
2. Mở Codex ở workspace có quyền đọc thư mục này.
3. Gửi **Bootstrap Prompt** bên dưới.
4. Sau đó gửi lần lượt **Prompt 00 đến Prompt 10**. Có thể sao chép từng mục nguyên văn.
5. Mỗi bước Codex phải báo: file tạo/sửa, contract input/output, validation, test, câu hỏi chưa rõ.
6. **Chỉ tạo Skills ở giai đoạn này**, không tạo PBI cho sản phẩm thực tế; chỉ dùng fixture test độc lập.

### Bootstrap Prompt — Codex chưa có context

```text
Bạn chưa có ngữ cảnh về dự án này. Hãy đọc toàn bộ BA-Skills-Kit/README.md và BA-Skills-Kit/SKILL_CREATION_PROMPTS.md trước khi hành động.
Mục tiêu của tôi: tạo bộ 9 Codex BA Skills tái sử dụng cho nhiều project, biến mô tả ý tưởng phần mềm thành brainstorm.md → requirements.md → product-backlog.md → round-plan.md → business.md + spec.md cho từng PBI, review rồi xuất vào R{n}/{PBI-ID}-{slug}/.
Mọi Skill phải truyền dữ liệu qua Markdown có YAML metadata và khối YAML có cấu trúc; phải có schema, validator, truy vết ID và kiểm thử pipeline. Không gắn cứng MISA Note.
Trước hết hãy kiểm tra môi trường, quy chuẩn Codex Skills đang hỗ trợ và trình bày kế hoạch thực hiện Prompt 00–10. Không tạo hoặc sửa file trước khi tôi xác nhận.
```

---

## Prompt 00 — Nền tảng Contract, Config, Validator

```text
Bạn là Software Architect + Senior BA + Codex Skills Engineer. Đọc README.md trước.
NHIỆM VỤ: Xây dựng nền tảng dùng chung để các Skills giao tiếp bằng dữ liệu có cấu trúc, không dựa vào suy đoán nội dung văn xuôi.

A. Khảo sát
- Kiểm tra cấu trúc hiện có; không ghi đè không kiểm soát.
- Kiểm tra format SKILL.md và cách cài Skills của Codex trong môi trường này; không tự giả định đường dẫn discovery.
- Tạo kế hoạch file sẽ sinh; không sửa mã nguồn ứng dụng nào.

B. Project configuration
- Tạo templates/ba-project.example.yaml gồm project_id, project_name, repository_root, output_root, planning_dir, round_prefix, pbi_prefix, language, skill_runtime, approval_policy.
- Config phải được truyền hoặc tự tìm theo quy tắc minh bạch. Resolve path an toàn, chống path traversal, hỗ trợ đa project.

C. Markdown data contract
- Mọi file: YAML front matter gồm schema_version='1.0', document_type, project_id, status, source_documents (path + sha256), generated_by.
- Mỗi file có chính xác một BA-DATA block được đánh dấu <!-- BA-DATA:START --> / <!-- BA-DATA:END -->, bên trong là fenced YAML parse được.
- Dữ liệu có cấu trúc là nguồn chuẩn cho IDs, refs, states; văn xuôi trình bày cho con người, không được mâu thuẫn.
- Định nghĩa 7 JSON Schema cho brainstorm, requirements, product-backlog, round-plan, business, spec, review. JSON Schema validate YAML đã parse, không validate raw Markdown.
- Định nghĩa chi tiết các object CAP, REQ, EPIC, FEAT, PBI, Round, BR, Flow, EC, AC; có required fields, enum, pattern, unique constraints bằng kiểm tra bổ sung nếu JSON Schema không hỗ trợ.
- Cho phép một-nhiều và nhiều-nhiều; không bắt ép mọi PBI chỉ có một requirement.
- Phân biệt status tài liệu (draft/in_review/approved), trạng thái xác nhận (Confirmed/Proposed/Open Question), review (PASS/CONDITIONAL/FAIL) và human approval.

D. Conventions
- Tạo conventions/BA-CONVENTIONS.md: naming, ID stability, no renumbering, slug generation, Vietnamese content, template headings, source traceability, data status, approvals, error handling, stale source handling, Round transfer, out-of-scope safety.
- Định nghĩa source fingerprint SHA-256 của raw bytes, có logic phát hiện stale.

E. Validator thực thi
- Tạo scripts/validate_ba_document.py có CLI --project-config, --file, --check-refs, --format text|json (nếu phù hợp).
- Parse YAML an toàn, kiểm tra schema_version, document_type, required fields, headings, ID uniqueness, cross-document refs, project_id match, PBI ID match, AC Given/When/Then, EC expected behavior hoặc Open Question, source hashes.
- Phân loại ERROR/WARNING; exit code 0 chỉ khi không có ERROR.
- Lỗi có code, file, location, message, suggested_fix; không tự sửa business decisions.
- Đặt parser/validator code ở scripts/ hoặc package nội bộ; không phụ thuộc vào môi trường ngoài nếu có thể tránh. Nếu cần thư viện, ghi rõ và cung cấp setup riêng cho Kit, không sửa package.json của project đích.

F. Tests
- Tạo tests/fixtures/ cho một project giả lập có 1 CAP, 2 REQ, 1 EPIC, 1 FEAT, 2 PBI, 1 Round, 1 business/spec/review.
- Kiểm thử: valid, missing field, invalid document_type, invalid version, broken ref, duplicate ID, wrong PBI ID, missing Given/When/Then, missing EC outcome, stale source, invalid path.
- Chạy test thật và sửa lỗi kỹ thuật.

OUTPUT: templates/, conventions/, contracts/, scripts/, tests/.
KHÔNG tạo Skills, không chạy pipeline trên project thật, không commit/push.
BÁO CÁO: file đã tạo, schema mapping, câu lệnh validate, kết quả tests, quyết định còn mở.
```

## Prompt 01 — `ba-brainstorm` → `brainstorm.md`

```text
Đọc README.md, conventions/BA-CONVENTIONS.md, contracts/brainstorm.schema.json và validator trước khi tạo Skill.
Tạo skills/ba-brainstorm/SKILL.md theo format Codex đang hỗ trợ; tên kỹ thuật ba-brainstorm, description đủ rõ để trigger khi người dùng muốn phân tích ý tưởng phần mềm.

PURPOSE: Từ một đoạn ý tưởng tự nhiên tạo Product Discovery / brainstorm có cấu trúc; không tạo Requirement hoặc PBI.
INPUT: user idea (required); optional user research, current product docs, repo context. Không yêu cầu người dùng điền form dài; hỏi tối đa các câu hỏi có ảnh hưởng quyết định, còn lại ghi Proposed.
WORKFLOW:
1. Parse đầy đủ các ý người dùng nêu; lưu nguồn, không tự thêm như confirmed.
2. Xác định vision, problem hypotheses, target user groups, jobs-to-be-done, goals, business value, product scope, exclusions, constraints.
3. Tạo Capability CAP-001... với name, description, target_users, business_value, source_refs, confirmation_status.
4. Phân biệt Confirmed / Proposed / Open Question cho từng thông tin. Không bịa nghiên cứu, KPI hay tình trạng sản phẩm.
5. Kiểm tra capability coverage với từng tính năng người dùng nêu; không bỏ sót.
6. Sinh {planning_dir}/brainstorm.md theo contract: YAML front matter + BA-DATA YAML + headings: Product Overview, Vision, Target Users, Problems, Capabilities, Goals, Scope, Assumptions, Open Questions, Metrics.
7. Chạy validator, sửa lỗi schema/format, không sửa quyết định nghiệp vụ để qua test.
UPDATE MODE: so sánh với file cũ, giữ CAP IDs và decisions; tạo change log; đánh dấu downstream stale.
ERROR: nếu thiếu idea, báo rõ; nếu path/config sai, dừng; không tự gọi ba-requirements.
OUTPUT REPORT: path, số CAP, Proposed/Open Questions, validation status, source hashes.
Tạo thêm references/brainstorm-template.md và references/checklist.md nếu hữu ích. Không tạo brainstorm thật lúc cài Skill. Thêm ví dụ invocation và acceptance tests của Skill.
```

## Prompt 02 — `ba-requirements` → `requirements.md`

```text
Đọc README.md, conventions, contracts/brainstorm.schema.json, contracts/requirements.schema.json, validator.
Tạo skills/ba-requirements/SKILL.md.

INPUT CONTRACT: {planning_dir}/brainstorm.md phải tồn tại, đúng project_id, document_type=brainstorm, schema_version hỗ trợ, validator PASS. Đọc BA-DATA.capabilities, target_users, problems, scope, goals, assumptions, open_questions; không chỉ đọc heading.
PURPOSE: Chuyển Capabilities thành yêu cầu nghiệp vụ/phần mềm có thể truy vết; chưa phân rã PBI.
WORKFLOW:
1. Validate input, check freshness; nếu fail dừng và nêu skill/file cần sửa.
2. Phân tích actors, roles, preconditions, triggers, outcomes, data entities/states.
3. Với từng CAP, sinh REQ IDs ổn định; mỗi REQ có title, description, actor, trigger, preconditions, expected_outcome, capability_refs, source_refs, confirmation_status, related business_rule_refs.
4. Phân tích As-Is (chỉ khi có evidence), To-Be, Main/Alternative/Exception flows cấp feature, Business Rules BR IDs, permission/validation/data/state rules, nonfunctional considerations.
5. Phân tích edge cases theo input boundaries, duplicates, concurrency, permission changes, stale objects, cancellation, network timeout, retries, partial success, data integrity. Chỉ giữ case liên quan; chưa biết expected outcome thì Open Question.
6. Trace CAP → REQ, không có orphan REQ; ghi coverage và gaps; không biến giả định thành confirmed.
7. Output {planning_dir}/requirements.md theo contract; source_documents phải chứa path + sha256 của brainstorm.md.
8. Validate output, cross-ref check, heading check, no duplicate IDs.
UPDATE: giữ REQ IDs, phát hiện yêu cầu thêm/sửa/bỏ; downstream outputs stale nếu source hash đổi.
ERROR: thiếu CAP/contract sai → dừng; không tự chạy brainstorm; không tự viết backlog.
Tạo references/requirements-template.md và edge-case-taxonomy.md; ví dụ CAP-001 → REQ-001, REQ-002. Chỉ tạo Skill, không tạo requirements thật.
```

## Prompt 03 — `ba-product-backlog` → `product-backlog.md`

```text
Đọc README.md, conventions, contracts của brainstorm/requirements/product-backlog, validator.
Tạo skills/ba-product-backlog/SKILL.md.

INPUT CONTRACT: brainstorm.md và requirements.md đều tồn tại, cùng project_id, version tương thích, valid, không stale. Trích xuất CAP, REQ, actor, priority proposal, scope, BR refs, dependencies, confirmation status.
PURPOSE: Tạo Epic → Feature → PBI với traceability và vertical slicing.
WORKFLOW:
1. Validate cả hai input, kiểm tra REQ.capability_refs đều trỏ tới CAP tồn tại.
2. Nhóm nhu cầu thành Epic (EPIC-xxx), Feature (FEAT-xxx) dựa trên giá trị sản phẩm, không chỉ cấu trúc menu UI.
3. Phân rã mỗi Feature thành PBI có giá trị người dùng, nhỏ và có thể nghiệm thu; áp dụng INVEST. Không chia chỉ theo frontend/backend, không tự tạo Task kỹ thuật.
4. Mỗi PBI: pbi_id, epic_id, feature_id, title, user_story, business_value, scope, out_of_scope, requirement_refs, dependencies, priority_proposal, estimation_status=Unestimated, confirmation_status, open_questions.
5. Mỗi Feature có epic_id và requirement_refs; kiểm tra REQ coverage (covered/unassigned with reason). Một REQ có thể thuộc nhiều PBI.
6. Chống trùng lặp và oversized PBI; nếu thiếu thông tin, Proposed/Open Question.
7. Output {planning_dir}/product-backlog.md theo schema, source_documents hashes của cả hai inputs.
8. Validate ID uniqueness, parent references, coverage, schema, heading, source freshness.
UPDATE: preserve IDs, record added/changed/deprecated, không renumber, không tự xóa PBI đã dùng.
ERROR: invalid input → dừng; không tự lập Round, không tự đặt Story Points.
Tạo references/backlog-template.md, invest-checklist.md, vertical-slicing-examples.md và ví dụ 1 CAP → 2 REQ → 1 Epic → 1 Feature → 2 PBI.
Chỉ tạo Skill, không sinh backlog thật.
```

## Prompt 04 — `ba-round-plan` → `round-plan.md`

```text
Đọc README.md, conventions, contracts product-backlog/requirements/round-plan và validator.
Tạo skills/ba-round-plan/SKILL.md.

INPUT: {planning_dir}/product-backlog.md và requirements.md phải valid, cùng project_id, không stale; optional capacity, velocity, release goals, priorities, team constraints. Đọc PBI IDs, dependencies, priority proposals, scope, estimation status.
PURPOSE: Đề xuất Round Goals và phân bổ PBI có căn cứ; Round không mặc định là Scrum Sprint.
WORKFLOW:
1. Validate input và resolve dependency graph; phát hiện vòng lặp hoặc dependency thiếu.
2. Đề xuất mục tiêu từng Round theo các lát cắt giá trị có thể dùng được.
3. Xếp PBI theo business value, risk, dependency, readiness; ghi lý do ưu tiên.
4. Nếu thiếu capacity/estimate, chỉ tạo Proposed allocation, không cam kết khối lượng; cho phép unassigned backlog.
5. Mỗi Round: round_id, goal, status, pbi_refs, dependencies, risks, capacity_assumptions, approval_status.
6. Không tạo PBI mới, không đổi PBI ID, không đưa cùng PBI vào hai Round đang hoạt động. Khi chuyển Round, giữ ID và change history.
7. Output {planning_dir}/round-plan.md, hashes của input, heading đầy đủ, approval_status chưa approved nếu chưa có quyết định của con người.
8. Validate refs PBI, dependency order, schema, duplicate allocation, source freshness.
ERROR: thiếu input → dừng; thiếu capacity → warning/proposed, không giả vờ kế hoạch đã duyệt.
Tạo references/round-plan-template.md và dependency-checklist.md; có ví dụ 2 PBI phân Round.
Chỉ tạo Skill, không lập kế hoạch thật.
```

## Prompt 05 — `ba-business` → `business.md`

```text
Đọc README.md, conventions, contracts business/product-backlog/requirements/brainstorm, validator.
Tạo skills/ba-business/SKILL.md.

INPUT: --pbi-id bắt buộc; brainstorm.md, requirements.md, product-backlog.md valid; round-plan.md optional nhưng nếu được dùng phải validate. Đọc CHÍNH XÁC PBI có ID được chọn; resolve feature/epic, requirement_refs, related CAP/BR; không trộn nội dung PBI khác.
PURPOSE: Viết câu chuyện nghiệp vụ, mục tiêu, giá trị và giải pháp phần mềm cho một PBI, không sao chép toàn bộ spec.
WORKFLOW:
1. Validate inputs và PBI ID tồn tại duy nhất; kiểm tra PBI scope và source refs.
2. Viết business context, current problem (có evidence hay hypothesis), target users, as-is nếu có chứng cứ, to-be, goals, measurable outcomes nếu có căn cứ.
3. Viết giải pháp chi tiết: điểm vào, thành phần UI được xác nhận hoặc Proposed, thao tác, data/state, business rules, permissions, feedback, dependencies, out of scope, risks.
4. Mọi thông số không có nguồn phải là Proposed/Open Question, không tự gán Approved.
5. Tạo front matter pbi_id, epic_id, feature_id, round_id nếu có, requirement_refs, source hashes; BA-DATA theo business.schema.json.
6. Headings: Thông tin PBI, Câu chuyện nghiệp vụ, Vấn đề, Đối tượng, Mục tiêu, Giá trị, As-Is/To-Be, Giải pháp phần mềm chi tiết, Scope, Rules, Dependencies, Risks, Open Questions, Sources.
7. Output {planning_dir}/drafts/{PBI-ID}/business.md; validate output và refs.
UPDATE: merge có kiểm soát, giữ confirmed decisions, báo conflict; không tự ghi file chính thức trong R{n}.
ERROR: PBI ID không tồn tại/sai refs → dừng; không tự tạo PBI.
Tạo references/business-template.md và quality-checklist.md, ví dụ PBI tạo ghi chú. Chỉ tạo Skill.
```

## Prompt 06 — `ba-spec` → `spec.md`

```text
Đọc README.md, conventions, contracts spec/business/requirements/product-backlog, validator.
Tạo skills/ba-spec/SKILL.md.

INPUT: --pbi-id bắt buộc; {planning_dir}/drafts/{PBI-ID}/business.md, requirements.md, product-backlog.md bắt buộc và valid. Kiểm tra pbi_id trong business.md = requested PBI ID = backlog PBI ID; requirement_refs hợp lệ, cùng project_id, source không stale. Nếu business.md thiếu, dừng và đề xuất ba-business; không tự tạo thay.
PURPOSE: Tạo đặc tả đủ để Dev triển khai và QA thiết kế test, không quyết định thay PO.
WORKFLOW:
1. Resolve PBI scope, actor, User Story As a/I want/So that, preconditions, postconditions, data and states.
2. Main Flow: numbered steps, actor/system actions, inputs, results; rõ điểm bắt đầu/kết thúc.
3. Alternative Flows AF-xxx: trigger, branch point, steps, rejoin/termination, expected outcome.
4. Exception Flows EF-xxx: error trigger, system behavior, data state, feedback, recovery/retry.
5. BR-xxx/validation/permission/state rules với source + confirmation_status.
6. Edge Cases EC-xxx: boundary min/max, empty/null/whitespace, special characters, duplicate, rapid click, cancel, permission changes, concurrency, deleted parent/stale state, timeout after server success, retries, partial save, integrity. Chỉ tạo case có liên quan. Mỗi EC có scenario, preconditions, expected_behavior hoặc explicit Open Question, related_br_refs, related_ac_refs.
7. AC-xxx: title, Given, When, Then, requirement_refs, related flow/EC refs; cover main success, important alternatives, errors, high-risk edge cases. Không viết AC mơ hồ, không coi AC là test case chi tiết.
8. Traceability matrix REQ ↔ BR/Flow/EC ↔ AC; no dangling refs; kiểm tra scope, no contradictory behavior, không tự đặt API/database design.
9. Output {planning_dir}/drafts/{PBI-ID}/spec.md với front matter + BA-DATA theo spec.schema.json, headings đầy đủ, hashes của business/backlog/requirements.
10. Validate output, IDs, GWT fields, edge outcomes, cross-file consistency, freshness.
UPDATE: preserve AC/EC IDs, đánh dấu downstream review stale, không sửa business.md khi chưa được yêu cầu.
ERROR: thiếu business, wrong PBI ID, unconfirmed critical behavior → dừng hoặc draft có blockers rõ, tuyệt đối không tự phê duyệt.
Tạo references/spec-template.md, flow-guide.md, edge-case-checklist.md, ac-gwt-guide.md và ví dụ đầy đủ PBI tạo thư mục.
Chỉ tạo Skill, không sinh spec thật.
```

## Prompt 07 — `ba-review` → `review.md`

```text
Đọc README.md, conventions, contracts review/spec/business, validator.
Tạo skills/ba-review/SKILL.md.

INPUT: --pbi-id; draft business.md, spec.md, requirements.md, product-backlog.md; optional round-plan.md. Validate all, cùng project_id và PBI ID, source hashes.
PURPOSE: Review độc lập tài liệu PBI; không tự sửa business/spec hoặc duyệt thay PO.
WORKFLOW:
1. Validate cấu trúc, heading, required fields, refs, ID, version, freshness.
2. So sánh mục tiêu ↔ User Story ↔ scope ↔ flows ↔ rules ↔ EC ↔ AC ↔ source requirements.
3. Kiểm tra main/alternative/exception coverage; tự tìm missing edge cases có liên quan (permission, concurrent, timeout, retry, data integrity...).
4. Đánh giá Given/When/Then cụ thể, kiểm chứng được, không mâu thuẫn, không duplicate; kiểm tra traceability coverage.
5. Mỗi finding: finding_id, severity Critical/Major/Minor, file, section, evidence, impact, recommendation, status.
6. Kết quả PASS nếu không có Critical/Major và không có blocker nghiệp vụ; CONDITIONAL nếu có điểm cần refinement; FAIL nếu lỗi trọng yếu. Review PASS KHÔNG đồng nghĩa human approval.
7. Output {planning_dir}/reviews/{PBI-ID}-review.md theo schema; chứa source hashes của business/spec.
8. Validate review output. Nếu source thay đổi sau review, review stale và publish phải chặn.
UPDATE: so sánh findings cũ, giữ history, không âm thầm xóa finding.
ERROR: input invalid → ghi diagnostic, không tự tạo review PASS.
Tạo references/review-template.md và severity-rubric.md, tests cho mismatch PBI ID, missing AC, stale source.
Chỉ tạo Skill.
```

## Prompt 08 — `ba-publish` → Round/PBI directories

```text
Đọc README.md, conventions, contracts và validator. Tạo skills/ba-publish/SKILL.md.

INPUT: project config, round-plan.md, product-backlog.md, selected PBI IDs, draft business/spec, review; explicit human approval for publishing. Phải validate tất cả inputs, source hashes và đúng Round allocation.
PURPOSE: Chỉ xuất tài liệu hợp lệ vào {output_root}/{round_id}/{PBI-ID}-{slug}/ với chính xác business.md và spec.md.
WORKFLOW:
1. Validate project config, resolve safe paths, round IDs, PBI IDs, review source freshness, approval state.
2. Kiểm tra review PASS; CONDITIONAL chỉ cho phép draft publication nếu có xác nhận rõ, không gắn approved; FAIL phải chặn publish.
3. Tạo dry-run manifest: paths, create/update/skip/conflict, expected hashes; trình bày trước khi ghi đè/move/delete.
4. Khi được phép, tạo Round folder và PBI folder; chỉ xuất business.md + spec.md, không để review.md trong thư mục PBI.
5. Giữ IDs và metadata, đảm bảo links và source refs. Kiểm tra file sau ghi, hashes và cross-refs.
6. Nếu PBI chuyển Round, không tạo duplicate không kiểm soát; yêu cầu quyết định giữ lịch sử/di chuyển/link và không tự xóa đường dẫn cũ.
7. Idempotent: chạy lại cùng input không tạo bản sao hoặc thay đổi không cần thiết; xử lý conflict không phá dữ liệu.
8. In publish report stdout (không thêm file thứ ba vào PBI): created, updated, skipped, blocked, conflicts.
SAFETY: không sửa app source, manifest, lockfile, IDE; không git add ., commit, push; không gọi API ngoài; không tự approve.
Tạo references/publish-checklist.md và dry-run-example.md. Thêm tests publish PASS/FAIL, stale review, duplicate ID, path traversal, idempotence.
Chỉ tạo Skill, không publish project thật.
```

## Prompt 09 — `ba-workflow` → orchestrator/state

```text
Đọc README.md, conventions, contracts, validator và SKILL.md của tám Skills. Tạo skills/ba-workflow/SKILL.md.

PURPOSE: Điều phối pipeline end-to-end, không thay thế trách nhiệm của từng Skill.
INPUT: user idea hoặc workflow state của project + config; modes INTERACTIVE, DRAFT, RESUME, SINGLE-PBI, SINGLE-ROUND.
WORKFLOW:
1. Load config, detect existing files/state, validate; xác định bước tiếp theo, không chạy lại không cần thiết.
2. Run ba-brainstorm → validate; ba-requirements → validate; ba-product-backlog → validate.
3. Human checkpoint: xác nhận backlog, scope, unresolved decisions có tác động lớn.
4. Run ba-round-plan → validate; human checkpoint: xác nhận hoặc cho phép proposed allocation.
5. Với mỗi selected PBI: ba-business → validate; ba-spec → validate; ba-review → validate. Nếu FAIL, báo findings, không tự sửa business decisions, chỉ retry khi có thay đổi hợp lệ.
6. Human checkpoint trước publish, bảo đảm approval và review freshness.
7. ba-publish dry-run → approval → publish → post-validate.
8. Lưu {planning_dir}/workflow-state.md với current_phase, completed, pending, blockers, input/output paths, hashes, approvals, last_updated; định nghĩa schema/format riêng nếu cần.
9. Nếu runtime không thể gọi Skill khác trực tiếp, đọc SKILL.md và thực hiện theo hợp đồng, ghi rõ thực tế đã thực hiện; không giả vờ invocation thành công.
10. On resume, so sánh source hashes, invalidate downstream outputs bị ảnh hưởng, bảo toàn confirmed decisions và IDs.
ERROR: nếu input invalid, dừng tại đúng bước; nêu file, error code, next action. Không chạy publish nếu review FAIL hoặc thiếu approval.
SECURITY: không tự commit/push, không sửa mã nguồn, không tự chạy external APIs.
Tạo references/workflow-map.md, checkpoint-policy.md, recovery-guide.md; ví dụ invocation cho dự án mới, resume, one PBI, one Round.
Chỉ tạo Skill và tests điều phối với fixture, không chạy trên project thật.
```

## Prompt 10 — Kiểm thử tích hợp, đóng gói, hướng dẫn cài đặt

```text
Đọc README.md, conventions và toàn bộ 9 SKILL.md. Kiểm tra từng Skill thực sự có Input Contract, Input Validation, Data Extraction, Processing, Output Contract, Output Validation, Error Handling, Traceability, Example Invocation, Completion Criteria.

NHIỆM VỤ:
1. Chạy pipeline thật trên fixture project giả lập "Example Notes" với idea: ghi chú cá nhân, ghi chú công ty, tạo tài liệu từ mẫu, tìm kiếm. Không chạy trên repository sản phẩm thật.
2. Dùng output FILE THẬT của Skill trước làm input của Skill sau, không tự viết tay dữ liệu thay thế giữa bước.
3. Ghi input/output path, schema version, SHA-256, validation result cho từng bước.
4. Test CAP → REQ → EPIC/FEAT → PBI → Round → business/spec → AC → review → publish.
5. Negative tests: missing file, wrong document_type, wrong schema version, missing field, duplicate ID, broken reference, wrong PBI ID, missing Given/When/Then, Edge Case thiếu expected behavior và open question, stale input, review FAIL, missing human approval, path traversal, publish conflict.
6. Test RESUME và idempotent rerun; sửa một REQ rồi kiểm tra downstream bị đánh dấu stale.
7. Kiểm tra mỗi thư mục PBI cuối cùng chỉ có business.md và spec.md.
8. Đóng gói BA-Skills-Kit độc lập: README, prompts, templates, contracts, scripts, tests, skills; tạo INSTALL.md với cách cài trên Codex runtime đã xác minh, hướng dẫn copy sang project mới, cấu hình ba-project.yaml, cập nhật Skills.
9. Tạo báo cáo tests/INTEGRATION_REPORT.md gồm matrix: Skill | Input | Output | Schema | Validator | Test Result | Evidence.
10. Nếu test không thể thực thi do thiếu runtime, nêu rõ NOT RUN, không đánh dấu PASS; tách unit tests và agent-driven integration tests.

BẢO VỆ: Không tự commit/push, không sửa mã nguồn sản phẩm, không xóa dữ liệu project thật. Chỉ kết luận READY khi các điều kiện hoàn thành được kiểm chứng.
```

---

## Mẫu lệnh dùng bộ Skills sau khi cài

```text
$ba-workflow mode=INTERACTIVE project_config=./ba-project.yaml
Tôi muốn làm website ghi chú cá nhân và doanh nghiệp, hỗ trợ tạo tài liệu từ mẫu, tổ chức thư mục, tìm kiếm và chia sẻ. Hãy bắt đầu từ brainstorm, dừng ở checkpoint để tôi duyệt backlog và Round.
```

```text
$ba-spec pbi_id=PBI-001 project_config=./ba-project.yaml
Đọc business.md, requirements.md và product-backlog.md đúng contract. Phân tích Main/Alternative/Exception Flows, Edge Cases và Given-When-Then AC. Validate trước khi báo hoàn thành.
```

> Cú pháp gọi Skill có thể khác nhau tùy phiên bản Codex. Sau khi cài, kiểm tra cơ chế discovery thực tế; các dòng trên là ví dụ lệnh mong muốn, không phải bảo đảm runtime đã hỗ trợ.

## Tiêu chí nghiệm thu cuối cùng

- [ ] Tất cả 9 Skills có SKILL.md hợp lệ, được runtime nhận diện.
- [ ] Có project config tái sử dụng và không hardcode tên project.
- [ ] Có schemas + validator chạy được.
- [ ] Tất cả Skills đọc input từ đúng path và kiểm tra schema.
- [ ] Tất cả Skills tạo output theo schema và validate trước khi báo hoàn thành.
- [ ] CAP/REQ/EPIC/FEAT/PBI/BR/EC/AC refs được truy vết.
- [ ] Có stale detection bằng content hash.
- [ ] Có checkpoints phê duyệt và publish gating.
- [ ] Có negative tests và integration report với evidence.
- [ ] Cấu trúc Round/PBI cuối cùng có đúng hai file `business.md`, `spec.md`.
- [ ] Có INSTALL.md hướng dẫn triển khai Kit sang project mới.
