# Hướng dẫn viết tài liệu `business.md` cho PBI

> Nguồn: Nội dung hiển thị trên 3 ảnh chụp slide “Yêu cầu phần mềm (PBI)”, “Hướng dẫn viết Nội dung PBI” và “Hướng dẫn viết phần Giải pháp”. Tài liệu này chuyển các hướng dẫn trên slide sang Markdown, không bổ sung quy định chưa có trong ảnh.

## 1. Mục đích của PBI

- Là các yêu cầu sẽ đáp ứng trên phần mềm (thường tương ứng với mỗi giao diện màn hình, chức năng là 1 yêu cầu) tạo thành 1 PBI trên TFS.
- Là căn cứ để lập trình viên thi công chức năng, để QC viết test case và test chương trình.

### Đầu vào

- Thiết kế UI đã duyệt.
- Mô tả chi tiết yêu cầu nghiệp vụ trên cây yêu cầu người dùng.

## 2. Hướng dẫn viết nội dung PBI

Theo quy định được dẫn chiếu trong slide (liên kết “tại đây” không hiển thị URL trong ảnh).

- **Tiêu đề (Title):** Mô tả tóm tắt nội dung yêu cầu.
- **Thông tin tab Description:**
  - **Mục đích:** Vai trò gì? Muốn chức năng gì? Nhằm mục đích gì?
  - **YC Nghiệp vụ:** Mô tả lại các nghiệp vụ và quy tắc nghiệp vụ chi tiết. Có thể link đến cây tài liệu nghiệp vụ tương ứng.
  - **Giải pháp phần mềm, nghiệp vụ/chức năng bị ảnh hưởng:** Ghi lại giải pháp đáp ứng trên phần mềm (nhằm đáp ứng được nghiệp vụ và các chức năng nghiệp vụ bị ảnh hưởng khi phân tích) và các yêu cầu về tính tiện dụng cần phải thực hiện riêng cho các màn hình liên quan khi đáp ứng nghiệp vụ đang xét đến. Nội dung này cần được thể hiện dưới dạng hình ảnh trực quan để Dev dễ đọc, dễ hình dung.
  - **YC Hiệu năng, bảo mật:** Mô tả các yêu cầu về hiệu năng, bảo mật cho chức năng đang thực hiện.

## 3. Hướng dẫn viết phần Giải pháp

### 3.1. Trình tự mô tả

- Căn cứ vào giao diện, mô tả lần lượt từng thông tin (trường) và theo thứ tự từ trái qua phải, từ trên xuống dưới.
- Tùy thuộc vào mỗi dạng trường thông tin mà cách lấy sẽ khác nhau. Đối với mỗi trường thông tin thường lưu ý:
  - Lần đầu tiên vào ngầm định thế nào.
  - Lấy giá trị từ đâu hay nhập thông tin thế nào.
  - Có bắt buộc nhập không.
  - Có ảnh hưởng bởi tùy chọn chung gì không.
  - Lưu ý những thông tin theo Rule chung thì chỉ tới PBI chung.
  - …

## 4. Khung đề xuất cho `business.md` khi áp dụng hướng dẫn

> Phần này là **khung triển khai gợi ý**, không phải nội dung nguyên văn trên slide.

```markdown
# Đặc tả yêu cầu nghiệp vụ

**Tên PBI:** ...
**Mã PBI:** ...

## 1. Mục đích
- Vai trò sử dụng: ...
- Chức năng mong muốn: ...
- Mục tiêu nghiệp vụ: ...

## 2. Nghiệp vụ
- Bối cảnh nghiệp vụ: ...
- Quy tắc nghiệp vụ chi tiết: ...
- Liên kết tài liệu nghiệp vụ: ...

## 3. Giải pháp phần mềm
### 3.1. Vị trí áp dụng và giao diện liên quan
- ...

### 3.2. Mô tả các trường trên giao diện
| Trường | Giá trị mặc định | Nguồn dữ liệu / cách nhập | Bắt buộc | Tùy chọn / quy tắc liên quan | Xử lý / thông báo lỗi |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

### 3.3. Nghiệp vụ / chức năng bị ảnh hưởng
- ...

### 3.4. Yêu cầu tiện dụng và hình ảnh minh họa
- ...

## 4. Yêu cầu hiệu năng, bảo mật
- Hiệu năng: ...
- Bảo mật: ...
```

## 5. Checklist rà soát

- [ ] Tiêu đề tóm tắt được yêu cầu.
- [ ] Mục đích trả lời đủ vai trò, mong muốn và mục tiêu.
- [ ] Nghiệp vụ và quy tắc nghiệp vụ được mô tả chi tiết.
- [ ] Giải pháp mô tả theo thứ tự các trường trên giao diện.
- [ ] Mỗi trường nêu rõ mặc định, nguồn dữ liệu/cách nhập, bắt buộc hay không, tùy chọn chung liên quan.
- [ ] Các quy tắc chung được dẫn chiếu đến PBI chung khi phù hợp.
- [ ] Có mô tả chức năng bị ảnh hưởng và hình ảnh trực quan cho Dev.
- [ ] Có yêu cầu hiệu năng, bảo mật tương ứng.
