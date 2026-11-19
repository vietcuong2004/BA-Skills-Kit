# Feature Specification: Bắt buộc khai báo vị trí linh kiện khi thêm mới linh kiện

**Feature Branch:** `626180-bat-buoc-khai-bao-vi-tri-linh-kien-khi-them-moi`  
**Created:** 2026-11-02  
**Status:** Draft  
**PBI:** 626180  
**Platform:** Web MISA AMIS  
**Vòng phát hành:** R55

**Link Figma:** https://www.figma.com/design/Y6YFH9EEXUdeoIO039Vmya/AMIS-Tai-san-R55 (bổ sung node sau)

## User Scenarios & Testing

### User Story 1 — Thêm mới linh kiện tình trạng Tồn kho, bắt buộc chọn vị trí (Priority: P1)

Là nhân viên quản lý kho, tôi muốn khi thêm mới linh kiện ở tình trạng **Tồn kho**, hệ thống bắt buộc tôi chọn vị trí linh kiện, để mỗi linh kiện tồn kho đều xác định được nơi lưu kho ngay từ khi khởi tạo.

**Why this priority:** Đây là thay đổi validate cốt lõi của PBI — đảm bảo dữ liệu vị trí đủ cho toàn bộ linh kiện nhập kho.

**Independent Test:** Vào Danh sách linh kiện → nhấn **Thêm mới linh kiện** → điền thông tin chung → chọn tình trạng **Tồn kho** → để trống trường **Vị trí linh kiện** → nhấn **Lưu** → kiểm tra hệ thống hiển thị lỗi “Vị trí linh kiện không được để trống” và không lưu. Chọn vị trí → nhấn Lưu → linh kiện được lưu với vị trí tương ứng.

**Acceptance Scenarios:**

1. **Given** form Thêm mới linh kiện đang mở, **When** người dùng chọn tình trạng **Tồn kho**, **Then** trường **Vị trí linh kiện** hiển thị ở dạng combobox chỉ chọn 1, đánh dấu bắt buộc (*), danh sách lấy các vị trí có trạng thái **Đang theo dõi**.
2. **Given** tình trạng = **Tồn kho**, **When** người dùng nhấn **Lưu** mà chưa chọn **Vị trí linh kiện**, **Then** hệ thống hiển thị lỗi tại trường: “Vị trí linh kiện không được để trống” và không cho lưu.
3. **Given** tình trạng = **Tồn kho**, **When** người dùng chọn đủ các trường bắt buộc trong đó có **Vị trí linh kiện** và nhấn **Lưu**, **Then** hệ thống lưu linh kiện thành công, đóng form, hiển thị Toast thông báo lưu thành công theo cơ chế hiện hành.
4. **Given** linh kiện quản lý theo số lượng, **When** người dùng thêm mới ở tình trạng **Tồn kho**, **Then** trường **Vị trí linh kiện** vẫn bắt buộc và validate giống linh kiện quản lý theo mã.

### User Story 2 — Thêm mới linh kiện tình trạng Lắp vào tài sản, bắt buộc khai báo vị trí linh kiện (Priority: P1)

Là nhân viên quản lý kho, tôi muốn khi thêm mới linh kiện ở tình trạng **Lắp vào tài sản**, hệ thống hiển thị trường **Vị trí linh kiện** dạng combobox lấy tất cả vị trí có trạng thái **Đang theo dõi** trên hệ thống và bắt buộc chọn, để linh kiện luôn được gắn với một vị trí xác định ngay khi thêm mới.

**Why this priority:** Bảo đảm mọi linh kiện lắp vào tài sản đều được khai báo vị trí, không phát sinh linh kiện thiếu vị trí.

**Independent Test:** Vào form **Thêm mới linh kiện** → chọn tình trạng **Lắp vào tài sản** → kiểm tra trường **Vị trí linh kiện** xuất hiện ngay dưới trường **Tài sản** ở dạng combobox, danh sách lấy tất cả vị trí có trạng thái **Đang theo dõi** trên hệ thống → để trống trường vị trí và nhấn **Lưu** → kiểm tra hệ thống hiển thị lỗi “Vị trí linh kiện không được để trống” và không lưu. Chọn một vị trí → nhấn **Lưu** → linh kiện được lưu với vị trí đã chọn.

**Acceptance Scenarios:**

