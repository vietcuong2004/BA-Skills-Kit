# BA Skills Kit — Từ ý tưởng phần mềm đến bộ tài liệu để phát triển

**Bạn mô tả phần mềm mình muốn làm. Bộ skill này hướng dẫn agent AI phân tích ý tưởng, chia thành các phần việc, lập kế hoạch và viết tài liệu nghiệp vụ cùng đặc tả cho từng phần việc.**

Ví dụ đầu vào:

> Tôi muốn xây dựng website ghi chú cá nhân và công ty, hỗ trợ tạo tài liệu từ mẫu và tìm kiếm.

Sau các bước phân tích và những lần bạn xem xét, xác nhận, bạn sẽ nhận được:

- Bản mô tả sản phẩm: phục vụ ai, giải quyết vấn đề gì, gồm những khả năng nào.
- Danh sách yêu cầu và các phần việc cần phát triển.
- Kế hoạch chia các phần việc thành từng đợt.
- Với mỗi phần việc được chọn: tài liệu nghiệp vụ và đặc tả hành vi, điều kiện nghiệm thu để lập trình viên và người kiểm thử sử dụng.

Kit tập trung vào **phân tích và chuẩn bị tài liệu**. Lập trình, chạy sản phẩm và triển khai là các công việc tiếp theo, ngoài workflow này.

## 1. Skill là gì? Bạn cần chuẩn bị gì?

**Skill** là bộ hướng dẫn để agent AI (Claude Code, Codex hoặc Antigravity) thực hiện một loại công việc theo quy trình nhất quán. Bạn gọi skill trong cuộc trò chuyện với agent rồi cung cấp ý tưởng hoặc yêu cầu bằng ngôn ngữ tự nhiên.

Bộ này có **9 skill**. Người mới nên dùng **`ba-workflow`**: skill này hướng dẫn agent thực hiện các bước theo thứ tự và dừng ở những chỗ cần bạn quyết định. Bạn không cần nhớ và gọi riêng cả 9 skill.

Agent sẽ viết các file thật trong thư mục dự án. Các công cụ Python đi kèm kiểm tra file và hỗ trợ xuất tài liệu; chúng không tự tạo nội dung phân tích khi chạy một mình.

Bạn cần:

1. Codex có thể mở và làm việc với thư mục trên máy.
2. Python 3.10 trở lên cùng thư viện của Kit; phần cài đặt bên dưới hướng dẫn cụ thể.
3. Một thư mục dự án và mô tả ý tưởng. Dự án có thể mới hoàn toàn, chưa có mã nguồn.

### Các từ thường gặp

| Thuật ngữ | Hiểu đơn giản | Ví dụ |
| --- | --- | --- |
| BA — Business Analyst | Người phân tích nhu cầu và nghiệp vụ | Làm rõ ai được xem ghi chú công ty |
| Capability — CAP | Một khả năng sản phẩm cần có | Quản lý ghi chú cá nhân |
| Requirement — REQ | Yêu cầu cụ thể về sản phẩm | Người dùng tạo và đọc lại ghi chú |
| Epic / Feature | Nhóm nhu cầu lớn / nhóm chức năng bên trong | Quản lý tri thức → Ghi chú cá nhân |
| PBI — Product Backlog Item | Một phần việc có giá trị người dùng, có thể mô tả và nghiệm thu | `PBI-001`: Tạo ghi chú cá nhân |
| Backlog | Danh sách các PBI cần xem xét phát triển | Tạo ghi chú, tạo từ mẫu, tìm kiếm… |
| Round | Một đợt thực hiện các PBI đã chọn | `R1`: Làm hành trình tạo và đọc ghi chú |
| AC — Acceptance Criteria | Điều kiện để xác định phần việc đạt yêu cầu | Lưu xong thì đọc lại đúng nội dung |
| Review | Kiểm tra chất lượng tài liệu và chỉ ra điểm cần sửa | AC thiếu tình huống mất kết nối |
| Publish | Đưa cặp tài liệu đã kiểm tra vào thư mục bàn giao | Xuất vào `.specify/R1/PBI-001-tao-ghi-chu/` |

Round có thể tổ chức theo từng dự án, không bắt buộc là Sprint Scrum. **Publish ở đây là xuất file trong dự án**, không phải đưa website lên Internet.

## 2. Các bước thực hiện theo thứ tự

