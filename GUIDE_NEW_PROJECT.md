# Dự án mới: từ ý tưởng mơ hồ đến bộ tài liệu PBI

[Về README](README.md) · [Cài đặt](INSTALL.md) · [Hướng dẫn cho dự án hiện có](GUIDE_EXISTING_PROJECT.md)

Dùng luồng này khi `your-project` chưa có sản phẩm hoàn chỉnh và bạn chỉ có một nhu cầu ban đầu. Không cần tự viết sẵn yêu cầu, Epic, PBI hay tiêu chí nghiệm thu.

**Mục tiêu:** làm rõ vấn đề, chọn phạm vi sản phẩm và chia thành các PBI có tài liệu để nhóm phát triển cùng xem xét, triển khai và kiểm thử.

## Trước khi bắt đầu

- Cài Kit theo [INSTALL.md](INSTALL.md).
- Tạo/mở thư mục `your-project` trong agent. Thư mục có thể chưa có mã nguồn.
- Chuẩn bị một vài câu về người cần dùng sản phẩm và vấn đề họ gặp. Nếu chưa biết, cứ nêu điều bạn đang hình dung.
- Chuẩn bị `ba-project.yaml`; nếu chưa có, để agent đề xuất và hỏi bạn xác nhận. Mặc định hồ sơ trung gian vào `.temp`, cặp tài liệu bàn giao vào `.specify`.

Các đoạn dưới gửi vào **chat agent**. Ví dụ dùng Codex `$ba-…`; Claude Code thay bằng `/ba-…`, Antigravity có thể dùng câu “Dùng skill ba-…”. Thay `[nội dung]`, `PBI-001` và `R1` bằng nhu cầu và ID thật trong dự án.

## Quy trình bạn sẽ đi qua

```text
Ý tưởng mơ hồ
    ↓
brainstorm → requirements → backlog → Bạn duyệt phạm vi
    ↓
Round plan → Bạn duyệt hoặc cho phép dùng kế hoạch Proposed
    ↓
business → spec → review cho các PBI được chọn
    ↓
Sửa/làm rõ nếu cần → Xem trước xuất file → Bạn cho phép publish
```

Dùng `ba-workflow` để điều phối. `ba-explore-project` dành cho khảo sát sản phẩm đã có tính năng; luồng này bắt đầu từ nhu cầu bạn cung cấp.

## 1. Gửi ý tưởng, dù chưa biết rõ chức năng

Copy vào chat:

```text
$ba-workflow
Tôi muốn bắt đầu your-project để giúp [nhóm người dùng]
giải quyết [vấn đề hoặc công việc đang khó khăn].

Ý tưởng hiện tại: [mô tả vài câu, có thể chưa rõ chức năng].
Tôi chưa biết cần những tính năng gì hoặc nên làm phần nào trước.

Hãy hỏi các câu ảnh hưởng lớn đến phạm vi, làm rõ người dùng,
vấn đề, mục tiêu và kết quả mong muốn. Phần chưa xác nhận
phải được ghi rõ là Proposed hoặc Open Question.

Kiểm tra ba-project.yaml; nếu chưa có, đề xuất cấu hình để tôi xác nhận.
Thực hiện ba-brainstorm → ba-requirements → ba-product-backlog,
tạo file và kiểm tra sau từng bước. Dừng để tôi duyệt backlog.
```

Không cần đoán trước giới hạn dữ liệu, quyền hay chỉ số để điền cho đủ. Khi agent hỏi, trả lời điều đã biết và nói rõ điều chưa quyết định. Không có research/KPI thì giữ mục tiêu định tính hoặc ghi giả thuyết.

**Kết quả mặc định:**

| File | Bạn đọc để kiểm tra gì? |
| --- | --- |
| `.temp/brainstorm.md` | Hiểu đúng người dùng, vấn đề, mục tiêu, nhóm khả năng sản phẩm và phạm vi chưa? |
| `.temp/requirements.md` | Các yêu cầu, quy tắc, quyền và luồng đã có căn cứ hay còn cần quyết định? |
| `.temp/product-backlog.md` | Có những PBI nào, giá trị gì, ưu tiên đề xuất và phụ thuộc ra sao? |
| `.temp/workflow-state.md` | Đã thực hiện bước nào và đang chờ quyết định gì? |

