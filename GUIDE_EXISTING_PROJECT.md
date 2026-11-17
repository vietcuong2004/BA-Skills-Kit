# Dự án đã có tính năng: từ khảo sát hiện trạng đến tài liệu PBI

[Về README](README.md) · [Cài đặt](INSTALL.md) · [Hướng dẫn cho dự án mới](GUIDE_NEW_PROJECT.md)

Dùng luồng này khi `your-project` đã có giao diện, mã nguồn hoặc các chức năng đang hoạt động, nhưng thiếu tài liệu nghiệp vụ. Bạn có thể chưa biết dự án đang có những gì.

**Mục tiêu:** mô tả đúng sản phẩm hiện có bằng các PBI và cặp `business.md`/`spec.md`. Những PBI này phục vụ tài liệu hóa hiện trạng; không mặc định là tính năng cần xây mới.

## Trước khi bắt đầu

- Cài Kit theo [INSTALL.md](INSTALL.md), rồi mở agent tại root `your-project`.
- Agent cần đọc được repository và chạy Python có thư viện của Kit.
- Kiểm tra `.temp/ba-project.yaml`. Nếu đang có `ba-project.yaml` cũ ở root, cập nhật skill và chuyển file theo [INSTALL.md](INSTALL.md), không tạo thêm cấu hình mới. Nếu chưa có cấu hình nào, để agent đề xuất từ template và hỏi bạn xác nhận trước khi ghi hồ sơ.
- Mặc định hồ sơ làm việc nằm trong `.temp`; `.specify` chỉ chứa các cặp tài liệu đã được phép xuất.

Các đoạn dưới gửi vào **ô chat agent**. Ví dụ dùng cú pháp Codex `$ba-…`; Claude Code thay bằng `/ba-…`, Antigravity có thể dùng câu “Dùng skill ba-…”. Thay `[nội dung]`, `EXF-001`, `PBI-001`, `R1` bằng giá trị thật sau khi khảo sát.

## Quy trình bạn sẽ đi qua

```text
ba-explore-project → Bạn xem danh mục và chọn phạm vi tài liệu hóa
        ↓
ba-workflow: brainstorm → requirements → backlog → Bạn duyệt backlog
        ↓
Round plan → Bạn duyệt hoặc cho phép dùng kế hoạch Proposed
        ↓
business → spec → review cho các PBI được chọn
        ↓
Sửa/làm rõ nếu cần → Xem trước xuất file → Bạn cho phép publish
```

## 1. Khảo sát tính năng bằng ba-explore-project

Copy vào chat:

```text
$ba-explore-project
Tôi chưa biết rõ your-project. Dự án đã có giao diện và chức năng
nhưng thiếu bộ tài liệu nghiệp vụ.

Hãy đọc tài liệu và repository để xác định các tính năng hiện có,
nhóm theo phân hệ, chỉ rõ người dùng, điểm vào, luồng xử lý,
dữ liệu, quyền và quy tắc tìm được.

Ghi bằng chứng từ file/symbol; phân biệt chỉ có UI, dữ liệu mock,
có xử lý trong code và hành vi thực sự đã chạy thử.
Không kết luận tính năng hoàn thiện chỉ vì có màn hình.

Kiểm tra .temp/ba-project.yaml; nếu chưa có thì đề xuất cấu hình để tôi xác nhận.
Chuẩn bị hồ sơ khảo sát dưới .temp và dừng để tôi xem danh mục.
```

**Kết quả mặc định:**

```text
.temp/exploration/project-exploration.json
.temp/exploration/project-exploration.md
.temp/exploration/exploration-brief.md
```

Mở **`project-exploration.md`** để đọc danh mục. Mỗi tính năng có ID dạng `EXF-001`, bằng chứng và mức xác minh. Xem phần chưa khảo sát/câu hỏi mở trước khi chọn phạm vi; một báo cáo khảo sát tĩnh chưa chứng minh ứng dụng chạy đúng trong thực tế.

Nếu thiếu phân hệ, phản hồi: “Dùng ba-explore-project khảo sát thêm [phân hệ], giữ IDs đã có, cập nhật báo cáo có kiểm soát và báo các xung đột trước khi ghi đè.”

## 2. Chuyển kết quả khảo sát thành yêu cầu và backlog