```text
Bạn mô tả ý tưởng
        ↓
1. Làm rõ sản phẩm                  → brainstorm.md
        ↓
2. Phân tích yêu cầu                → requirements.md
        ↓
3. Chia thành các phần việc         → product-backlog.md
        ↓
   BẠN XEM VÀ DUYỆT PHẠM VI / BACKLOG
        ↓
4. Lập kế hoạch từng đợt            → round-plan.md
        ↓
   BẠN DUYỆT KẾ HOẠCH HOẶC CHO PHÉP DÙNG BẢN ĐỀ XUẤT
        ↓
   Với từng PBI được chọn:
5. Viết tài liệu nghiệp vụ          → bản nháp business.md
6. Viết đặc tả để Dev / QA sử dụng  → bản nháp spec.md
7. Kiểm tra tài liệu                → báo cáo review
        ↓
   Có lỗi quan trọng: sửa theo findings rồi review lại
        ↓
   BẠN XEM KẾT QUẢ VÀ CHO PHÉP XUẤT TÀI LIỆU
        ↓
8. Xuất cặp tài liệu vào thư mục Round / PBI
```

`ba-workflow` điều phối toàn bộ quy trình và lưu tiến độ để tiếp tục ở lần làm việc sau.

| Bước | Skill | Agent làm gì? | File tạo ra | Bạn cần xem gì? |
| --- | --- | --- | --- | --- |
| 1 | `ba-brainstorm` | Làm rõ người dùng, vấn đề, mục tiêu, phạm vi, khả năng sản phẩm và giả định | `brainstorm.md` | Ý tưởng đã được hiểu đúng và đủ chưa? |
| 2 | `ba-requirements` | Phân tích yêu cầu, quy tắc, quyền, luồng xử lý và tình huống đặc biệt | `requirements.md` | Quy tắc nào có căn cứ, câu nào cần quyết định? |
| 3 | `ba-product-backlog` | Nhóm Epic → Feature → PBI; đề xuất ưu tiên, phạm vi và phụ thuộc | `product-backlog.md` | Chọn phạm vi; sửa PBI quá lớn hoặc thiếu nhu cầu |
| 4 | `ba-round-plan` | Đề xuất mục tiêu và PBI từng đợt, chỉ rõ thông tin còn thiếu về năng lực thực hiện | `round-plan.md` | Thứ tự hợp lý chưa, đủ cơ sở cam kết khối lượng chưa? |
| 5 | `ba-business` | Giải thích vì sao cần PBI, ai dùng, giá trị, quy trình và giải pháp phần mềm | `drafts/PBI-xxx/business.md` | Đúng vấn đề, giá trị và phạm vi đã chọn chưa? |
| 6 | `ba-spec` | Mô tả luồng chính, nhánh khác, lỗi, quyền, dữ liệu và điều kiện nghiệm thu | `drafts/PBI-xxx/spec.md` | Dev hiểu cần làm gì và QA biết cần kiểm chứng gì chưa? |
| 7 | `ba-review` | Đối chiếu tài liệu, tìm điểm thiếu hoặc mâu thuẫn, ghi bằng chứng và khuyến nghị | `reviews/PBI-xxx-review.md` | Những lỗi nào phải sửa trước khi bàn giao? |
| 8 | `ba-publish` | Kiểm tra nguồn, review, phê duyệt và đường dẫn; xuất đúng hai file của PBI | `R…/PBI-xxx-ten-ngan/business.md` và `spec.md` | Xem trước các file sẽ xuất và cho phép xuất PBI đã chọn |
| Điều phối | `ba-workflow` | Thực hiện theo thứ tự, kiểm tra kết quả và lưu bước đang làm / còn chờ | `workflow-state.md` cùng các output trên | Đang ở đâu và cần làm gì tiếp? |

**Bạn vẫn là người quyết định yêu cầu nghiệp vụ.** AI có thể đề xuất, nhưng đề xuất chưa tự trở thành quyết định được duyệt. Kit cũng không tự gán story points hoặc cam kết số lượng PBI khi chưa có cơ sở.

## 3. Output là gì, nằm ở đâu?

Với cấu hình mặc định, các file nằm trong thư mục dự án như ví dụ sau. Đây là **một PBI đã được chọn và xuất tài liệu**, không phải số lượng PBI/Round cố định.

