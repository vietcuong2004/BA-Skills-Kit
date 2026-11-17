# BA Skills Kit

**Biến một ý tưởng phần mềm thành bộ tài liệu yêu cầu và PBI có cấu trúc, sẵn sàng để nhóm phát triển cùng xem xét.**

BA Skills Kit gồm **9 skill pipeline và 2 skill phụ: khảo sát dự án hiện có, thêm một PBI mới** dành cho các AI coding agent như Codex và Claude Code. Bộ công cụ hỗ trợ Business Analyst (BA), Product Owner (PO) và nhóm phát triển đi từ một mô tả sản phẩm ban đầu đến danh sách công việc phát triển (**Product Backlog**), kế hoạch theo **Round** và tài liệu chi tiết cho từng **Product Backlog Item (PBI)**.

Bạn **không cần biết cách viết PBI ngay từ đầu**. Hãy mô tả sản phẩm muốn xây dựng bằng ngôn ngữ thông thường; bộ Skills sẽ hỗ trợ phân tích từng bước, tạo tài liệu để bạn đọc, chỉnh sửa và phê duyệt. **AI không thay thế người quyết định nghiệp vụ.**

> **Ví dụ:** “Tôi muốn làm website MISA Note, có ghi chú cá nhân, ghi chú công ty, tạo tài liệu từ mẫu, tìm kiếm và chia sẻ tài liệu.”
>
> Từ mô tả này, bộ Kit giúp làm rõ yêu cầu, chia nhỏ thành PBI, đề xuất PBI nào thực hiện ở R1/R2, rồi tạo `business.md` và `spec.md` cho từng PBI được chọn.

## 1. BA Skills Kit giải quyết vấn đề gì?

Khi bắt đầu một dự án, ý tưởng thường mới chỉ là một vài câu: *“Tôi muốn có tính năng tạo ghi chú, quản lý thư mục, chia sẻ tài liệu…”* Nhưng để Developer xây dựng và QA kiểm thử, nhóm dự án còn phải làm rõ:

- **Ai** sử dụng tính năng và **vì sao** họ cần nó?
- Người dùng sẽ thao tác **như thế nào**? Phần mềm phải phản hồi ra sao?
- Có những **quy tắc nghiệp vụ**, quyền truy cập và tình huống lỗi nào?
- Một tính năng lớn cần chia thành **những phần việc nhỏ nào**?
- **Làm phần nào trước**, phần nào sau?
- **Điều kiện nào** chứng minh PBI đã được triển khai đúng?

Nếu yêu cầu chưa rõ, nhóm phát triển dễ hiểu khác nhau, thiếu các trường hợp đặc biệt (*edge cases*) hoặc phải sửa lại sau khi đã lập trình. BA Skills Kit tạo một **quy trình phân tích có thể kiểm tra lại**, thay vì yêu cầu AI viết tất cả tài liệu trong một lần.

### Những thuật ngữ cần biết

| Thuật ngữ | Hiểu đơn giản |
|---|---|
| **BA** | Người phân tích nhu cầu, quy trình và yêu cầu phần mềm. |
| **Skill** | Bộ hướng dẫn để AI thực hiện một công việc cụ thể theo quy tắc đã định. |
| **Epic** | Nhóm công việc lớn, ví dụ *Quản lý ghi chú*. |
| **Feature** | Một nhóm chức năng thuộc Epic, ví dụ *Ghi chú cá nhân*. |
| **PBI** | Một phần việc cụ thể trong Product Backlog, có phạm vi và kết quả kiểm chứng được; ví dụ *Tạo ghi chú cá nhân*. |
| **Product Backlog** | Danh sách các PBI cần xem xét, ưu tiên và thực hiện. |
| **Round** | Đợt triển khai gồm các PBI được chọn. Đây là cách tổ chức của nhóm dự án; không mặc định giống hoàn toàn Scrum Sprint. |
| **Acceptance Criteria (AC)** | Các điều kiện nghiệm thu: làm thế nào để biết tính năng đáp ứng yêu cầu. |
| **Edge Case** | Trường hợp đặc biệt hoặc sát giới hạn, ví dụ bấm Lưu hai lần, mất mạng khi đang lưu, quyền truy cập bị thu hồi. |

## 2. Quy trình hoạt động: từ ý tưởng đến PBI

