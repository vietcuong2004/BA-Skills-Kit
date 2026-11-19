# Hướng dẫn viết tài liệu `spec.md`

> **Mục đích:** Quy chuẩn để BA hoặc AI Agent xây dựng tài liệu Feature Specification (`spec.md`) đủ các phần, rõ yêu cầu, có thể triển khai và kiểm thử.
>
> **Nguồn tham chiếu:** `spec.md` của PBI 626180 – *Bắt buộc khai báo vị trí linh kiện khi thêm mới linh kiện* (R55).
>
> **Lưu ý:** Đây là hướng dẫn biên soạn dựa trên cấu trúc file tham chiếu, không phải quy định chính thức của tổ chức. Các ví dụ lấy từ file tham chiếu; các nguyên tắc kiểm tra và biểu mẫu là phần hướng dẫn được bổ sung.

## 1. Mục tiêu và nguyên tắc chung

`spec.md` mô tả **hệ thống phải làm gì**, trong hoàn cảnh nào, người dùng nhận được kết quả gì và cách xác nhận yêu cầu đã hoàn thành. Tài liệu là cơ sở để Dev phát triển, QC thiết kế test case và BA/PO nghiệm thu.

- Chỉ viết yêu cầu có căn cứ từ PBI, mô tả nghiệp vụ, UI/Figma đã duyệt hoặc quy tắc hiện hành đã xác minh.
- Không tự suy đoán giá trị mặc định, thông báo lỗi, trạng thái, giới hạn, phân quyền hay hành vi chưa được xác nhận.
- Dùng tên màn hình, trường, nút, trạng thái thống nhất; nêu rõ điều kiện, hành động và kết quả.
- Đánh mã yêu cầu ổn định (`FR-001`, `NFR-001`); các yêu cầu phải có khả năng kiểm thử.
- Nếu thiếu thông tin, ghi **[CẦN XÁC NHẬN]** tại đúng vị trí, không âm thầm điền giả định thành sự thật.
- Không coi việc một mục xuất hiện trong mẫu là bằng chứng mọi PBI đều phải có cùng số lượng User Story hoặc FR.

## 2. Cấu trúc đầy đủ của `spec.md`

| Thứ tự | Phần | Mức độ | Nội dung chính |
|---|---|---|---|
| 1 | Feature Specification và metadata | Bắt buộc | Tên tính năng, PBI, nhánh, ngày, trạng thái, nền tảng, vòng phát hành, Figma nếu có |
| 2 | User Scenarios & Testing | Bắt buộc | User Stories, độ ưu tiên, lý do ưu tiên, Independent Test, Acceptance Scenarios |
| 3 | Edge Cases | Bắt buộc rà soát | Các tình huống biên và hành vi xử lý; nếu không có phải nêu đã rà soát |
| 4 | Requirements / Functional Requirements | Bắt buộc | Các quy tắc chức năng đánh mã FR |
| 5 | Requirements / Non-Functional Requirements | Bắt buộc rà soát | Hiệu năng, trải nghiệm, bảo mật, tính nhất quán... nếu áp dụng |
| 6 | Success Criteria | Bắt buộc | Điều kiện xác nhận PBI đạt mục tiêu |
| 7 | Assumptions | Bắt buộc rà soát | Những giả định đang sử dụng, cần xác minh nếu chưa chắc chắn |
| 8 | Dependencies | Bắt buộc rà soát | PBI, danh mục, dữ liệu, API, quy tắc hiện hành liên quan |
| 9 | Kiểm tra tính đầy đủ và nhất quán | Bước kiểm soát chất lượng | Đối chiếu Story–AC–FR–Success Criteria, không nhất thiết là heading trong file đầu ra |

## 3. Hướng dẫn chi tiết từng phần

### 3.1. Tiêu đề và metadata

**Mục đích:** Xác định chính xác tài liệu thuộc PBI/tính năng và phiên bản phát triển nào.

Dùng định dạng:

```md
# Feature Specification: <Tên tính năng>

**Feature Branch:** `<mã-PBI>-<ten-tinh-nang-kebab-case>`  
**Created:** YYYY-MM-DD  
**Status:** Draft | In Review | Approved  
**PBI:** <Mã PBI>  
**Platform:** <Nền tảng>  
**Vòng phát hành:** <Round>

**Link Figma:** <URL hoặc [CHƯA CÓ]>
```

**Ví dụ tham chiếu:** PBI `626180`, R55, Web MISA AMIS, trạng thái Draft. Không tự tạo URL Figma hoặc node chưa có.

**Kiểm tra:** Tên tính năng khớp PBI; mã PBI và Round đúng; không để metadata mâu thuẫn.

### 3.2. User Scenarios & Testing

Mỗi **User Story** phải mô tả một mục tiêu sử dụng hoặc một nhóm hành vi có thể kiểm thử độc lập. Tách story khi khác luồng, khác điều kiện nghiệp vụ hoặc khác cách xác nhận kết quả (ví dụ thêm mới Tồn kho, Lắp vào tài sản, thêm hàng loạt, nhập khẩu).

#### 3.2.1. Tiêu đề và độ ưu tiên

```md
### User Story N — <Hành vi và điều kiện> (Priority: P1)
```

Ưu tiên phản ánh mức độ cần thiết của story; không mặc định tất cả đều P1. File tham chiếu dùng P1 cho các story hiển thị.

#### 3.2.2. Câu chuyện người dùng

Dùng mẫu: **Là [vai trò], tôi muốn [hành động/khả năng], để [giá trị hoặc mục tiêu nghiệp vụ].**

Ví dụ:

> Là nhân viên quản lý kho, tôi muốn khi thêm mới linh kiện ở tình trạng **Tồn kho**, hệ thống bắt buộc tôi chọn vị trí linh kiện, để mỗi linh kiện tồn kho đều xác định được nơi lưu kho ngay từ khi khởi tạo.

Không viết chung chung như “Là người dùng, tôi muốn hệ thống hoạt động tốt”.

#### 3.2.3. Why this priority

Giải thích **vì sao** story có mức ưu tiên đã chọn, dựa vào rủi ro nghiệp vụ, dữ liệu, tính phụ thuộc hoặc tác động đến luồng chính.

Ví dụ: “Đây là thay đổi validate cốt lõi của PBI — đảm bảo dữ liệu vị trí đủ cho toàn bộ linh kiện nhập kho.”

#### 3.2.4. Independent Test

Viết một kịch bản kiểm thử đầu-cuối có thể chạy riêng, gồm:

1. Điểm bắt đầu (màn hình hoặc điều kiện chuẩn bị).
2. Thao tác người dùng theo thứ tự.
3. Dữ liệu/điều kiện quan trọng.
4. Kết quả kỳ vọng ở nhánh không hợp lệ và nhánh hợp lệ, nếu áp dụng.

Ví dụ rút gọn: Mở **Thêm mới linh kiện** → chọn **Tồn kho** → để trống **Vị trí linh kiện** → **Lưu** → hiển thị lỗi và không lưu; chọn vị trí hợp lệ → **Lưu** → lưu thành công.

Independent Test không thay thế Acceptance Scenarios chi tiết.

#### 3.2.5. Acceptance Scenarios (Given–When–Then)

Mỗi scenario phải kiểm tra được một hành vi xác định:

- **Given:** Bối cảnh, dữ liệu hoặc trạng thái ban đầu.
- **When:** Hành động hoặc sự kiện kích hoạt.
- **Then:** Kết quả quan sát được, bao gồm UI, validate, lưu dữ liệu hoặc điều hướng nếu có căn cứ.

Ví dụ:

```md
**Acceptance Scenarios:**

1. **Given** form Thêm mới linh kiện đang mở,
   **When** người dùng chọn tình trạng **Tồn kho**,
   **Then** trường **Vị trí linh kiện** là combobox chỉ chọn 1,
   đánh dấu bắt buộc (*), danh sách gồm các vị trí **Đang theo dõi**.
2. **Given** tình trạng = **Tồn kho**,
   **When** người dùng nhấn **Lưu** mà chưa chọn **Vị trí linh kiện**,
   **Then** hệ thống hiển thị lỗi “Vị trí linh kiện không được để trống”
   tại trường và không cho lưu.
```