Sau khi đọc và chọn phạm vi, gửi:

```text
$ba-workflow
Tôi chọn tài liệu hóa [các EXF IDs hoặc tên phân hệ đã khảo sát].

Đọc .temp/exploration/exploration-brief.md cùng inventory và report.
Dùng kết quả đó làm đầu vào cho ba-brainstorm, rồi thực hiện
ba-requirements → ba-product-backlog.

Làm theo handoff guide của ba-explore-project để giữ bằng chứng,
mức xác minh và source fingerprints trong chuỗi tài liệu.
Mô tả hành vi hiện hữu; phần chưa rõ phải ghi câu hỏi hoặc giả định có nhãn.
Không biến các PBI này thành yêu cầu xây mới tính năng đã có.

Nếu đã có hồ sơ BA, đối chiếu và giữ ID/quyết định còn hiệu lực,
chỉ cập nhật phần được chọn, báo conflict trước khi thay đổi.
Dừng để tôi duyệt backlog.
```

Nếu cấu hình dùng planning_dir là thư mục con của `.temp`, thay đường dẫn brief tương ứng.

**Kết quả:** `.temp/brainstorm.md`, `requirements.md`, `product-backlog.md` và tiến độ trong `workflow-state.md`.

Mở **`product-backlog.md`** để kiểm tra: chức năng nào được đưa vào, PBI có trùng hoặc quá lớn không, có phần chưa được xác minh nhưng lại bị mô tả như đã hoạt động đầy đủ không. Xác nhận phạm vi khảo sát ở bước 1 chưa thay cho việc duyệt backlog này.

Nếu cần điều chỉnh, nói rõ PBI và nội dung cần sửa. Nếu thay đổi vượt yêu cầu đã phân tích, agent phải cập nhật nguồn liên quan trước khi chốt backlog.

## 3. Duyệt backlog và lập các đợt tài liệu hóa

Khi đã đồng ý với phiên bản backlog đang xem:

```text
Tôi duyệt backlog hiện tại cho phạm vi tài liệu hóa đã chọn.
Dùng ba-workflow tiếp tục bước ba-round-plan.

Đề xuất các Round theo phân hệ, dependency và mức độ sẵn sàng.
Đây là các đợt viết tài liệu, không phải lịch sử phát hành sản phẩm.
Nếu chưa có capacity/ước lượng, giữ kế hoạch Proposed, chưa cam kết khối lượng.
Dừng để tôi xem kế hoạch.
```

**Kết quả:** `.temp/round-plan.md`. Xem mục tiêu từng Round, các PBI được phân bổ và các mục còn chưa phân bổ. Không có số Round cố định; chưa cần viết mọi PBI trong một lượt.

## 4. Chọn PBI để viết business, spec và review

Sau khi xem kế hoạch:

```text
Tôi cho phép dùng kế hoạch Round hiện tại ở dạng Proposed để viết bản nháp,
chưa cam kết khối lượng.

Dùng ba-workflow tạo tài liệu cho PBI-001 và PBI-002 trong R1:
ba-business → ba-spec → ba-review, kiểm tra output giữa các bước.

Mô tả đúng hiện trạng với bằng chứng đã khảo sát. Giữ rõ phần chỉ có UI/mock,
chính sách chưa xác minh và các khác biệt giữa tài liệu với code.
Không tự thay hành vi đang có bằng giải pháp lý tưởng.
Dừng sau review, chưa publish.
```

Nếu đã có cơ sở và muốn duyệt kế hoạch chính thức, thay câu đầu bằng “Tôi duyệt kế hoạch Round hiện tại.” Chọn ID thật trong backlog/Round plan của bạn.

**Kết quả cho mỗi PBI:**

```text
.temp/drafts/PBI-001/business.md
.temp/drafts/PBI-001/spec.md
.temp/reviews/PBI-001-review.md
```

Đọc business để kiểm tra mục đích và phạm vi, đọc spec để kiểm tra hành vi và điều kiện nghiệm thu, rồi đọc review để biết điểm thiếu/mâu thuẫn.

## 5. Xử lý review trước khi bàn giao