```text
MyProject/
├── ba-project.yaml                 Cấu hình riêng của dự án
├── .agents/
│   └── skills/                     Nơi cài 9 skill cho Codex
└── .specify/
    ├── _planning/                  Hồ sơ phân tích và bản nháp
    │   ├── inputs/
    │   │   └── idea.txt            Ý tưởng gốc nếu được lưu từ chat
    │   ├── brainstorm.md
    │   ├── requirements.md
    │   ├── product-backlog.md
    │   ├── round-plan.md
    │   ├── workflow-state.md       Tiến độ, bước chờ, vấn đề chưa giải quyết
    │   ├── approvals.json          Ghi nhận quyết định phê duyệt thực tế
    │   ├── drafts/
    │   │   └── PBI-001/
    │   │       ├── business.md     Bản nháp nghiệp vụ
    │   │       └── spec.md         Bản nháp đặc tả
    │   └── reviews/
    │       └── PBI-001-review.md   Kết quả kiểm tra cặp tài liệu
    └── R1/
        └── PBI-001-tao-ghi-chu/
            ├── business.md        Bản được phép xuất để bàn giao
            └── spec.md            Bản được phép xuất để bàn giao
```

Mỗi thư mục PBI được publish chứa **chính xác hai file**: `business.md` và `spec.md`. Review và hồ sơ phê duyệt nằm trong `_planning`.

### Hai file bàn giao khác nhau thế nào?

**`business.md` trả lời “Vì sao cần làm và cần giải quyết điều gì?”** File mô tả câu chuyện nghiệp vụ, đối tượng, vấn đề, mục tiêu, giá trị, quy trình, giải pháp, phạm vi và rủi ro.

**`spec.md` trả lời “Phần mềm phải hoạt động ra sao để được nghiệm thu?”** File mô tả điều kiện trước/sau, thao tác người dùng, phản hồi hệ thống, quyền, dữ liệu, lỗi, tình huống đặc biệt và tiêu chí nghiệm thu.

Ví dụ một tiêu chí trong spec:

> **Given** người dùng đang ở không gian cá nhân và có quyền tạo ghi chú; **When** gửi dữ liệu hợp lệ; **Then** ghi chú được lưu đúng chủ sở hữu và có thể đọc lại.

Đây là ví dụ cách diễn đạt. Quy tắc dữ liệu và quyền thực tế phải được phân tích từ dự án của bạn.

### Đọc file `.md` thế nào?

`.md` là file văn bản Markdown. Bạn có thể mở bằng trình soạn thảo; trong VS Code có thể dùng **Open Preview** để xem dạng trình bày.

Tài liệu sinh ra có thông tin đầu file và khối dữ liệu YAML để các skill trao đổi dữ liệu, cùng các mục dễ đọc. Người mới tập trung vào các mục nội dung, bảng và câu hỏi. Khi muốn sửa, hãy yêu cầu Codex cập nhật file, giữ ID và kiểm tra lại các file phụ thuộc.

## 4. Cài đặt và bắt đầu sử dụng

Xem **[INSTALL.md](INSTALL.md)** để cài theo công cụ bạn dùng:

- **Claude Code**: cài vào `.claude/skills`, gọi `/ba-workflow`.
- **Codex**: cài vào `.agents/skills`, gọi `$ba-workflow` hoặc chọn qua giao diện.
- **Antigravity**: cài vào `.agents/skills`, yêu cầu agent dùng `ba-workflow`.

INSTALL hướng dẫn chuẩn bị Python, cài skill, tạo `ba-project.yaml`, kiểm tra nhận diện và gửi ý tưởng đầu tiên. Các ví dụ `$ba-…` bên dưới dùng cách gọi của Codex; trên Claude Code dùng `/ba-…`, trên Antigravity nêu tên skill và tham số tương ứng.

Cả ba dùng cùng quy trình BA và vị trí output theo cấu hình dự án. Hướng dẫn cài Claude Code/Antigravity dựa trên tài liệu chính thức; phần kiểm chứng runtime hiện có là Codex. Xem INSTALL để biết giới hạn cấu hình và kiểm thử.
## 5. Làm gì khi agent dừng để hỏi bạn?

Workflow có ba điểm bạn cần quyết định. Bạn có thể yêu cầu sửa tài liệu trước khi đồng ý.

### Lần 1 — Duyệt backlog và phạm vi