**Các nhóm scenario cần rà soát:** hiển thị và điều kiện xuất hiện; giá trị mặc định/nguồn dữ liệu; nhập hợp lệ; nhập thiếu/sai; thay đổi trạng thái; lưu và kết quả sau lưu; thao tác hủy; các biến thể đối tượng (theo mã/theo số lượng); trường hợp phụ thuộc. Chỉ đưa vào các nhóm áp dụng cho tính năng.

**Kiểm tra:** Không dùng Then mơ hồ (“hoạt động đúng”); không ghép nhiều luồng không liên quan; không có AC mâu thuẫn với FR.

### 3.3. Edge Cases

**Mục đích:** Ghi rõ hệ thống xử lý các tình huống ít gặp nhưng có ảnh hưởng đến dữ liệu hoặc trải nghiệm.

Rà soát: dữ liệu liên quan bị xóa/sửa trong khi form mở; Hủy khi chưa lưu; chuyển trạng thái; dữ liệu rỗng/không hợp lệ; khác biệt theo loại đối tượng; sửa sau khi tạo; thêm hàng loạt/nhập khẩu; lỗi hoặc thay đổi dữ liệu nguồn.

**Ví dụ từ file tham chiếu:** Khi tài sản được chọn bị xóa hoặc thay đổi vị trí trong lúc mở form, vị trí linh kiện người dùng chọn không bị ảnh hưởng; khi Lưu, hệ thống kiểm tra lại tài sản theo cơ chế hiện hành.

Mỗi edge case nên nêu **điều kiện → hành vi xử lý → kết quả**. Không phát minh cơ chế xử lý lỗi khi chưa có xác nhận.

### 3.4. Requirements — Functional Requirements

**Mục đích:** Đặc tả các quy tắc mà hệ thống **PHẢI** đáp ứng, đủ rõ để Dev triển khai và QC kiểm tra.

Mẫu:

```md
## Requirements

### Functional Requirements

- **FR-001:** Khi <điều kiện>, tại <màn hình/vị trí>,
  hệ thống PHẢI <hành vi cụ thể>, với <nguồn dữ liệu/quy tắc>.
- **FR-002:** Khi <hành động không hợp lệ>,
  hệ thống PHẢI <thông báo/vị trí lỗi> và <ngăn hoặc cho phép thao tác>.
```

**Ví dụ tham chiếu:**

- **FR-001:** Ở form Thêm mới linh kiện, khi chọn **Tồn kho**, trường **Vị trí linh kiện** phải bắt buộc, là combobox chọn một và lấy các vị trí **Đang theo dõi**.
- **FR-002:** Khi nhấn **Lưu** mà chưa chọn vị trí ở tình trạng **Tồn kho**, phải báo lỗi tại trường và không cho lưu.

Với từng trường hoặc hành vi, rà soát các thuộc tính sau nếu áp dụng: vị trí trên UI; điều kiện hiển thị/ẩn; kiểu điều khiển; bắt buộc/không bắt buộc; giá trị mặc định; danh sách và bộ lọc; cho phép chỉnh sửa; quy tắc validate; thông báo lỗi; thời điểm kiểm tra; hành vi Lưu/Hủy; dữ liệu được ghi nhận; ảnh hưởng đến màn hình/bảng liên quan.

**Nguyên tắc đánh mã:** mỗi FR có một mã duy nhất, không bỏ sót tham chiếu; khi chỉnh sửa không tự ý đổi mã làm hỏng liên kết với AC/test case. Nếu viện dẫn quy tắc hiện hành, ghi rõ PBI hoặc tài liệu nguồn khi biết.

**Phân biệt AC và FR:** AC mô tả tình huống có thể kiểm chứng theo Given–When–Then; FR mô tả quy tắc chức năng chuẩn tắc. Một FR có thể được xác minh bởi nhiều AC và ngược lại.