| Kết quả | Cách xử lý |
| --- | --- |
| `PASS` | Có thể chuẩn bị dry-run; vẫn cần bạn cho phép xuất tài liệu. |
| `CONDITIONAL` | Đọc các finding còn mở; chỉ xuất draft nếu bạn cho phép rõ ràng. |
| `FAIL` | Giải quyết lỗi quan trọng hoặc quyết định còn thiếu, sửa và review lại trước khi xuất. |

Ví dụ phản hồi khi cần sửa:

```text
Dùng ba-workflow xử lý findings của PBI-001.
Quyết định/làm rõ của tôi: [ghi nội dung theo từng câu hỏi hoặc finding].
Sửa tài liệu trong phạm vi này, giữ ID và bằng chứng nguồn.
Dùng ba-review để kiểm tra lại và báo các vấn đề còn mở. Chưa publish.
```

Nếu không đủ bằng chứng để quyết định hành vi, giữ câu hỏi/blocker và nêu cần khảo sát hoặc hỏi ai; đừng điền một câu trả lời giả chỉ để review PASS.

## 6. Xem trước và cho phép xuất tài liệu

Trước tiên gửi:

```text
Dùng ba-publish tạo dry-run cho PBI-001 trong R1.
Kiểm nguồn, review, Round allocation và các quyết định phê duyệt.
Cho tôi xem file/đường dẫn sẽ xuất, file được bỏ qua và các xung đột.
Chưa ghi cặp tài liệu vào .specify.
```

**Dry-run** là xem trước, chưa xuất file. Khi đã đọc và đồng ý, nếu review PASS:

```text
Tôi cho phép publish cặp tài liệu hiện tại của PBI-001 vào R1
theo dry-run vừa trình bày. Dùng ba-publish để thực hiện và kiểm tra sau ghi.
```

Với CONDITIONAL, nếu bạn chấp nhận bản nháp, nói rõ: “Tôi cho phép Draft Publication cho cặp tài liệu hiện tại của PBI-001 theo dry-run; giữ trạng thái draft và các finding còn mở.” FAIL hoặc blocker chưa giải quyết phải được xử lý trước.

**Kết quả bàn giao:**

```text
your-project/
├── .temp/                         # Giữ toàn bộ hồ sơ làm việc và nguồn
└── .specify/
    └── R1/
        └── PBI-001-ten-tinh-nang/
            ├── business.md
            └── spec.md
```

Mỗi Round có thể chứa nhiều PBI; mỗi PBI xuất ra chỉ có đúng hai file đọc được. Spec có 18 mục theo [bố cục bàn giao](templates/spec-handover.md), bắt đầu bằng tên PBI; không có YAML front matter, BA-DATA, Contract Summary hoặc source hashes. Metadata nằm trong drafts dưới .temp. `.specify` không chứa exploration, backlog, review hoặc `_planning`. Đừng xóa `.temp` sau bàn giao vì truy vết nguồn và RESUME vẫn cần các hồ sơ đó.

## 7. Tiếp tục sau này hoặc bổ sung tính năng mới

Lần sau mở lại cùng project:

```text
$ba-workflow mode=RESUME project_config=./.temp/ba-project.yaml
Đọc state và các nguồn hiện tại, cho biết phần nào đã xong,
phần nào bị ảnh hưởng bởi thay đổi code và quyết định nào còn chờ tôi.
Tiếp tục phần hợp lệ trong phạm vi đã chọn.
```

Nếu báo `STALE_INPUT`, nguồn đã đổi từ lần tạo tài liệu trước. Yêu cầu đối chiếu source, cập nhật và review lại phần bị ảnh hưởng; không chỉ thay hash để bỏ cảnh báo. Nếu project còn layout cũ `.specify/_planning`, xử lý theo [quy trình chuyển layout](conventions/BA-CONVENTIONS.md#chuyển-dự-án-đang-dùng-layout-cũ) trước khi chạy tiếp.

Khi đã có hồ sơ nền và muốn **phát triển thêm** một tính năng, dùng skill riêng:

```text
$ba-pbi
Tạo một PBI mới cho tính năng [mô tả thay đổi].
Đối chiếu hiện trạng và backlog, giữ các PBI cũ, dừng để tôi duyệt scope.
Sau khi duyệt, viết business/spec và review cho PBI mới.
```

Đây là yêu cầu thay đổi sản phẩm, khác với việc tài liệu hóa các chức năng đang có ở các bước trên.