## 2. Hiểu PBI được hình thành thế nào và chỉnh phạm vi

PBI được phân rã từ yêu cầu đã phân tích. Ví dụ minh họa, nếu nhu cầu của bạn là quản lý hồ sơ:

```text
CAP-001: Quản lý hồ sơ
    ↓
REQ-001: Người có quyền tạo hồ sơ
    ↓
EPIC-001: Quản lý hồ sơ → FEAT-001: Tiếp nhận hồ sơ
    ↓
PBI-001: Tạo hồ sơ mới
```

Đây chỉ là ví dụ; nghiệp vụ và cách chia thật phải theo nhu cầu `your-project`. Một yêu cầu có thể liên quan nhiều PBI và ngược lại.

Trong backlog, xem mỗi PBI có một kết quả người dùng nhận được không, phạm vi có đủ nhỏ để nghiệm thu không, có trùng/thiếu nhu cầu không. Không cần tự ước lượng story points để duyệt phạm vi.

Nếu chưa đúng, phản hồi cụ thể:

```text
Dùng ba-workflow điều chỉnh phạm vi theo phản hồi sau:
[những phần muốn giữ, bỏ, hoãn, thêm hoặc làm rõ].

Cập nhật nguồn và backlog liên quan, giữ ID/quyết định còn hiệu lực.
Cho tôi xem phần thay đổi cùng các câu hỏi còn mở trước khi lập Round.
```

Bạn có thể chọn phạm vi đầu tiên nhỏ, chưa cần chốt mọi chức năng tương lai.

## 3. Duyệt backlog và đề xuất Round

Khi đã đọc và đồng ý với phiên bản backlog hiện tại:

```text
Tôi duyệt phạm vi và backlog hiện tại.
Dùng ba-workflow tiếp tục bước ba-round-plan.

Ưu tiên kết quả đầu tiên là [giá trị hoặc hành trình muốn có trước].
Đề xuất các Round và PBI tương ứng, giải thích phụ thuộc và rủi ro.
Nếu chưa có capacity/ước lượng, giữ kế hoạch Proposed, không cam kết khối lượng.
Dừng để tôi xem kế hoạch.
```

**Kết quả:** `.temp/round-plan.md`. Round là đợt thực hiện theo nhu cầu dự án, không có số đợt cố định. Thiếu thông tin năng lực nhóm thì kế hoạch vẫn là đề xuất; PBI chưa sẵn sàng có thể chưa được phân Round.

## 4. Duyệt hoặc cho phép kế hoạch và chọn PBI để viết chi tiết

Sau khi đọc kế hoạch:

```text
Tôi cho phép dùng kế hoạch Round hiện tại ở dạng Proposed để viết bản nháp,
chưa cam kết khối lượng.

Dùng ba-workflow tạo tài liệu cho PBI-001 trong R1.
Thực hiện ba-business → ba-spec → ba-review, kiểm tra giữa từng bước.

Viết rõ bối cảnh, giá trị, scope, giải pháp, luồng chính/nhánh khác/lỗi,
quyền, dữ liệu, tình huống đặc biệt và tiêu chí Given–When–Then.
Quyết định chưa có nguồn phải ghi Proposed hoặc câu hỏi; vấn đề quan trọng
chưa chốt phải báo blocker. Dừng sau review, chưa publish.
```

Nếu đã đủ cơ sở và muốn duyệt kế hoạch chính thức, thay câu đầu bằng “Tôi duyệt kế hoạch Round hiện tại.” Có thể chọn thêm PBI khác bằng ID thực tế, nhưng nên bắt đầu với một hoặc vài PBI để kiểm tra chất lượng.

**Kết quả cho PBI được chọn:**

```text
.temp/drafts/PBI-001/business.md
.temp/drafts/PBI-001/spec.md
.temp/reviews/PBI-001-review.md
```

- Đọc **business**: đúng vấn đề, người dùng, giá trị, phạm vi và giải pháp mong muốn chưa?
- Đọc **spec**: hiểu được người dùng làm gì, hệ thống phản hồi ra sao, quyền/dữ liệu thay đổi thế nào và nghiệm thu bằng gì chưa?
- Đọc **review**: còn thiếu hoặc mâu thuẫn ở đâu, vấn đề nào cần bạn quyết định?

