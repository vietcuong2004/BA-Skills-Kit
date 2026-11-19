# Đặc tả yêu cầu nghiệp vụ

## Nhập khẩu thêm mới tài sản — Quy định lại cách nhập khẩu các trường mở rộng

**PBI:** 692956  
**Vòng lặp:** R55

## 1. Mục đích

Khi muốn quy định lại cách nhập khẩu các **trường mở rộng** trong tệp mẫu nhập khẩu thêm mới tài sản: mỗi kiểu trường mở rộng có cách nhập và kiểm tra dữ liệu riêng, thay vì nhập tự do như hiện tại — đảm bảo dữ liệu nhập khẩu lên phần mềm đúng định dạng, đúng danh sách giá trị đã thiết lập.

## 2. Nghiệp vụ

**Câu chuyện nghiệp vụ:** Trường mở rộng là các trường do KH tự thiết lập trên phần mềm để bổ sung thông tin tài sản theo đặc thù đơn vị. Mỗi trường được khai báo theo một kiểu: một dòng, nhiều dòng, đường dẫn, ngày, tháng, số, tiền tệ, số thập phân, phần trăm, chọn một, tích chọn, chọn nhiều, nhân viên, tổ chức. Trên tệp mẫu nhập khẩu thêm mới tài sản, các cột trường mở rộng hiện tại đều cho nhập tự do — không ràng buộc theo kiểu trường. Vì vậy khi nhập khẩu, KH dễ nhập sai định dạng (ngày, sai số âm, số thập phân thừa chữ số), sai danh sách giá trị (chọn một/chọn nhiều), sai nhân viên/phòng ban — dẫn đến dữ liệu sai lệch hoặc đồng bộ lỗi phải sửa lại tay sau khi nhập khẩu.

**Khó khăn:**

- Các cột trường mở rộng trên tệp mẫu nhập khẩu không phân biệt kiểu trường — đều nhập tự do.
- Dữ liệu nhập sai định dạng hoặc sai danh sách giá trị chỉ phát hiện sau khi nhập khẩu — KH phải sửa lại từng dòng.
- Với trường kiểu chọn một, chọn nhiều, tích chọn, nhân viên, tổ chức nhập tự do không đảm bảo giá trị khớp với dữ liệu đã thiết lập trên phần mềm.

**Nhu cầu KH:**

- Quy định lại cách nhập cho từng kiểu trường mở rộng trên tệp mẫu nhập khẩu thêm mới tài sản: kiểu nhập (tự do/combobox), định dạng dữ liệu, và cách hệ thống xử lý giá trị không hợp lệ khi nhập khẩu.

## 3. Giải pháp phần mềm

**Vị trí áp dụng:**

- Tệp mẫu nhập khẩu thêm mới tài sản (tải từ **Danh sách tài sản → Nhập khẩu thêm mới tài sản**), áp dụng cho các cột trường mở rộng.

### 3.1. Quy định cách nhập theo từng kiểu trường mở rộng

