# BA Skills Kit — Mở dự án trong Codex rồi yêu cầu phân tích thế nào?

**README này là bộ câu nhắn để bạn copy vào ô chat Codex khi đang mở một dự án.** Bạn mô tả nhu cầu bằng tiếng Việt và nói rõ muốn dùng skill nào; Codex sẽ tạo các file phân tích trong dự án.

Cài đặt cho Claude Code, Codex và Antigravity xem tại **[INSTALL.md](INSTALL.md)**. Các ví dụ dưới đây dành cho Codex, giả sử bộ skill đã được cài. Nếu chưa có `ba-project.yaml`, câu nhắn đầu tiên sẽ yêu cầu Codex hỗ trợ chuẩn bị cấu hình trước.

### Agent bắt đầu đọc từ đâu?

Kit có [AGENTS.md](AGENTS.md) làm hướng dẫn chung và [SKILL.md](SKILL.md) chỉ đường tới chín skill. [CLAUDE.md](CLAUDE.md) import hướng dẫn chung cho Claude Code. Khi mở Kit làm workspace, agent dùng hướng dẫn workspace phù hợp; nếu Kit chỉ nằm trong thư mục con hoặc ở nơi khác, hãy chỉ rõ đường dẫn để agent đọc.

Sau khi cài, mỗi skill có SKILL.md riêng trong thư mục discovery của runtime. Không cần chép đè AGENTS.md/CLAUDE.md của Kit vào project sản phẩm. Nếu chưa cài nhưng muốn agent đọc Kit trực tiếp, gửi:

```text
Đọc D:/BA-Skills-Kit/AGENTS.md và D:/BA-Skills-Kit/SKILL.md.
Dùng hướng dẫn ba-workflow trong Kit để phân tích dự án hiện tại.
Nhu cầu của tôi: [mô tả]. Dùng ./ba-project.yaml nếu đã có;
nếu chưa có thì đề xuất cấu hình để tôi xác nhận trước khi tạo hồ sơ BA.
Đi đến backlog và dừng để tôi duyệt phạm vi.
```

Thay đường dẫn bằng nơi giữ Kit trên máy bạn. Đọc file trực tiếp không đồng nghĩa skill đã được cài hoặc xuất hiện trong selector.

## 1. Chưa biết bắt đầu từ đâu? Copy câu này

Mở Codex tại thư mục dự án cần phân tích, thay phần trong ngoặc vuông rồi gửi:

```text
Dùng skill ba-workflow để phân tích nghiệp vụ cho dự án hiện tại.

Tôi muốn: [mô tả sản phẩm hoặc tính năng bạn cần].

Hãy đọc README và các tài liệu liên quan trong dự án để hiểu bối cảnh.
Nếu đã có mã nguồn, khảo sát phần liên quan để phân biệt tính năng hiện có
với nhu cầu mới; dẫn nguồn cho những gì đã xác minh.

Kiểm tra ba-project.yaml. Nếu chưa có, đề xuất cấu hình từ template của Kit
và hỏi tôi xác nhận tên dự án, thư mục gốc và nơi lưu tài liệu trước khi tạo hồ sơ BA.

Sau đó thực hiện brainstorm → requirements → product backlog.
Ghi tài liệu vào planning_dir theo cấu hình, kiểm tra output từng bước
và dừng để tôi duyệt backlog trước khi lập kế hoạch Round.
```

**Bạn nhận được gì?** Với cấu hình mặc định, Codex tạo `brainstorm.md`, `requirements.md`, `product-backlog.md` và lưu tiến độ trong `workflow-state.md`, dưới `.specify/_planning/`.

Bạn không cần tự gọi từng skill khi dùng `ba-workflow` cho chuỗi công việc này. Nếu có câu hỏi ảnh hưởng phạm vi hoặc hành vi quan trọng, Codex sẽ hỏi; phần chưa xác nhận phải được ghi là đề xuất hoặc câu hỏi mở.

Bạn cũng có thể mở đầu bằng `$ba-workflow` thay cho câu “Dùng skill ba-workflow”. Ví dụ rút gọn:

```text
$ba-workflow
Phân tích nghiệp vụ dự án hiện tại cho nhu cầu: [mô tả nhu cầu].
Dùng ba-project.yaml ở root dự án. Làm từ brainstorm đến backlog,
kiểm tra các file đầu ra và dừng để tôi duyệt phạm vi.
```