Mở `product-backlog.md`. Kiểm tra PBI có đúng nhu cầu, thiếu gì, có phần việc quá lớn hoặc phạm vi chưa rõ không.

Ví dụ phản hồi sau khi đã đọc:

```text
Tôi duyệt backlog hiện tại. Hãy lập kế hoạch Round.
Ưu tiên hành trình tạo và đọc lại ghi chú cá nhân trước.
```

Hoặc yêu cầu sửa cụ thể: “Tách phần ghi chú công ty khỏi PBI cá nhân rồi cho tôi xem lại backlog.”

### Lần 2 — Duyệt kế hoạch hoặc cho phép dùng bản đề xuất

Mở `round-plan.md`. Xem mục tiêu mỗi đợt, PBI được chọn, phụ thuộc và thông tin còn thiếu. Nếu chưa có năng lực nhóm hoặc ước lượng, kế hoạch phải được giữ là đề xuất.

Ví dụ:

```text
Tôi cho phép dùng kế hoạch Round hiện tại ở dạng Proposed,
chưa cam kết khối lượng. Hãy tạo business, spec và review
cho PBI-001 trong R1, rồi dừng trước khi xuất tài liệu.
```

Chọn ID thực tế trong backlog; `PBI-001` và `R1` chỉ là ví dụ.

### Lần 3 — Cho phép xuất tài liệu

Đọc cặp nháp `business.md`, `spec.md` và review. Codex sẽ cho xem trước đường dẫn và file dự kiến được xuất; thao tác xem trước được gọi là **dry-run**.

| Review result | Ý nghĩa | Xử lý tiếp |
| --- | --- | --- |
| `PASS` | Không còn finding mở hoặc blocker theo review | Bạn vẫn cần cho phép publish |
| `CONDITIONAL` | Còn điểm cần làm rõ nhưng không có lỗi quan trọng đang mở | Chỉ xuất draft nếu bạn cho phép rõ ràng |
| `FAIL` | Còn lỗi quan trọng hoặc quyết định bắt buộc chưa giải quyết | Sửa nguồn, review lại trước khi publish |

“Finding” là vấn đề review phát hiện; “blocker” là vấn đề bắt buộc giải quyết trước khi đi tiếp.

Ví dụ khi đã xem dry-run và review PASS:

```text
Tôi đồng ý xuất cặp tài liệu hiện tại của PBI-001 vào R1
theo dry-run vừa trình bày. Hãy publish và kiểm tra kết quả.
```

Nếu review CONDITIONAL và bạn chấp nhận xuất nháp, nói rõ: “Tôi cho phép Draft Publication cho PBI-001; giữ trạng thái draft và các finding còn mở.”

Codex ghi nhận quyết định vào hồ sơ phê duyệt rồi kiểm tra trước/sau khi xuất. **Review PASS và trạng thái tài liệu được duyệt là hai điều khác nhau.** File xuất có thể vẫn là draft theo đúng quyết định của bạn.

Các nhãn nội dung thường gặp: **Confirmed** = đã có căn cứ xác nhận, **Proposed** = đề xuất, **Open Question** = câu hỏi chưa quyết định. Trạng thái toàn tài liệu: **draft** = nháp, **in_review** = đang xem xét, **approved** = đã được duyệt. Chúng không thay thế cho nhau.

## 6. Tiếp tục công việc hoặc chạy riêng một bước

### Tiếp tục ở lần làm việc sau

Mở lại cùng project và gửi:

```text
$ba-workflow mode=RESUME project_config=./ba-project.yaml
Đọc workflow-state và tiếp tục từ bước đang chờ.
Python dùng cho công cụ Kit: D:/BA-Skills-Kit/.venv/Scripts/python.exe
```

Codex kiểm tra file thật và các nguồn trước khi tiếp tục. Nếu bạn đã sửa yêu cầu, tài liệu phía sau có thể cần cập nhật/review lại.

### Chỉ viết spec cho một PBI

Khi đã có business draft cùng backlog và requirements hợp lệ:

```text
$ba-spec pbi_id=PBI-001 project_config=./ba-project.yaml
Viết đặc tả cho đúng PBI này từ business draft hiện tại.
Kiểm tra flows, edge cases và điều kiện nghiệm thu.
Python dùng cho công cụ Kit: D:/BA-Skills-Kit/.venv/Scripts/python.exe
```