BA Skills Kit có **8 bước nghiệp vụ** và **1 Skill điều phối** tên `ba-workflow`.

```text
BẠN NHẬP Ý TƯỞNG SẢN PHẨM
   │
   ▼
01. ba-brainstorm        → brainstorm.md
    Làm rõ sản phẩm, người dùng, vấn đề, mục tiêu
   │
   ▼
02. ba-requirements      → requirements.md
    Phân tích yêu cầu, quy tắc, luồng và tình huống đặc biệt
   │
   ▼
03. ba-product-backlog   → product-backlog.md
    Chia yêu cầu thành Epic → Feature → PBI
   │
   ├── BẠN XEM VÀ XÁC NHẬN BACKLOG
   ▼
04. ba-round-plan        → round-plan.md
    Đề xuất PBI cho R1, R2, R3…
   │
   ├── BẠN XEM VÀ XÁC NHẬN KẾ HOẠCH
   ▼
    LẶP LẠI VỚI TỪNG PBI ĐƯỢC CHỌN
   │
05. ba-business          → business.md (bản nháp)
    Giải thích bối cảnh, mục tiêu, giá trị, giải pháp nghiệp vụ
   │
   ▼
06. ba-spec              → spec.md (bản nháp)
    Mô tả luồng xử lý, quy tắc, edge cases, AC
   │
   ▼
07. ba-review            → báo cáo review
    Kiểm tra thiếu sót, mâu thuẫn và khả năng kiểm thử
   │
   ├── BẠN XỬ LÝ CÁC VẤN ĐỀ VÀ CHO PHÉP XUẤT
   ▼
08. ba-publish           → .specify/R1/PBI-001-.../
    Xuất 2 file business.md và spec.md vào thư mục PBI
```

**Điểm cốt lõi:** File do bước trước tạo ra là **đầu vào thực tế** của bước sau. Ví dụ, `ba-product-backlog` đọc `requirements.md` để tạo PBI; `ba-spec` đọc `business.md` và các yêu cầu liên quan để viết đặc tả. Bộ Kit dùng **Data Contracts** (quy ước cấu trúc dữ liệu) và chương trình kiểm tra (*validator*) để phát hiện file thiếu trường, sai ID hoặc tham chiếu không hợp lệ.

### Mỗi Skill làm gì?

| Bước | Skill | Việc cần làm | Kết quả |
|---|---|---|---|
| 1 | `ba-brainstorm` | Hiểu ý tưởng, xác định người dùng, vấn đề, nhóm chức năng, mục tiêu | `brainstorm.md` |
| 2 | `ba-requirements` | Chuyển ý tưởng thành yêu cầu chức năng, quy tắc, quyền, luồng, ngoại lệ | `requirements.md` |
| 3 | `ba-product-backlog` | Nhóm yêu cầu thành Epic, Feature, các PBI nhỏ có giá trị | `product-backlog.md` |
| 4 | `ba-round-plan` | Đề xuất ưu tiên, phụ thuộc và phân bổ PBI theo Round | `round-plan.md` |
| 5 | `ba-business` | Viết câu chuyện nghiệp vụ, mục tiêu, giá trị và giải pháp cho một PBI | `business.md` |
| 6 | `ba-spec` | Viết User Story, luồng chính/nhánh khác/lỗi, edge cases, AC | `spec.md` |
| 7 | `ba-review` | Đối chiếu hai file, tìm lỗi và câu hỏi còn mở | Báo cáo review |
| 8 | `ba-publish` | Kiểm tra điều kiện, xuất tài liệu đã được cho phép vào đúng Round | Thư mục PBI |
| Điều phối | `ba-workflow` | Gọi/điều phối các bước trên, ghi tiến độ và dừng tại điểm cần duyệt | Quy trình xuyên suốt |

Bạn có thể dùng **`ba-workflow`** để đi qua nhiều bước hoặc gọi **từng Skill riêng** khi chỉ cần làm một việc.

## 3. Ví dụ xuyên suốt: xây dựng MISA Note

Giả sử bạn nhập:

> Tôi muốn xây dựng website MISA Note cho cá nhân và doanh nghiệp. Người dùng có thể tạo ghi chú cá nhân, ghi chú công ty, tạo tài liệu nhanh từ mẫu, soạn thảo nội dung, tìm kiếm, tổ chức theo thư mục và chia sẻ tài liệu.

