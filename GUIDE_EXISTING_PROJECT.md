# Viết tài liệu cho dự án đã có tính năng

Dự án đã có mã nguồn hoặc giao diện nhưng bạn chưa biết có những tính năng nào? Làm theo ba bước dưới đây để tìm hiểu dự án và tạo tài liệu. **PBI** là một phần việc cụ thể, chẳng hạn “Tìm tài liệu theo tên”. Mỗi PBI có hai file giải thích tính năng dùng để làm gì và hoạt động ra sao.

## Trước khi bắt đầu

Mở thư mục `your-project` trong Codex, Claude Code hoặc Antigravity đã cài BA Skills Kit. Dán từng câu mẫu vào ô chat. [Hướng dẫn cài đặt](INSTALL.md)

Bạn có thể dùng nguyên câu mẫu. Để chọn skill trực tiếp, chẳng hạn ở bước 1, gõ `$ba-explore-project` trong Codex hoặc `/ba-explore-project` trong Claude Code, rồi thêm phần yêu cầu.

## Bước 1. Xem dự án có những tính năng nào

```text
Dùng skill ba-explore-project để xem dự án này có những tính năng nào. Chỉ khảo sát và liệt kê các tính năng tìm được.
```

**Bạn nhận được gì?** Báo cáo `.temp/exploration/project-exploration.md` cho biết mỗi tính năng làm được gì, nằm ở đâu và phần nào còn chưa rõ.

## Bước 2. Chia tính năng thành các PBI

```text
Dùng skill ba-workflow để chia các tính năng vừa khảo sát thành từng PBI. Chỉ lập và lưu danh sách PBI.
```

**Bạn nhận được gì?** Danh sách `.temp/product-backlog.md` cho biết tên và mã của từng phần việc. Ví dụ, tính năng tìm kiếm có thể được chia thành `PBI-001` “Tìm tài liệu theo tên” và `PBI-002` “Lọc theo ngày”.

## Bước 3. Viết và lưu tài liệu PBI

```text
Dùng skill ba-workflow để viết, kiểm tra và lưu tài liệu cho các PBI trong danh sách vừa lập.
```

Muốn làm trước một phần việc, thay “các PBI trong danh sách vừa lập” bằng tên hoặc mã của phần việc đó, ví dụ `PBI-001`.

**Bạn nhận được gì?** Mở thư mục `.specify` trong dự án. Mỗi PBI có thư mục riêng trong một đợt như `R1` hoặc `R2`. Ví dụ dưới đây là một PBI trong đợt đầu.

```text
.specify/R1/PBI-001-tim-tai-lieu/
├── business.md
└── spec.md
```

- **`business.md`** giải thích ai dùng tính năng, dùng để làm gì và nghiệp vụ diễn ra thế nào.
- **`spec.md`** mô tả thao tác, phản hồi của hệ thống và các tình huống cần kiểm thử.

Trợ lý ghi phần chưa rõ trong bản nháp và tiếp tục phần có thể làm. Nếu file đã lưu có nội dung khác, trợ lý giữ file đó và gửi đường dẫn bản đọc thử.

Giữ thư mục `.temp` để dùng lại kết quả đã làm. Khi mở lại dự án, bạn có thể nhắn “Dùng skill ba-workflow để tiếp tục viết những PBI còn thiếu.”

## Nếu muốn chạy cả ba bước trong một lượt

```text
Dùng skill ba-workflow để khảo sát dự án này và tạo tài liệu PBI cho các tính năng đã có.
```

Trợ lý tự khảo sát, lập danh sách, viết, kiểm tra và lưu hai file cho mỗi PBI.

## Nếu muốn bổ sung một tính năng mới

```text
Dùng skill ba-pbi để viết và lưu tài liệu cho tính năng cho phép người dùng tải danh sách tài liệu xuống.
```

Thay phần mô tả bằng tính năng bạn muốn thêm. Trợ lý dùng thông tin của dự án hiện tại để viết một PBI cho phần thay đổi đó.

[Về README](README.md) · [Hướng dẫn cho dự án mới](GUIDE_NEW_PROJECT.md)