1. **Given** form Thêm mới linh kiện đang mở, **When** người dùng chọn tình trạng **Lắp vào tài sản**, **Then** trường **Tài sản** hiển thị, bắt buộc nhập như quy tắc hiện hành; trường **Vị trí linh kiện** hiển thị ngay dưới trường **Tài sản** ở dạng combobox chỉ chọn 1, đánh dấu bắt buộc (*), danh sách lấy tất cả vị trí có trạng thái **Đang theo dõi** trên hệ thống.
2. **Given** tình trạng = **Lắp vào tài sản**, **When** người dùng nhấn **Lưu** mà chưa chọn **Vị trí linh kiện**, **Then** hệ thống hiển thị lỗi tại trường: “Vị trí linh kiện không được để trống” và không cho lưu.
3. **Given** tình trạng = **Lắp vào tài sản** với đủ các trường bắt buộc, **When** người dùng nhấn **Lưu**, **Then** hệ thống lưu linh kiện thành công; vị trí linh kiện được ghi nhận bằng vị trí người dùng chọn trên form.
4. **Given** linh kiện quản lý theo số lượng, **When** người dùng thêm mới ở tình trạng **Lắp vào tài sản**, **Then** trường **Vị trí linh kiện** vẫn hiển thị dạng combobox, bắt buộc và validate giống linh kiện quản lý theo mã.

### User Story 3 — Thêm hàng loạt linh kiện, vị trí bắt buộc trên từng dòng (Priority: P1)

Là nhân viên quản lý kho, tôi muốn khi thêm hàng loạt linh kiện (quản lý theo mã), trường **Vị trí linh kiện** trên từng dòng bắt buộc nhập, để toàn bộ linh kiện thêm hàng loạt đều có vị trí lưu kho.

**Why this priority:** Bảo đảm dữ liệu vị trí đủ ngay cả khi nhập nhiều linh kiện cùng lúc.

**Independent Test:** Vào Danh sách linh kiện → mở form **Thêm hàng loạt linh kiện** → điền các dòng linh kiện mà để trống trường **Vị trí linh kiện** → nhấn **Lưu** → kiểm tra hệ thống hiển thị lỗi “Vị trí linh kiện không được để trống” tại từng dòng thiếu vị trí và không lưu. Chọn đủ vị trí cho mọi dòng → nhấn **Lưu** → lưu thành công.

**Acceptance Scenarios:**

> Phần nội dung Acceptance Scenarios của User Story 3 bị cắt ở ảnh chụp, cần đối chiếu file gốc để bổ sung chính xác.

> **Các phần không xuất hiện đầy đủ trong 5 ảnh:** User Story 4 và các User Stories tiếp theo (nếu có); một phần Functional Requirements (từ FR-008 trở đi hoặc các mục nằm ngoài vùng chụp). Không tự bổ sung yêu cầu chưa xác minh.

## Edge Cases

- **Tài sản được chọn bị xóa hoặc thay đổi vị trí trong lúc mở form:** vị trí linh kiện do người dùng chọn nên không bị ảnh hưởng; khi nhấn **Lưu**, hệ thống kiểm tra lại tài sản theo cơ chế hiện hành.
- **Nhấn Hủy khi đang điền form:** đóng form, không lưu dữ liệu, không thay đổi gì.
- **Linh kiện quản lý theo số lượng:** áp dụng cùng quy tắc vị trí; các trường Số lượng, Đơn giá, Thành tiền validate theo quy tắc hiện hành của PBI 681759.
- **Form sửa thông tin linh kiện:** trường **Vị trí linh kiện** luôn hiển thị như tại form thêm mới — cho phép chỉnh sửa nếu linh kiện được thêm mới và lắp luôn vào tài sản (cập nhật xuống bảng **Quá trình sử dụng** tương ứng), không cho phép chỉnh sửa nếu linh kiện được thêm mới trước rồi mới lắp vào tài sản.
- **Nhập khẩu linh kiện:** trường **Mã vị trí linh kiện** trên file mẫu luôn bắt buộc nhập — xem User Story 4 và FR-011.

## Requirements

### Functional Requirements