**Bước 1 – Làm rõ ý tưởng.** AI lập `brainstorm.md`, nhóm các năng lực như *Quản lý ghi chú*, *Soạn thảo tài liệu*, *Tìm kiếm*, *Chia sẻ*. Đồng thời ghi câu hỏi còn thiếu: ai được tạo ghi chú công ty, có cho phép chia sẻ ngoài công ty không, v.v.

**Bước 2 – Phân tích yêu cầu.** AI lập `requirements.md`. Ví dụ, từ nhóm *Quản lý ghi chú* có yêu cầu `REQ-001 – Tạo ghi chú cá nhân`, `REQ-002 – Chỉnh sửa ghi chú cá nhân`. Với mỗi yêu cầu, tài liệu mô tả hành vi, quy tắc và tình huống cần làm rõ.

**Bước 3 – Lấy PBI từ yêu cầu.** AI lập `product-backlog.md`, ví dụ:

```text
EPIC-001: Quản lý ghi chú
└── FEAT-001: Ghi chú cá nhân
    ├── PBI-001: Tạo ghi chú cá nhân    ← REQ-001
    └── PBI-002: Chỉnh sửa ghi chú      ← REQ-002
```

Đây là bước trả lời câu hỏi **“PBI từ đâu mà có?”**: PBI được phân rã từ yêu cầu đã phân tích, không phải danh sách công việc AI nghĩ ra tùy ý. Bạn kiểm tra và điều chỉnh danh sách trước khi tiếp tục.

**Bước 4 – Lập Round.** AI đề xuất `round-plan.md`, chẳng hạn R1 gồm PBI-001 và PBI-002, R2 gồm những PBI khác. Đây chỉ là **đề xuất** nếu chưa có thông tin về năng lực nhóm, ưu tiên và phê duyệt.

**Bước 5 và 6 – Viết hai tài liệu cho PBI-001.**

- `business.md` trả lời **vì sao cần tính năng này, ai dùng, mang lại giá trị gì và giải pháp nghiệp vụ ra sao**.
- `spec.md` trả lời **phần mềm phải hoạt động cụ thể thế nào và kiểm tra đúng/sai bằng tiêu chí gì**.

Ví dụ `spec.md` có thể yêu cầu kiểm tra: tạo ghi chú thành công; nhập tiêu đề rỗng; bấm tạo nhiều lần; mất mạng khi lưu. Hành vi chưa được quyết định sẽ được ghi thành câu hỏi, **không tự coi là quy tắc đã duyệt**.

**Bước 7 – Review.** AI so sánh tài liệu với yêu cầu gốc, phát hiện AC còn thiếu hoặc các luồng mâu thuẫn. Bạn xử lý những điểm cần quyết định.

**Bước 8 – Xuất tài liệu.** Khi đủ điều kiện và được phép, bộ Kit tạo:

```text
MISA-Note/
└── .specify/
    ├── _planning/
    │   ├── brainstorm.md
    │   ├── requirements.md
    │   ├── product-backlog.md
    │   ├── round-plan.md
    │   ├── drafts/
    │   └── reviews/
    ├── R1/
    │   ├── PBI-001-tao-ghi-chu-ca-nhan/
    │   │   ├── business.md
    │   │   └── spec.md
    │   └── PBI-002-chinh-sua-ghi-chu/
    │       ├── business.md
    │       └── spec.md
    └── R2/
```

**Mỗi thư mục PBI chính thức chỉ có hai file `business.md` và `spec.md`.** Báo cáo review và tài liệu phân tích tổng thể nằm riêng trong `_planning/`.

## 4. Cần chuẩn bị gì trước khi sử dụng?

- Một **dự án phần mềm**: có thể là repository đã có mã nguồn hoặc một thư mục dự án mới.
- Một **AI Agent tương thích** đã được thiết lập, ví dụ Codex hoặc Claude Code.
- Bộ **BA Skills Kit đã được cài** cho Agent bạn sử dụng.
- **Python và các thư viện phụ thuộc** nếu bộ cài/script trong phiên bản Kit của bạn yêu cầu.
- Một **mô tả nhu cầu** bằng tiếng Việt. Không cần viết sẵn Epic, PBI hay AC.