Các đoạn này gửi vào **chat Codex**, không chạy trong PowerShell. Tên kỹ thuật của skill viết thường, có dấu gạch nối: `ba-workflow`, `ba-spec`…

## 2. Ví dụ điền nhu cầu cho dự án của bạn

### Dự án mới, chưa có mã nguồn

```text
Dùng skill ba-workflow để phân tích ý tưởng sản phẩm mới.

Tôi muốn website ghi chú cho cá nhân và công ty. Người dùng có thể tạo ghi chú,
soạn tài liệu từ mẫu, tìm kiếm và chia sẻ trong phạm vi được cho phép.

Dùng ba-project.yaml của dự án; nếu chưa có thì đề xuất cấu hình để tôi xác nhận.
Làm rõ người dùng, vấn đề, phạm vi và các câu hỏi cần quyết định.
Tạo brainstorm, requirements và backlog; dừng để tôi duyệt backlog.
```

### Dự án đang có sẵn, muốn bổ sung tính năng

```text
Dùng skill ba-workflow để phân tích nhu cầu bổ sung chức năng chia sẻ ghi chú
trong dự án hiện tại.

Hãy đọc tài liệu và mã nguồn liên quan đến ghi chú, tài khoản và phân quyền.
Chỉ ghi nhận tính năng đang có khi có bằng chứng từ repository;
phần chưa xác minh phải nêu rõ.

Đối chiếu với hồ sơ BA hiện có. Nếu cần cập nhật, giữ ID và quyết định đã xác nhận,
chỉ ra phạm vi bị ảnh hưởng và đề xuất thay đổi trước khi sửa phần có xung đột.
Nếu chưa có hồ sơ BA, bắt đầu từ brainstorm.

Dùng ba-project.yaml. Đi đến backlog và dừng để tôi duyệt phạm vi mới.
```

Khảo sát repository giúp hiểu hiện trạng; các bước này tạo **tài liệu BA**. Việc lập trình tính năng là công việc tiếp theo.

## 3. Sau câu đầu tiên, tiếp tục nói gì?

Làm theo thứ tự dưới đây. **PBI** là một phần việc có thể mô tả và nghiệm thu; **Round** là một đợt thực hiện các PBI đã chọn. Thay `PBI-001`, `PBI-002`, `R1` bằng ID thật Codex đã tạo cho dự án của bạn.

### Bước 1 — Đọc backlog, yêu cầu sửa hoặc duyệt

Mở `.specify/_planning/product-backlog.md`. Xem có đúng nhu cầu, thiếu phần việc hoặc chia quá lớn không.

Nếu cần sửa:

```text
Dùng skill ba-product-backlog để điều chỉnh backlog hiện tại:
[ghi rõ các phần cần thêm, tách, gộp hoặc làm rõ].

Giữ các ID và quyết định đã xác nhận, chỉ ra ảnh hưởng tới tài liệu liên quan.
Nếu thay đổi vượt requirements hiện tại, báo nguồn cần cập nhật trước.
Cho tôi xem lại backlog sau khi kiểm tra.
```

Khi đồng ý và muốn đi tiếp:

```text
Tôi duyệt phạm vi và backlog hiện tại.
Dùng skill ba-workflow để tiếp tục bước ba-round-plan.
Đề xuất mục tiêu từng Round và các PBI tương ứng, giải thích thứ tự ưu tiên.
Nếu chưa có capacity hoặc ước lượng, giữ kế hoạch là Proposed,
chưa cam kết khối lượng. Dừng để tôi xem và duyệt kế hoạch.
```

**Output:** `.specify/_planning/round-plan.md`.

### Bước 2 — Cho phép dùng kế hoạch và chọn PBI để viết tài liệu

Sau khi đọc Round plan:

```text
Tôi cho phép dùng kế hoạch Round hiện tại ở dạng Proposed, chưa cam kết khối lượng.
Dùng skill ba-workflow để tạo bộ tài liệu cho PBI-001 và PBI-002 trong R1.

Với mỗi PBI, thực hiện ba-business → ba-spec → ba-review.
Viết rõ nghiệp vụ, giải pháp, luồng chính/nhánh khác/lỗi, quyền, dữ liệu,
tình huống đặc biệt và điều kiện nghiệm thu Given–When–Then.

Nếu review có lỗi quan trọng, báo findings và đề xuất cách sửa;
không tự quyết các vấn đề nghiệp vụ còn mở.
Dừng sau review, trước khi xuất tài liệu sang thư mục Round.
```

Nếu bạn đã có cơ sở và thực sự duyệt kế hoạch, thay câu đầu bằng “Tôi duyệt kế hoạch Round hiện tại.”

**Output cho từng PBI được chọn:**

```text
.specify/_planning/drafts/PBI-001/business.md
.specify/_planning/drafts/PBI-001/spec.md
.specify/_planning/reviews/PBI-001-review.md
```

### Bước 3 — Xem review và làm rõ điểm cần sửa

“Finding” là vấn đề được phát hiện khi review; “blocker” là vấn đề bắt buộc giải quyết trước khi đi tiếp.

| Kết quả review | Bạn làm gì tiếp? |
| --- | --- |
| `PASS` | Đọc tài liệu rồi yêu cầu xem trước đường dẫn xuất |
| `CONDITIONAL` | Xem các điểm còn mở; có thể cho phép xuất draft rõ ràng nếu phù hợp |
| `FAIL` | Giải quyết lỗi quan trọng hoặc quyết định còn thiếu, rồi review lại |

Ví dụ yêu cầu sửa và review lại:

```text
Dùng skill ba-workflow để xử lý các findings của PBI-001.

Quyết định của tôi cho những điểm cần làm rõ là:
[ghi quyết định tương ứng từng finding hoặc câu hỏi].

Cập nhật business/spec trong phạm vi cần thiết, giữ ID và ghi lịch sử thay đổi.
Dùng ba-review để review lại sau khi kiểm tra các file đã sửa.
Dừng trước publish và báo các finding còn mở.
```

### Bước 4 — Xem trước rồi cho phép xuất tài liệu

Yêu cầu xem trước:

```text
Dùng skill ba-publish để kiểm tra PBI-001 trong Round R1 và tạo dry-run.
Cho tôi xem đường dẫn, file sẽ tạo hoặc bỏ qua, các xung đột và điều kiện còn thiếu.
Chưa ghi cặp tài liệu sang thư mục Round ở bước này.
```

Sau khi đọc dry-run, nếu review PASS và bạn đồng ý:

```text
Tôi cho phép publish cặp tài liệu hiện tại của PBI-001 vào R1
đúng theo dry-run vừa trình bày.
Dùng skill ba-publish để xuất file và kiểm tra kết quả sau khi ghi.
```

**Output mặc định:**

```text
.specify/R1/PBI-001-ten-ngan/business.md
.specify/R1/PBI-001-ten-ngan/spec.md
```

`ten-ngan` được tạo từ tiêu đề PBI. Mỗi thư mục PBI xuất ra chứa **chính xác hai file** trên. Publish là xuất file bàn giao trong dự án, không phải triển khai sản phẩm lên Internet.

## 4. Nếu chỉ muốn chạy riêng một bước

Các câu dưới đây dùng khi bạn đã có đầu vào cần thiết. Skill đơn lẻ sẽ báo file thiếu hoặc nguồn không hợp lệ; dùng `ba-workflow` khi muốn điều phối nhiều bước liên tiếp.