- **FR-001:** Tại form **Thêm mới linh kiện**, mục **Thông tin tình trạng**, khi người dùng chọn tình trạng **Tồn kho**, hệ thống PHẢI đánh dấu trường **Vị trí linh kiện** là bắt buộc (*). Trường là combobox chỉ chọn 1, danh sách lấy các vị trí có trạng thái **Đang theo dõi**.
- **FR-002:** Khi người dùng nhấn **Lưu** với tình trạng **Tồn kho** mà chưa chọn **Vị trí linh kiện**, hệ thống PHẢI hiển thị lỗi tại trường: “Vị trí linh kiện không được để trống” và không cho lưu.
- **FR-003:** Khi người dùng chọn tình trạng **Lắp vào tài sản**, hệ thống PHẢI hiển thị trường **Tài sản** (bắt buộc) theo quy tắc hiện hành; đồng thời hiển thị trường **Vị trí linh kiện** ngay dưới trường **Tài sản** ngay khi chọn tình trạng, không phụ thuộc vào việc đã chọn tài sản hay chưa.
- **FR-004:** Trường **Vị trí linh kiện** (trường hợp **Lắp vào tài sản**) PHẢI ở dạng combobox chỉ chọn 1, đánh dấu bắt buộc (*), danh sách lấy lên tất cả vị trí có trạng thái **Đang theo dõi** trên hệ thống; giá trị mặc định để trống.
- **FR-005:** Giá trị trường **Vị trí linh kiện** do người dùng chọn. Khi nhấn **Lưu** mà chưa chọn **Vị trí linh kiện**, hệ thống PHẢI hiển thị lỗi “Vị trí linh kiện không được để trống” và không cho lưu.
- **FR-006:** Việc tài sản được chọn có khai báo vị trí hay chưa KHÔNG ảnh hưởng đến giá trị và validate của trường **Vị trí linh kiện**; trường này luôn bắt buộc nhập ở tình trạng **Lắp vào tài sản**.
- **FR-007:** Sau khi lưu thành công, hệ thống PHẢI ghi nhận vị trí linh kiện theo giá trị trên form tại thời điểm lưu:
  - Tình trạng **Tồn kho** → vị trí theo trường **Vị trí linh kiện** người dùng chọn.
  - Tình trạng **Lắp vào tài sản** → vị trí theo trường **Vị trí linh kiện** người dùng chọn.

> Phần tiếp theo của Functional Requirements không hiển thị đầy đủ trong ảnh. Ảnh có nhắc tới **FR-011** nhưng không có nội dung nguyên văn của yêu cầu này.

### Non-Functional Requirements

- **NFR-001:** Thời gian tải danh sách vị trí (các vị trí **Đang theo dõi** trên hệ thống) và giá trị vị trí hiện tại của linh kiện PHẢI đáp ứng trải nghiệm nhập form thông thường, không gây giật khi chuyển tình trạng.
- **NFR-002:** Thông báo lỗi validate hiển thị tại trường theo pattern validate chung của hệ thống.

## Success Criteria

- Linh kiện thêm mới ở tình trạng **Tồn kho** luôn có vị trí — không thể lưu khi để trống trường **Vị trí linh kiện**.
- Linh kiện thêm mới ở tình trạng **Lắp vào tài sản** luôn hiển thị trường **Vị trí linh kiện** dưới trường **Tài sản** dạng combobox lấy tất cả vị trí có trạng thái **Đang theo dõi** trên hệ thống, bắt buộc chọn — không thể lưu khi để trống.
- Chuyển đổi qua lại giữa hai tình trạng không để sót giá trị của tình trạng cũ.
- Vị trí linh kiện sau lưu hiển thị đúng trong bảng **Quá trình sử dụng** và form xem chi tiết linh kiện.
- Áp dụng cho cả linh kiện quản lý theo mã và quản lý theo số lượng.
- Trường **Vị trí linh kiện** trên từng dòng form **Thêm hàng loạt linh kiện** (quản lý theo mã) bắt buộc nhập — không thể lưu khi có dòng để trống.
- Trường **Mã vị trí linh kiện** trên file mẫu nhập khẩu luôn bắt buộc nhập với mọi dòng dữ liệu.
- Form **Sửa thông tin linh kiện** hiển thị trường **Vị trí linh kiện** như form thêm mới; linh kiện thêm mới và lắp luôn vào tài sản thì sửa được và cập nhật xuống bảng **Quá trình sử dụng**, linh kiện lắp vào tài sản sau khi thêm mới thì chỉ đọc.

## Assumptions

- Trường **Vị trí linh kiện** tại form **Thêm mới linh kiện** hiện là không bắt buộc với tình trạng **Tồn kho** và không hiển thị với tình trạng **Lắp vào tài sản** — PBI này thay đổi hai hành vi đó.
- Danh sách vị trí ở cả hai tình trạng **Tồn kho** và **Lắp vào tài sản** đều lấy các vị trí có trạng thái **Đang theo dõi** trên hệ thống.
- Trường hợp tài sản chưa khai báo vị trí không ảnh hưởng đến trường **Vị trí linh kiện** — người dùng vẫn phải chọn vị trí.
- Form **Thêm hàng loạt linh kiện** chỉ áp dụng với linh kiện quản lý theo mã.

## Dependencies

- **PBI 681759 — Quản lý linh kiện theo mã hoặc số lượng:** cấu trúc form Thêm mới linh kiện, cách quản lý theo mã/số lượng, bảng Chi tiết linh kiện.
- **PBI 622753 — Bảo dưỡng linh kiện; PBI 621821 — Sửa chữa linh kiện:** pattern bảng Quá trình sử dụng của linh kiện.
- **Danh mục vị trí hiện có:** nguồn danh sách vị trí **Đang theo dõi**.