### 3.5. Requirements — Non-Functional Requirements

**Mục đích:** Nêu chất lượng và ràng buộc vận hành của chức năng, không phải thao tác nghiệp vụ.

Mẫu:

```md
### Non-Functional Requirements

- **NFR-001:** <Yêu cầu về hiệu năng/trải nghiệm, điều kiện áp dụng,
  tiêu chí đánh giá nếu đã được xác nhận>.
- **NFR-002:** <Yêu cầu nhất quán UI, bảo mật, khả năng sử dụng...>.
```

**Ví dụ tham chiếu:** danh sách vị trí phải tải đủ mượt khi chuyển tình trạng; lỗi validate hiển thị tại trường theo pattern chung của hệ thống.

**Khuyến nghị bổ sung:** Nếu cần tiêu chí định lượng (ví dụ thời gian phản hồi), phải lấy từ nguồn đã duyệt; không tự đặt con số. Kiểm tra bảo mật, phân quyền, tính sẵn sàng, khả năng truy cập chỉ khi có liên quan.

### 3.6. Success Criteria

**Mục đích:** Xác định các kết quả tổng thể để đánh giá PBI đã hoàn thành, không chỉ một thao tác riêng lẻ.

Viết thành các mệnh đề có thể xác minh: dữ liệu đúng sau lưu; không lưu được khi thiếu dữ liệu bắt buộc; hiển thị đúng khi chuyển trạng thái; các luồng thêm mới, hàng loạt, nhập khẩu, sửa được bao phủ theo phạm vi đã duyệt.

**Ví dụ tham chiếu:** “Linh kiện thêm mới ở tình trạng **Tồn kho** luôn có vị trí — không thể lưu khi để trống trường **Vị trí linh kiện**.”

Đối chiếu Success Criteria với toàn bộ story và FR; không thêm mục tiêu mới chưa xuất hiện trong phạm vi yêu cầu.

### 3.7. Assumptions

**Mục đích:** Minh bạch những tiền đề được dùng để xây dựng đặc tả.

Ví dụ từ file tham chiếu: trường vị trí hiện không bắt buộc với **Tồn kho** và không hiển thị với **Lắp vào tài sản**; PBI thay đổi hai hành vi này.

Phân biệt:

- **Đã xác minh:** ghi rõ tiền đề và nguồn.
- **Chưa xác minh:** đánh dấu **[CẦN XÁC NHẬN]**, nêu câu hỏi cần làm rõ.

Không biến một giả định thành FR bắt buộc nếu chưa được xác nhận.

### 3.8. Dependencies

**Mục đích:** Cho biết chức năng phụ thuộc vào yêu cầu, cấu trúc, nguồn dữ liệu hay quy tắc nào.

Ví dụ tham chiếu:

- **PBI 681759:** Quản lý linh kiện theo mã hoặc số lượng; cấu trúc form và bảng chi tiết.
- **PBI 622753 / 621821:** Pattern bảng Quá trình sử dụng.
- **Danh mục vị trí hiện có:** nguồn các vị trí **Đang theo dõi**.

Với mỗi dependency, nêu **tên/mã → nội dung phụ thuộc → tác động**. Nếu phụ thuộc chưa rõ phiên bản hoặc trạng thái, ghi cần xác minh.

## 4. Quy trình viết `spec.md` từ đầu đến cuối

1. **Thu thập nguồn:** PBI, `business.md`, UI/Figma, quy tắc hiện hành, PBI liên quan; ghi rõ nguồn nào chưa có.
2. **Xác định phạm vi:** tính năng thay đổi gì, ở màn hình nào, cho loại đối tượng nào; phân biệt trong/ngoài phạm vi.
3. **Tách User Stories:** theo mục tiêu, luồng hoặc điều kiện nghiệp vụ độc lập.
4. **Viết story và ưu tiên:** vai trò–mong muốn–giá trị; lý do ưu tiên.
5. **Viết Independent Test:** một luồng chạy độc lập để chứng minh story.
6. **Viết Acceptance Scenarios:** bao phủ các hành vi chính, validate, lưu và biến thể liên quan.
7. **Rà soát Edge Cases:** dữ liệu thay đổi, chuyển trạng thái, hủy, sửa, nhập khẩu/hàng loạt nếu có.
8. **Đặc tả FR/NFR:** mã duy nhất, câu chữ chính xác, có căn cứ và kiểm thử được.
9. **Viết Success Criteria, Assumptions, Dependencies:** kết quả tổng thể, tiền đề và các ràng buộc.
10. **Đối chiếu và duyệt:** đảm bảo không thiếu phần, không mâu thuẫn, không tự thêm nghiệp vụ.