Ví dụ AC: **Given** người dùng có quyền và đã nhập dữ liệu hợp lệ; **When** gửi yêu cầu tạo; **Then** hệ thống lưu và cho đọc lại đúng dữ liệu. Trường dữ liệu và quyền thực tế phải được xác định trong hồ sơ của bạn.

## 5. Trả lời các câu hỏi và review lại

| Kết quả review | Ý nghĩa và bước tiếp theo |
| --- | --- |
| `PASS` | Không còn finding mở hoặc blocker theo review; bạn vẫn cần xem xét trước khi cho phép xuất. |
| `CONDITIONAL` | Còn điểm cần refinement; chỉ xuất draft khi bạn chấp nhận rõ ràng. |
| `FAIL` | Còn lỗi quan trọng hoặc blocker; giải quyết rồi sửa/review lại. |

Ví dụ phản hồi:

```text
Dùng ba-workflow xử lý các findings của PBI-001.
Quyết định của tôi cho các câu hỏi là: [ghi theo từng câu hỏi/finding].
Cập nhật business/spec trong phạm vi cần thiết, giữ ID và lịch sử thay đổi.
Review lại bằng ba-review, báo những điểm còn mở; chưa publish.
```

Review PASS là kết quả kiểm tra, không tự thay việc bạn duyệt yêu cầu hoặc cho phép bàn giao. Khi chưa biết câu trả lời, nói rõ để giữ câu hỏi/blocker thay vì chốt một quy tắc tùy ý.

## 6. Xem trước rồi xuất cặp tài liệu

Yêu cầu dry-run trước:

```text
Dùng ba-publish tạo dry-run cho PBI-001 trong R1.
Kiểm tra nguồn, review, Round và phê duyệt; cho tôi xem đường dẫn,
file sẽ tạo/bỏ qua và các xung đột. Chưa ghi vào .specify.
```

**Dry-run** là xem trước. Khi đã xem và đồng ý, nếu review PASS:

```text
Tôi cho phép publish cặp tài liệu hiện tại của PBI-001 vào R1
theo dry-run vừa trình bày. Dùng ba-publish thực hiện và kiểm tra sau ghi.
```

Nếu review CONDITIONAL và bạn chấp nhận bàn giao bản nháp, nói rõ: “Tôi cho phép Draft Publication cho cặp tài liệu hiện tại của PBI-001 theo dry-run; giữ trạng thái draft và các finding còn mở.” FAIL hoặc blocker chưa giải quyết phải được xử lý trước.

**Kết quả:**

```text
your-project/
├── .temp/                         # Ý tưởng, yêu cầu, backlog, drafts, review, state
└── .specify/
    └── R1/
        └── PBI-001-ten-tinh-nang/
            ├── business.md
            └── spec.md
```

Mỗi Round chứa các PBI đã được chọn; mỗi thư mục PBI xuất ra có đúng hai file trên. Giữ `.temp` vì nguồn và tiến độ vẫn được dùng để tiếp tục/review sau này. Việc xuất tài liệu chưa có nghĩa tính năng đã được lập trình hoặc triển khai.

## 7. Tiếp tục công việc hoặc bổ sung yêu cầu

Lần sau mở lại `your-project`:

```text
$ba-workflow mode=RESUME project_config=./ba-project.yaml
Kiểm tra state và nguồn, báo bước đã xong, bước còn chờ và các tài liệu stale.
Tiếp tục phần hợp lệ trong phạm vi đã chọn, giữ ID và quyết định còn hiệu lực.
```

Khi yêu cầu đổi, nói rõ thay đổi và đề nghị cập nhật các nguồn/tài liệu bị ảnh hưởng. `STALE_INPUT` nghĩa là nguồn đã thay đổi từ lần tạo tài liệu trước; cần đối chiếu và cập nhật thật, không chỉ sửa hash để bỏ cảnh báo.

Nếu đã có hồ sơ nền và chỉ muốn thêm một tính năng mới:

```text
$ba-pbi
Thêm một PBI cho [tính năng mới], đối chiếu hồ sơ hiện tại để tránh trùng.
Giữ các PBI cũ, phân tích delta và dừng để tôi duyệt phạm vi mới.
```

Nếu sau này sản phẩm đã có chức năng nhưng thiếu tài liệu cho phần triển khai thực tế, dùng [hướng dẫn khảo sát dự án hiện có](GUIDE_EXISTING_PROJECT.md).