Skill đơn lẻ thiếu đầu vào sẽ báo file còn thiếu và bước cần chạy trước. Khi cần Codex thực hiện nhiều bước liên tiếp, dùng `ba-workflow` và nêu rõ phạm vi mong muốn.

### Cập nhật yêu cầu đã có

Ví dụ: “Yêu cầu tạo ghi chú đã thay đổi như sau… Hãy cập nhật requirements, giữ ID cũ, chỉ ra các PBI/tài liệu bị ảnh hưởng và dừng ở quyết định cần tôi duyệt.”

Kit lưu dấu nhận diện nội dung nguồn bằng SHA-256 để phát hiện thay đổi. `STALE_INPUT` có nghĩa là nguồn đã đổi kể từ lúc tài liệu phụ thuộc được tạo. Cần đọc lại nguồn, cập nhật và kiểm tra tài liệu bị ảnh hưởng; chỉ thay hash không giải quyết nội dung nghiệp vụ.

## 7. Những lỗi thường gặp

| Tình huống | Cách xử lý |
| --- | --- |
| `python` không được nhận diện | Cài Python, mở lại terminal, kiểm tra `python --version` |
| `No module named yaml` hoặc `jsonschema` | Dùng đúng `.venv/Scripts/python.exe` đã cài thư viện; gửi đường dẫn đó cho Codex |
| Không thấy `ba-workflow` | Kiểm tra project có `.agents/skills/ba-workflow/SKILL.md`, mở Codex tại đúng project rồi mở phiên mới |
| `MISSING_CONFIG` | Tạo `ba-project.yaml` tại root project, truyền đúng `project_config` |
| `MISSING_INPUT` | Đọc đường dẫn còn thiếu, chạy skill upstream được chỉ ra; hoặc yêu cầu workflow điều phối phần việc đó |
| `PBI_MISMATCH` / `BROKEN_REF` | Dùng đúng ID trong backlog; yêu cầu Codex sửa liên kết tài liệu từ nguồn đúng |
| `STALE_INPUT` | Yêu cầu cập nhật/review lại tài liệu phụ thuộc nguồn đã đổi |
| `MISSING_APPROVAL` | Xem nội dung/dry-run rồi đưa ra quyết định rõ ràng cho checkpoint còn thiếu |
| `PUBLISH_CONFLICT` / `ROUND_TRANSFER_CONFLICT` | So bản cũ/mới, quyết định cách giữ lịch sử; công cụ giữ lại nội dung hiện có |

Cài user-wide và hướng dẫn thêm cho macOS/Linux nằm trong [INSTALL.md](INSTALL.md).

## 8. Cập nhật skill và xem tài liệu tham khảo

Hướng dẫn cập nhật bản đã cài nằm trong [INSTALL.md](INSTALL.md#8-cập-nhật-bản-đã-cài). Cập nhật skill không tự cập nhật nội dung BA đã tạo cho dự án.

| Muốn tìm hiểu thêm | Xem ở đâu |
| --- | --- |
| Cài đặt nâng cao, công cụ CLI và kiểm thử | [INSTALL.md](INSTALL.md) |
| Quy ước tài liệu, ID, trạng thái, nguồn và phê duyệt | [BA-CONVENTIONS.md](conventions/BA-CONVENTIONS.md) |
| Hướng dẫn chi tiết từng skill | [Thư mục skills](skills/) |
| Mẫu cấu hình | [ba-project.example.yaml](templates/ba-project.example.yaml) |
| Quy tắc cấu trúc dữ liệu để máy kiểm tra | [Thư mục contracts](contracts/) |
| Kết quả kiểm thử và giới hạn đã biết | [INTEGRATION_REPORT.md](tests/INTEGRATION_REPORT.md) |
| Ví dụ file trong lượt phân tích giả lập | [Fixture agent-notes](tests/fixtures/agent-notes/.specify/) |
| Bộ prompt dùng để xây dựng/bảo trì Kit | [SKILL_CREATION_PROMPTS.md](SKILL_CREATION_PROMPTS.md) |

Các fixture trong `tests/fixtures` là dữ liệu giả lập, gồm cả phê duyệt mô phỏng phục vụ kiểm thử. Khi bắt đầu dự án thật, hãy tạo cấu hình và nội dung riêng theo các bước trên.