## 5. Ma trận truy vết yêu cầu (khuyến nghị bổ sung)

Ma trận này là **công cụ kiểm tra**, không phải heading có sẵn trong file `spec.md` tham chiếu.

| User Story | Acceptance Scenarios | Functional Requirements | Success Criteria | Trạng thái |
|---|---|---|---|---|
| US1 – Thêm mới Tồn kho | AC của US1 | FR-001, FR-002, FR-007 | Bắt buộc có vị trí khi Tồn kho | Có thể đối chiếu |
| US2 – Lắp vào tài sản | AC của US2 | FR-003 đến FR-007 | Bắt buộc có vị trí khi lắp vào tài sản | Có thể đối chiếu |
| US3 – Thêm hàng loạt | Chưa đủ ảnh nguồn | Chưa đủ ảnh nguồn | Mỗi dòng bắt buộc vị trí | CẦN BỔ SUNG |
| US4 – Nhập khẩu | Chưa đủ ảnh nguồn | Có tham chiếu FR-011, thiếu nguyên văn | Mã vị trí trên file mẫu bắt buộc | CẦN BỔ SUNG |

**Chú ý:** Ma trận trên chỉ phản ánh thông tin nhìn thấy trong file tham chiếu; không suy ra toàn bộ các FR bị thiếu.

## 6. Checklist kiểm tra trước khi bàn giao

### A. Cấu trúc

- [ ] Có tiêu đề và đầy đủ metadata đã biết.
- [ ] Có `User Scenarios & Testing` và các User Story thuộc phạm vi PBI.
- [ ] Mỗi story có Priority, câu chuyện người dùng, Why this priority, Independent Test, Acceptance Scenarios.
- [ ] Có Edge Cases hoặc ghi rõ kết quả rà soát.
- [ ] Có Functional Requirements đánh mã liên tục, duy nhất.
- [ ] Có Non-Functional Requirements hoặc ghi rõ không áp dụng và lý do.
- [ ] Có Success Criteria, Assumptions, Dependencies (hoặc kết quả rà soát tương ứng).

### B. Nội dung nghiệp vụ

- [ ] Tên trường, trạng thái, màn hình, nút thống nhất với nguồn.
- [ ] Có điều kiện hiển thị, kiểu dữ liệu, nguồn dữ liệu, mặc định, bắt buộc và validate khi áp dụng.
- [ ] Có hành vi lưu, không lưu, hủy, chuyển trạng thái và kết quả sau lưu khi áp dụng.
- [ ] Có cả trường hợp thành công và lỗi quan trọng.
- [ ] Đã xét các biến thể trong phạm vi (ví dụ theo mã/theo số lượng, thêm đơn lẻ/hàng loạt/nhập khẩu).
- [ ] Không tự tạo thông báo lỗi, quy tắc hay số liệu chưa được xác nhận.

### C. Tính kiểm thử và nhất quán

- [ ] Mỗi Acceptance Scenario có Given, When, Then rõ ràng.
- [ ] Mỗi FR có thể kiểm chứng và có AC/test tương ứng hoặc ghi lý do chưa có.
- [ ] Success Criteria không mâu thuẫn với FR và AC.
- [ ] Các dependency và assumption ảnh hưởng đến chức năng đã được nêu.
- [ ] Không còn placeholder không được đánh dấu hoặc đoạn bị cắt được trình bày như nội dung đã xác minh.

## 7. Template `spec.md` để sao chép