| Kiểu trường mở rộng | Cách nhập trên tệp mẫu | Xử lý khi nhập khẩu | Thông báo lỗi |
|---|---|---|---|
| Một dòng | Nhập text tự do | Lưu giá trị đã nhập vào trường tương ứng | Không có |
| Nhiều dòng | Nhập text tự do | Lưu giá trị đã nhập vào trường tương ứng | Không có |
| Đường dẫn | Nhập text tự do | Lưu giá trị đã nhập vào trường tương ứng | Không có |
| Ngày | Nhập ngày theo định dạng **dd/mm/yyyy** | Giá trị đúng định dạng: lưu vào trường tương ứng. Giá trị sai định dạng: cảnh báo lỗi, không nhập khẩu dòng đó | `[Tên trường] không hợp lệ. Vui lòng nhập ngày theo định dạng dd/mm/yyyy` |
| Tháng | Nhập theo định dạng **mm/yyyy** | Giá trị đúng định dạng: lưu vào trường tương ứng. Giá trị sai định dạng: cảnh báo lỗi, không nhập khẩu dòng đó | `[Tên trường] không hợp lệ. Vui lòng nhập tháng theo định dạng mm/yyyy` |
| Số | Nhập số nguyên, **không chấp nhận số thập phân và số âm**, độ dài tối đa theo `maxlength` đã thiết lập của trường trên phần mềm | Giá trị hợp lệ: lưu vào trường tương ứng. Giá trị là số thập phân hoặc số âm: cảnh báo lỗi, không nhập khẩu dòng đó. Giá trị vượt quá `maxlength`: cảnh báo lỗi, không nhập khẩu dòng đó | `Số thập phân hoặc số âm: [Tên trường] không hợp lệ` / `Vượt maxlength: [Tên trường] không hợp lệ. Vui lòng nhập không quá [Maxlength] chữ số` |
| Tiền tệ | Nhập số nguyên, **không chấp nhận số thập phân và số âm** (xử lý giống kiểu Số), độ dài tối đa theo `maxlength` đã thiết lập của trường trên phần mềm | Giá trị hợp lệ: lưu vào trường tương ứng. Giá trị là số thập phân hoặc số âm: cảnh báo lỗi, không nhập khẩu dòng đó. Giá trị vượt quá `maxlength`: cảnh báo lỗi, không nhập khẩu dòng đó | `Số thập phân hoặc số âm: [Tên trường] không hợp lệ` / `Vượt maxlength: [Tên trường] không hợp lệ. Vui lòng nhập không quá [Maxlength] chữ số` |
| Số thập phân | Nhập số, cho phép số thập phân tối đa **2 chữ số sau dấu phẩy**, độ dài tối đa theo `maxlength` đã thiết lập của trường trên phần mềm | Giá trị quá 2 chữ số sau dấu phẩy: khi nhập khẩu lên phần mềm, hệ thống tự động làm tròn đến 2 chữ số sau dấu phẩy rồi lưu (ví dụ nhập 10,256 → phần mềm lưu 10,26). Giá trị vượt quá `maxlength`: cảnh báo lỗi, không nhập khẩu dòng đó. Các trường hợp khác: lưu giá trị đã nhập | `Quá 2 chữ số sau dấu phẩy: không báo lỗi (tự động làm tròn khi nhập khẩu)` / `Vượt maxlength: [Tên trường] không hợp lệ. Vui lòng nhập không quá [Maxlength] chữ số` |
| Phần trăm | Nhập số, cho phép số thập phân tối đa **2 chữ số sau dấu phẩy**, độ dài tối đa theo `maxlength` đã thiết lập của trường trên phần mềm | Xử lý giống kiểu Số thập phân. Quá 2 chữ số sau dấu phẩy: tự động làm tròn đến 2 chữ số rồi lưu. Giá trị vượt quá `maxlength`: cảnh báo lỗi, không nhập khẩu dòng đó. Giá trị hợp lệ: lưu vào trường tương ứng | `Quá 2 chữ số sau dấu phẩy: không báo lỗi (tự động làm tròn khi nhập khẩu)` / `Vượt maxlength: [Tên trường] không hợp lệ. Vui lòng nhập không quá [Maxlength] chữ số` |
| Chọn một | Combobox chọn một, danh sách lấy theo danh sách giá trị đã thiết lập của trường | Giá trị có trong danh sách: lưu vào trường tương ứng. Giá trị ngoài danh sách: cảnh báo lỗi, không nhập khẩu dòng đó | `[Tên trường] không hợp lệ. Vui lòng chọn giá trị trong danh sách giá trị đã thiết lập` |
| Tích chọn | Combobox chọn một, gồm 2 giá trị: **Có, Không** | Chọn Có: hệ thống hiểu là có tích. Chọn Không: hệ thống hiểu là không tích. Giá trị khác: cảnh báo lỗi, không nhập khẩu dòng đó | `[Tên trường] không hợp lệ. Vui lòng chọn Có hoặc Không` |
| Chọn nhiều | Nhập text theo format: `[Giá trị 1], [Giá trị 2], ...` — nhiều giá trị trong cùng một ô, các giá trị ngăn cách nhau bằng dấu phẩy (,) hoặc dấu chấm phẩy (;); các giá trị hợp lệ được hệ thống load vào sheet **Danh sách** trong tệp mẫu để người dùng tra cứu | Mỗi giá trị phải có trong danh sách giá trị đã thiết lập của trường. Giá trị không có trong danh sách: cảnh báo lỗi, không nhập khẩu dòng đó. Đủ giá trị hợp lệ: lưu toàn bộ các giá trị đã chọn vào trường tương ứng | `[Tên trường] không hợp lệ. Giá trị [Giá trị] không có trong danh sách giá trị đã thiết lập` |
| Nhân viên | Combobox chọn một, danh sách lấy toàn bộ người dùng có trạng thái **đang làm việc** trên hệ thống, hiển thị theo format **Mã nhân viên <<Tên nhân viên>>**; danh sách được hệ thống load vào sheet **Danh sách** trong tệp mẫu để người dùng tra cứu | Giá trị có trong danh sách: lưu nhân viên tương ứng vào trường. Giá trị ngoài danh sách: cảnh báo lỗi, không nhập khẩu dòng đó | `[Tên trường] không hợp lệ. Vui lòng chọn nhân viên trong danh sách` |
| Tổ chức | Combobox chọn một, danh sách lấy toàn bộ cơ cấu tổ chức có trạng thái **đang theo dõi** trên hệ thống, hiển thị theo format **Mã phòng ban <<Tên phòng ban>>**; danh sách được hệ thống load vào sheet **Danh sách** trong tệp mẫu để người dùng tra cứu | Giá trị có trong danh sách: lưu phòng ban tương ứng vào trường. Giá trị ngoài danh sách: cảnh báo lỗi, không nhập khẩu dòng đó | `[Tên trường] không hợp lệ. Vui lòng chọn phòng ban trong danh sách` |