| Bạn muốn | Copy câu này vào Codex | Đầu vào cần có |
| --- | --- | --- |
| Làm rõ ý tưởng | Dùng skill ba-brainstorm để phân tích ý tưởng: [mô tả]. Làm rõ người dùng, vấn đề, mục tiêu, phạm vi và câu hỏi mở. | Ý tưởng và cấu hình dự án |
| Phân tích yêu cầu | Dùng skill ba-requirements để chuyển brainstorm hiện tại thành yêu cầu, quy tắc nghiệp vụ, quyền, flows và edge cases có truy vết. | `brainstorm.md` |
| Chia phần việc | Dùng skill ba-product-backlog để phân rã yêu cầu hiện tại thành Epic, Feature và PBI có giá trị người dùng; nêu coverage và dependencies. | Brainstorm và requirements |
| Lập kế hoạch đợt | Dùng skill ba-round-plan để đề xuất các Round từ backlog hiện tại. Nêu mục tiêu, phụ thuộc và capacity còn thiếu. | Backlog và requirements |
| Viết nghiệp vụ | Dùng skill ba-business để viết business.md cho PBI-001, đúng phạm vi đã có trong backlog. | PBI ID, brainstorm, requirements, backlog; Round nếu dùng |
| Viết đặc tả | Dùng skill ba-spec để viết spec.md cho PBI-001 từ business draft, bao gồm flows, rules, edge cases và AC Given–When–Then. | Business đúng PBI, requirements và backlog |
| Kiểm tra tài liệu | Dùng skill ba-review để review business/spec của PBI-001; báo findings có bằng chứng và readiness. | Cặp draft đúng PBI, requirements, backlog và nguồn liên quan |
| Chuẩn bị xuất file | Dùng skill ba-publish để tạo dry-run cho PBI-001, kiểm review, phê duyệt và Round trước khi ghi. | Round, backlog, cặp draft, review; phê duyệt thật để thực hiện ghi |
| Điều phối nhiều bước | Dùng skill ba-workflow để thực hiện [các bước mong muốn] cho [phạm vi/PBI/Round], dừng tại checkpoint cần tôi duyệt. | Ý tưởng hoặc hồ sơ/state hiện tại và cấu hình |

Bạn có thể thêm “Dùng cấu hình `./ba-project.yaml`” vào bất kỳ câu nào khi cần chỉ rõ file cấu hình.

## 5. Làm gì khi agent dừng để hỏi bạn?

Hãy đọc câu hỏi và tài liệu tương ứng rồi trả lời bằng quyết định cụ thể. Ba điểm chính cần bạn xác nhận là **backlog/phạm vi → kế hoạch Round → cho phép publish**. Những câu duyệt ở mục 3 chỉ dùng khi bạn thực sự đồng ý với phiên bản tài liệu đang xem.

Các trạng thái giúp bạn phân biệt thông tin:

- **Confirmed**: có căn cứ xác nhận; **Proposed**: đề xuất; **Open Question**: chưa quyết định.
- **draft / in_review / approved**: trạng thái toàn tài liệu — nháp / đang xem xét / đã duyệt.
- **Review PASS**: kết quả kiểm tra; không tự thay quyết định phê duyệt của bạn.

Nếu review CONDITIONAL và bạn chỉ muốn bàn giao bản nháp, sau khi xem dry-run có thể nói:

```text
Tôi cho phép Draft Publication cho cặp tài liệu hiện tại của PBI-001
đúng dry-run vừa xem. Giữ trạng thái draft và các finding còn mở.
Dùng skill ba-publish để thực hiện và kiểm tra lại kết quả.
```

Review FAIL hoặc blocker nghiệp vụ còn mở phải được xử lý trước. Các quyết định đã có và còn đúng phạm vi/phiên bản có thể được tái sử dụng; khi nguồn thay đổi, Codex sẽ kiểm tra lại ảnh hưởng.

## 6. Hôm sau mở lại dự án, nói gì?

```text
Dùng skill ba-workflow ở mode RESUME để tiếp tục phân tích dự án hiện tại.
Đọc ba-project.yaml và workflow-state.md, kiểm tra các file cùng nguồn đầu vào.
Cho biết bước nào đã xong, bước nào cần cập nhật và quyết định nào còn chờ tôi.
Tiếp tục phần đang chờ nếu đã đủ đầu vào và phê duyệt phù hợp.
```

Muốn chỉ làm một PBI hoặc một Round:

```text
Dùng skill ba-workflow ở mode SINGLE-PBI để làm bộ tài liệu draft cho PBI-001.
Dùng hồ sơ hiện có của dự án; kiểm tra đầu vào và dừng trước publish.
```

```text
Dùng skill ba-workflow ở mode SINGLE-ROUND để review các PBI đã phân vào R1.
Giữ nguyên phân bổ Round và báo kết quả từng PBI.
```

## 7. Nếu muốn thay đổi yêu cầu đã phân tích