Bộ Kit **không phải** một website có nút bấm riêng. Bạn sử dụng nó bằng cách trò chuyện với Agent đang mở dự án; Agent sẽ đọc hướng dẫn Skill và tạo/cập nhật file Markdown trong dự án.

## 5. Cài đặt BA Skills Kit

**Cài một lần trên mỗi máy**, sau đó dùng chung cho nhiều project. Bạn không cần sao chép toàn bộ `skills/`, `contracts/`, `scripts/`, `templates/` vào từng repository sản phẩm.

### Bước 1: Lấy bộ Kit

Tải hoặc clone repository [BA-Skills-Kit](https://github.com/vietcuong2004/BA-Skills-Kit) về máy.

### Bước 2: Cài cho Agent bạn đang dùng

Mở **[INSTALL.md](INSTALL.md)** và làm theo hướng dẫn dành cho **Codex**, **Claude Code** hoặc **Antigravity**. Hướng dẫn cài đặt có thể khác nhau giữa các Agent và phiên bản. Nếu phiên bản Kit có script cài đặt, hãy đọc `INSTALL.md` trước khi chạy; không mặc định rằng script tồn tại hoặc chạy được trên mọi máy.

### Bước 3: Kiểm tra Agent nhận diện được Skill

Mở Agent, yêu cầu:

```text
Hãy kiểm tra BA Skills Kit đã được cài chưa.
Liệt kê các BA Skills có thể sử dụng, đặc biệt là ba-workflow.
Chưa tạo hoặc sửa tài liệu dự án.
```

Nếu Agent không thấy Skill, kiểm tra đường dẫn cài đặt theo `INSTALL.md`. Chỉ đặt thư mục Kit ở đâu đó trên ổ đĩa **không đồng nghĩa** Agent đã nhận diện Skills.

### Bước 4: Mở dự án muốn phân tích

Mở Codex/Claude Code tại **thư mục gốc của dự án sản phẩm**, không phải thư mục gốc BA-Skills-Kit. Mỗi dự án có cấu hình `ba-project.yaml` riêng. Nếu chưa có, yêu cầu Agent đề xuất cấu hình từ mẫu và hỏi bạn xác nhận trước khi tạo.

> **Lưu ý:** `README.md` dành cho người đọc; `AGENTS.md`, `CLAUDE.md` và các `SKILL.md` là hướng dẫn cho Agent. Các file hướng dẫn ở root Kit không nhất thiết tự được đọc khi Agent đang làm việc ở repository khác. Cài đặt đúng là bước cần thiết.

## 6. Dùng lần đầu: chỉ cần gửi một câu lệnh

### Đang có dự án, muốn thêm một PBI cho tính năng mới

```text
$ba-pbi
Tạo một PBI mới cho tính năng: [mô tả tính năng muốn bổ sung].
Đọc hiện trạng và hồ sơ BA liên quan, phân tích phần thay đổi.
Thêm PBI vào backlog, giữ các PBI cũ và dừng để tôi duyệt phạm vi.
Sau khi tôi duyệt, viết business.md, spec.md và review cho đúng PBI đó.
```

Hoặc chỉ cần: **“Dùng skill BA-PBI để viết một PBI mới cho tính năng [mô tả] trong dự án hiện tại.”** Codex gọi `$ba-pbi`, Claude Code gọi `/ba-pbi`.

Skill đề xuất ID/parent/requirement refs dựa trên hồ sơ thật, kiểm tra overlap, cập nhật nguồn tối thiểu khi cần và giữ lịch sử. Nếu chưa có hồ sơ BA nền, nó chỉ ra bước explore/bootstrap cần thiết. Yêu cầu quá lớn sẽ được đề nghị thu nhỏ/tách trước khi tạo, không tự nhét nhiều outcome vào một PBI.

Output: request record trong `.specify/_planning/pbi-requests/`, backlog cập nhật và (sau duyệt scope) `drafts/PBI-ID/{business.md,spec.md}` cùng `reviews/PBI-ID-review.md`. Round là tùy chọn cho draft; publish là bước riêng. Xem [hướng dẫn BA-PBI](skills/ba-pbi/SKILL.md).

### Dự án đã có giao diện và chức năng, nhưng bạn chưa biết hiện trạng

```text
$ba-explore-project
Tôi chưa biết dự án này đang có những tính năng gì. Hãy khảo sát repository,
lập danh mục tính năng hiện hữu có bằng chứng, phân biệt UI/mock/backend/đã chạy thử.
Chuẩn bị đầu vào cho các skill BA hiện có để viết tài liệu PBI mô tả hiện trạng.
Dừng để tôi xem danh mục và chọn phạm vi trước khi chuyển sang pipeline BA.
```

Tên hiển thị là **BA-explore-project**, tên gọi kỹ thuật là `ba-explore-project`. Claude Code dùng `/ba-explore-project`; các agent khác có thể nhận câu “Dùng skill BA-explore-project để khảo sát dự án hiện tại”.

Output mặc định nằm trong `.specify/_planning/exploration/`:

- `project-exploration.json`: tính năng, mức xác minh, nguồn file/line/symbol và SHA-256.
- `project-exploration.md`: báo cáo hiện trạng để bạn đọc và chọn phạm vi.
- `exploration-brief.md`: đầu vào cho ba-brainstorm, giữ giới hạn và câu hỏi chưa rõ.

Sau khi đọc báo cáo, gửi:

```text
$ba-workflow
Tôi chọn tài liệu hóa [EXF IDs hoặc phân hệ] từ
.specify/_planning/exploration/exploration-brief.md.
Đọc inventory và report cùng thư mục, dùng làm input cho ba-brainstorm.
Tạo brainstorm → requirements → backlog mô tả hiện trạng, giữ evidence refs,
mức xác minh và câu hỏi còn mở. Đưa raw source_documents do helper explore
cung cấp vào brainstorm để phát hiện khi code/docs nguồn thay đổi.
Không coi các PBI hiện hữu là tính năng mới cần xây. Dừng để tôi duyệt backlog.
```

Sau đó tiếp tục Round → business/spec → review/publish như mục 7. Chín skill cũ và contracts của chúng giữ nguyên; skill phụ chỉ cung cấp đầu vào. Xem [handoff guide](skills/ba-explore-project/references/handoff-guide.md).

### Dự án mới hoặc nhu cầu mới đã mô tả được

Sau khi cài, mở Agent tại project và gửi **đoạn sau vào ô chat** (không phải PowerShell hoặc Terminal):

```text
Dùng skill ba-workflow để phân tích dự án hiện tại.

Ý tưởng của tôi: Tôi muốn xây dựng website ghi chú cho cá nhân và công ty,
có tạo ghi chú, tạo tài liệu từ mẫu, tìm kiếm, quản lý thư mục và chia sẻ.

Hãy đọc tài liệu dự án hiện có để hiểu bối cảnh.
Nếu có mã nguồn, phân biệt tính năng đã tồn tại và tính năng mới.
Kiểm tra ba-project.yaml; nếu chưa có, đề xuất cấu hình để tôi xác nhận.

Thực hiện ba-brainstorm → ba-requirements → ba-product-backlog.
Tạo các file đầu ra, kiểm tra dữ liệu sau từng bước.
Dừng lại để tôi xem và duyệt Product Backlog trước khi lập Round.
```

**Sau lệnh này bạn sẽ nhận được gì?** Theo cấu hình mặc định, các file sau được tạo trong project:

```text
.specify/_planning/brainstorm.md
.specify/_planning/requirements.md
.specify/_planning/product-backlog.md
```

Mở `product-backlog.md`, kiểm tra có thiếu PBI, trùng PBI hoặc chia PBI quá lớn không. Nếu chưa đúng, hãy yêu cầu sửa. **Không cần chạy lại từ đầu nếu chỉ cần điều chỉnh một phần**; Agent cần giữ ID và xác định các tài liệu bị ảnh hưởng.

## 7. Sau khi có Backlog, làm tiếp thế nào?

Quy trình thường có **ba lần bạn cần xem xét hoặc ra quyết định**.

### Lần 1: Xác nhận danh sách PBI

Khi backlog phù hợp, gửi:

```text
Tôi đã xem và đồng ý với phạm vi Product Backlog hiện tại.
Dùng ba-workflow tiếp tục bước ba-round-plan.
Đề xuất mục tiêu R1, R2 và các PBI cho từng Round.
Giải thích thứ tự ưu tiên và các phụ thuộc.
Dừng để tôi xem kế hoạch trước khi viết tài liệu PBI.
```

Kết quả: `.specify/_planning/round-plan.md`.

### Lần 2: Chọn PBI cần viết chi tiết

Sau khi xem Round Plan, gửi:

```text
Tôi cho phép sử dụng kế hoạch Round hiện tại để viết bản nháp.
Hãy tạo tài liệu cho PBI-001 và PBI-002 trong R1.
Với từng PBI, chạy ba-business → ba-spec → ba-review.
Bảo đảm spec có luồng chính, luồng thay thế, luồng lỗi,
Edge Cases và Acceptance Criteria theo Given–When–Then.
Dừng sau review; chưa publish.
```

Kết quả cho mỗi PBI, ví dụ:

```text
.specify/_planning/drafts/PBI-001/business.md
.specify/_planning/drafts/PBI-001/spec.md
.specify/_planning/reviews/PBI-001-review.md
```

Nếu review báo lỗi nghiêm trọng hoặc câu hỏi nghiệp vụ chưa giải quyết, hãy trả lời và yêu cầu sửa/review lại. **Review PASS không đồng nghĩa PO đã phê duyệt**.

### Lần 3: Cho phép xuất vào thư mục Round

Trước tiên yêu cầu xem trước:

```text
Dùng ba-publish kiểm tra PBI-001 của R1 và tạo dry-run.
Cho tôi xem đường dẫn, các file sẽ tạo và vấn đề còn tồn tại.
Chưa ghi file chính thức.
```

Nếu đồng ý với kết quả và PBI đủ điều kiện:

```text
Tôi cho phép publish PBI-001 vào R1 theo dry-run vừa trình bày.
Hãy xuất business.md và spec.md, sau đó kiểm tra lại kết quả.
```

**Publish ở đây nghĩa là xuất tài liệu vào cấu trúc thư mục của project**, không phải đưa website lên Internet.

## 8. Muốn dùng riêng một Skill thì sao?

Bạn không bắt buộc phải chạy cả quy trình. Ví dụ, khi đã có backlog và chỉ muốn viết đặc tả cho một PBI:

```text
Dùng skill ba-spec để viết spec.md cho PBI-001.
Đọc business.md, requirements.md và product-backlog.md tương ứng.
Phân tích đầy đủ Edge Cases và Acceptance Criteria.
Kiểm tra cấu trúc đầu ra và báo các câu hỏi chưa được xác nhận.
```

Hoặc chỉ muốn kiểm tra tài liệu:

```text
Dùng skill ba-review để kiểm tra business.md và spec.md của PBI-001.
Tìm các yêu cầu mơ hồ, thiếu Edge Cases, AC không thể kiểm thử
và mâu thuẫn giữa hai file. Không tự sửa khi chưa được phép.
```

**Điều kiện:** Skill riêng cần có tài liệu đầu vào từ các bước trước. Nếu thiếu hoặc không hợp lệ, nó phải báo rõ thay vì tự bịa dữ liệu. Dùng `ba-workflow` nếu muốn Agent điều phối nhiều bước.

## 9. Khi quay lại dự án vào hôm sau

Không cần mô tả lại toàn bộ ý tưởng. Nếu project đã có hồ sơ và trạng thái workflow, gửi:

```text
Dùng ba-workflow ở chế độ RESUME.
Đọc ba-project.yaml, workflow-state.md và các tài liệu hiện có.
Cho biết đã hoàn thành bước nào, đang chờ quyết định gì,
và tiếp tục từ bước hợp lệ gần nhất.
```

Nếu yêu cầu sản phẩm thay đổi, hãy nói rõ thay đổi đó. Agent cần kiểm tra tài liệu nào bị ảnh hưởng và giữ các ID/ quyết định còn hiệu lực, thay vì âm thầm viết lại toàn bộ PBI.

## 10. Bộ Kit gồm những thư mục gì?

```text
BA-Skills-Kit/
├── README.md                # Tài liệu bạn đang đọc
├── INSTALL.md               # Hướng dẫn cài đặt theo Agent
├── AGENTS.md                # Hướng dẫn chung cho Agent tương thích
├── CLAUDE.md                # Hướng dẫn dành cho Claude Code
├── SKILL.md                 # Điểm dẫn tới các Skills (nếu phiên bản Kit có)
├── skills/                  # 9 skill pipeline, ba-explore-project và ba-pbi
├── conventions/             # Quy ước viết tài liệu BA
├── contracts/               # Cấu trúc dữ liệu chuẩn giữa các bước
├── scripts/                 # Kiểm tra dữ liệu, quản lý tiến độ, xuất tài liệu
└── templates/               # Mẫu tài liệu
```

`tests/` chỉ được giữ local để kiểm tra/bảo trì Kit, đã được `.gitignore` bỏ qua và không nằm trong gói ZIP cài đặt. Máy hoặc dự án khác không cần thư mục này để dùng skill.

Phân biệt **hai nơi**:

- **BA-Skills-Kit:** bộ công cụ dùng chung; không chứa hồ sơ nghiệp vụ riêng của từng sản phẩm.
- **Project của bạn:** nơi lưu `ba-project.yaml`, thư mục `.specify/`, backlog, Round và tài liệu PBI.

Đó là lý do một máy có thể dùng cùng một BA Skills Kit cho MISA Note, CRM, ERP hoặc dự án khác mà không trộn dữ liệu giữa các project.

## 11. AI tự quyết được những gì?

AI có thể **đề xuất** yêu cầu, cách chia PBI, kế hoạch Round, quy tắc và tình huống đặc biệt. Tuy nhiên, phải phân biệt:

- **Confirmed:** đã được xác nhận bằng nguồn hoặc quyết định phù hợp.
- **Proposed:** phương án AI đề xuất, cần xem xét.
- **Open Question:** thông tin chưa rõ, cần người phụ trách trả lời.

AI **không được** tự coi đề xuất là quyết định chính thức; tự duyệt phạm vi hoặc kế hoạch; tự đổi PBI ID; tự sửa mã nguồn sản phẩm; tự commit/push; hoặc xuất tài liệu chính thức khi chưa đủ điều kiện và chưa được phép.

## 12. Câu hỏi thường gặp

**Tôi chưa biết BA hay Scrum, có dùng được không?** Có. Bạn có thể bắt đầu bằng mô tả nhu cầu thông thường. Tuy nhiên, vẫn cần người hiểu sản phẩm đọc và xác nhận tài liệu trước khi nhóm phát triển sử dụng.

**Tôi có cần viết tất cả PBI trong một lần không?** Không. Nên duyệt backlog trước, rồi chọn từng Round hoặc một vài PBI để viết chi tiết và review.

**Bộ Kit có lập trình website giúp tôi không?** Không phải mục đích chính. Bộ Kit tạo và kiểm tra **tài liệu phân tích nghiệp vụ**. Developer hoặc Agent lập trình có thể dùng các tài liệu đã duyệt làm đầu vào cho công việc tiếp theo.

**Có cần cài Kit vào mỗi project không?** Không, nếu đã thiết lập chế độ dùng chung đúng theo `INSTALL.md`. Mỗi project chỉ cần cấu hình và thư mục tài liệu riêng.

**Tại sao Skill sau không tự chạy khi Skill trước xong?** Các Skills là những đơn vị công việc độc lập. `ba-workflow` đảm nhận việc điều phối theo trình tự, kiểm tra đầu ra và dừng ở những điểm cần bạn duyệt.

**Tôi không thấy Skill trong Codex/Claude Code?** Xem [INSTALL.md](INSTALL.md), kiểm tra đường dẫn cài đặt và khả năng nhận diện Skill của Agent đang sử dụng. Không mặc định mọi Agent đọc cùng một loại file hướng dẫn.

---

## Bắt đầu ngay

**Người mới:** Đọc [INSTALL.md](INSTALL.md) để cài BA Skills Kit → mở project trong Agent → gửi prompt ở [Mục 6](#6-dùng-lần-đầu-chỉ-cần-gửi-một-câu-lệnh) → đọc và duyệt Product Backlog → tiếp tục lập Round và viết PBI.

**Người đã cài:** Gọi `ba-workflow` với mô tả sản phẩm và cho biết muốn dừng ở bước nào.

**Mục tiêu cuối cùng:** Mỗi PBI được chọn có một cặp tài liệu **`business.md` + `spec.md`** nhất quán, truy vết được về yêu cầu ban đầu và được tổ chức đúng Round để nhóm dự án cùng sử dụng.