```md
# Feature Specification: <Tên tính năng>

**Feature Branch:** `<branch>`  
**Created:** <YYYY-MM-DD>  
**Status:** <Draft/In Review/Approved>  
**PBI:** <Mã PBI>  
**Platform:** <Nền tảng>  
**Vòng phát hành:** <Round>

**Link Figma:** <Link hoặc [CHƯA CÓ]>

## User Scenarios & Testing

### User Story 1 — <Tên story> (Priority: <P1/P2/P3>)

Là <vai trò>, tôi muốn <khả năng>, để <giá trị>.

**Why this priority:** <Lý do>

**Independent Test:** <Điểm bắt đầu → thao tác → kết quả>

**Acceptance Scenarios:**

1. **Given** <bối cảnh>, **When** <hành động>, **Then** <kết quả>.
2. **Given** <bối cảnh lỗi>, **When** <hành động>, **Then** <thông báo và cách xử lý>.

<!-- Lặp lại User Story cho các luồng khác trong phạm vi -->

## Edge Cases

- **<Tình huống>:** <Hành vi xử lý và kết quả>.

## Requirements

### Functional Requirements

- **FR-001:** <Điều kiện → hệ thống PHẢI làm gì → kết quả>.
- **FR-002:** <Quy tắc chức năng tiếp theo>.

### Non-Functional Requirements

- **NFR-001:** <Yêu cầu chất lượng và điều kiện áp dụng>.

## Success Criteria

- <Kết quả có thể xác minh 1>.
- <Kết quả có thể xác minh 2>.

## Assumptions

- <Tiền đề đã xác minh hoặc [CẦN XÁC NHẬN]>.

## Dependencies

- **<PBI/danh mục/hệ thống>:** <Nội dung phụ thuộc>.
```

## 8. Quy tắc dành cho AI Agent khi tự sinh `spec.md`

1. **Đọc nguồn trước:** không tạo story, FR, thông báo lỗi hoặc điều kiện chỉ vì chúng “thường có” ở sản phẩm tương tự.
2. **Bảo toàn phạm vi:** mọi story và FR phải truy được về nguồn nghiệp vụ/UI/PBI hoặc được đánh dấu cần xác nhận.
3. **Không bỏ sót biến thể:** lập danh sách luồng và trạng thái trước khi viết story.
4. **Không lặp yêu cầu vô ích:** dùng AC để kiểm thử hành vi, FR để đặc tả quy tắc; giữ thuật ngữ đồng nhất.
5. **Kiểm tra liên kết:** truy vết Story → AC → FR → Success Criteria; phát hiện mục không được bao phủ.
6. **Không che giấu thiếu dữ liệu:** nếu nguồn bị cắt hoặc không đọc được, đánh dấu vị trí thiếu, không điền nội dung đoán.
7. **Xuất đúng định dạng:** file Markdown UTF-8 tên `spec.md`; dùng heading và mã FR/NFR ổn định; không tự sửa tài liệu nguồn.
8. **Báo cáo phần chưa hoàn chỉnh:** cuối quá trình tạo, liệt kê các điểm `[CẦN XÁC NHẬN]` để BA xử lý trước khi duyệt.

## 9. Những thiếu hụt đã phát hiện trong `spec.md` tham chiếu

File tham chiếu hiện tại được tạo từ ảnh chụp nên **chưa phải một mẫu đầy đủ về nội dung**:

- Acceptance Scenarios của User Story 3 bị cắt.
- User Story 4 được nhắc đến nhưng không có nội dung nguyên văn.
- Functional Requirements chỉ có FR-001 đến FR-007; nội dung FR-008 trở đi, trong đó có FR-011 được nhắc đến, chưa có.
- Một số Success Criteria đề cập nhập khẩu và sửa linh kiện nhưng không đủ story/FR tương ứng để đối chiếu trọn vẹn.

**Cách xử lý:** Giữ các nội dung đã xác minh, ghi rõ phần thiếu, yêu cầu bổ sung file gốc hoặc ảnh đầy đủ trước khi tuyên bố đặc tả đã hoàn tất.