**Lưu ý:**

- Với trường mở rộng kiểu **chọn nhiều, nhân viên, tổ chức** hệ thống load các giá trị tương ứng vào sheet **Danh sách** trong tệp mẫu — người dùng mở sheet này để tra cứu và lấy đúng giá trị khi điền dữ liệu.
- Trường mở rộng được thiết lập **bắt buộc** trên hệ thống thì trong file nhập khẩu cũng là bắt buộc. Trường hợp để trống: cảnh báo lỗi `[Tên trường] không được để trống`, không nhập khẩu dòng đó.
- Trường mở rộng có thiết lập **giá trị mặc định**: nếu trong file mẫu nhập khẩu để trống thì khi nhập khẩu lên phần mềm tự động lấy theo giá trị mặc định đã thiết lập của trường.
- Trường mở rộng kiểu **tài ảnh, tài tệp**: không hiển thị trên tệp mẫu nhập khẩu. *(Tên kiểu trường trong ảnh có độ phân giải nhỏ; cần đối chiếu bản gốc để xác nhận chính xác.)*

**Phạm vi ảnh hưởng:**

- Bước ghép trường dữ liệu khi nhập khẩu: hiển thị cả các trường mở rộng trong danh sách trường ghép.
- Sau khi nhập khẩu: thông tin hiển thị đúng trên các trường mở rộng tương ứng trên phần mềm (**Danh sách tài sản, form tài sản**).

---

*Nguồn: nội dung hiển thị trong 3 ảnh chụp `business.md` do người dùng cung cấp. Một số dấu câu, ký hiệu định dạng và tên kiểu trường nhỏ cần đối chiếu file gốc để bảo đảm chính xác tuyệt đối.*