```text
Dùng skill ba-workflow để cập nhật phân tích cho thay đổi sau:
[mô tả thay đổi và các quyết định mới của tôi].

Đọc hồ sơ hiện tại trước khi sửa. Giữ ID và các quyết định còn hiệu lực,
chỉ ra requirements/PBI/business/spec/review bị ảnh hưởng.
Cập nhật các tài liệu trong phạm vi thay đổi, kiểm tra lại nguồn,
và dừng để tôi duyệt các thay đổi về scope, Round hoặc publish.
```

Nếu gặp `STALE_INPUT`, có nghĩa là tài liệu nguồn đã thay đổi. Bạn có thể nói:

```text
Dùng skill ba-workflow ở mode RESUME để xử lý STALE_INPUT.
Chỉ ra nguồn nào đổi và tài liệu nào bị ảnh hưởng.
Đề xuất cập nhật cần thiết, giữ ID và quyết định đã xác nhận;
kiểm tra/review lại sau khi sửa, không chỉ thay hash để bỏ cảnh báo.
```

## 8. Tôi đọc file nào sau khi chạy?

Các đường dẫn dưới đây theo cấu hình mặc định; nếu đổi `planning_dir` hoặc `output_root`, dùng đường dẫn trong `ba-project.yaml`.

| File | Nội dung để bạn đọc |
| --- | --- |
| `.specify/_planning/brainstorm.md` | Hiểu sản phẩm, người dùng, vấn đề, phạm vi và khả năng cần có |
| `.specify/_planning/requirements.md` | Các yêu cầu, quy tắc nghiệp vụ, quyền và hành vi cần làm rõ |
| `.specify/_planning/product-backlog.md` | Epic/Feature/PBI, phạm vi từng phần việc, ưu tiên và phụ thuộc |
| `.specify/_planning/round-plan.md` | Mục tiêu từng đợt và PBI được chọn hoặc chưa phân bổ |
| `.specify/_planning/drafts/PBI-001/business.md` | Vì sao cần PBI, giá trị, quy trình và giải pháp nghiệp vụ |
| `.specify/_planning/drafts/PBI-001/spec.md` | Phần mềm phải hoạt động thế nào để Dev triển khai, QA kiểm thử |
| `.specify/_planning/reviews/PBI-001-review.md` | Vấn đề phát hiện, bằng chứng, khuyến nghị và kết quả review |
| `.specify/_planning/workflow-state.md` | Tiến độ thực tế và bước còn chờ |
| `.specify/_planning/approvals.json` | Ghi nhận các quyết định phê duyệt thực tế |
| `.specify/R1/PBI-001-ten-ngan/` | Cặp business.md/spec.md đã được cho phép xuất |

File `.md` là văn bản Markdown; có thể đọc trực tiếp hoặc dùng Open Preview trong trình soạn thảo. Metadata và khối YAML giúp máy kiểm tra liên kết giữa các bước; bạn tập trung đọc các mục nội dung và câu hỏi nghiệp vụ.

## 9. Khi câu nhắn chưa chạy được

- **Không thấy skill**: kiểm tra đã cài cho project chưa; xem [INSTALL.md](INSTALL.md).
- **Thiếu cấu hình**: nhắn “Đề xuất ba-project.yaml từ template và hỏi tôi xác nhận các giá trị thiết yếu.”
- **Thiếu file đầu vào**: xem skill upstream được báo; dùng `ba-workflow` nếu muốn làm chuỗi bước cần thiết.
- **Thiếu thư viện Python**: cung cấp Python đã cài thư viện cho Codex, ví dụ “Dùng `D:/BA-Skills-Kit/.venv/Scripts/python.exe` để chạy công cụ Kit.” Thay bằng vị trí thật trên máy.
- **Sai PBI**: chọn ID thật từ backlog, không lấy số trong ví dụ nếu chưa tồn tại.
- **Xung đột khi publish**: yêu cầu so bản cũ/mới và thống nhất cách giữ lịch sử trước khi ghi tiếp.

Tham khảo thêm: [quy ước tài liệu](conventions/BA-CONVENTIONS.md), [hướng dẫn từng skill](skills/), [báo cáo kiểm thử](tests/INTEGRATION_REPORT.md). Các file trong `tests/fixtures` là ví dụ giả lập, không phải hồ sơ hay phê duyệt cho dự án thật của bạn.
