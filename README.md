# BA Skills Kit

**BA Skills Kit giúp bạn dùng AI để viết tài liệu phần mềm cho nhóm phát triển và kiểm thử.**

Kit gồm 11 skill cho Codex, Claude Code và Antigravity. Trợ lý có thể đọc mã nguồn để mô tả các tính năng hiện có, hoặc dựa vào ý tưởng của bạn để đề xuất phần mềm cần làm gì. Trợ lý chia các tính năng thành từng phần việc, gọi là **PBI**, rồi viết tài liệu cho từng phần.

## Cài đặt

1. Tải BA Skills Kit về máy và chuẩn bị Python 3.10 trở lên. [Kho mã nguồn BA Skills Kit](https://github.com/vietcuong2004/BA-Skills-Kit)
2. Cài skill cho công cụ bạn dùng. Bạn có thể cài riêng cho `your-project` hoặc cài một lần để dùng cho nhiều dự án. [Hướng dẫn cài đặt](INSTALL.md)
3. Mở `your-project` trong công cụ đã cài skill, rồi gửi câu mẫu trong hướng dẫn bên dưới vào ô chat. Trợ lý sẽ tạo `.temp/ba-project.yaml` nếu dự án chưa có cấu hình.

Trong Codex, bạn có thể chọn skill bằng `$ba-workflow`. Trong Claude Code, dùng `/ba-workflow`. Trong Antigravity, bạn có thể nhắn “Dùng skill ba-workflow…” và mô tả việc cần làm.

## Chọn hướng dẫn phù hợp

- **Dự án đã có tính năng.** Khảo sát bằng `ba-explore-project`, sau đó dùng `ba-workflow` để lập danh sách và viết PBI. Bạn cũng có thể dùng `ba-workflow` để làm cả ba bước trong một lượt. [Hướng dẫn cho dự án hiện có](GUIDE_EXISTING_PROJECT.md)
- **Dự án mới, bạn mới có ý tưởng.** Mô tả ai sẽ dùng phần mềm và họ cần làm gì. `ba-workflow` sẽ phân tích ý tưởng và viết tài liệu cho các PBI. [Hướng dẫn cho dự án mới](GUIDE_NEW_PROJECT.md)

Muốn thêm một tính năng vào dự án đang có, dùng `ba-pbi` và mô tả tính năng đó. [Câu mẫu để bổ sung tính năng](GUIDE_EXISTING_PROJECT.md#nếu-muốn-bổ-sung-một-tính-năng-mới)

Mặc định, khi bạn yêu cầu viết PBI, trợ lý tự lập danh sách, nhóm các PBI theo đợt, viết, kiểm tra và lưu tài liệu trong cùng lượt. Phần chưa rõ được ghi trong bản nháp. Nếu bạn chỉ yêu cầu khảo sát hoặc lập danh sách, trợ lý dừng ở kết quả đó.

## PBI và Round là gì?

### PBI là một phần việc có kết quả kiểm tra được

**PBI** viết tắt của *Product Backlog Item*. Hãy nghĩ về PBI như một mục trong danh sách việc cần phát triển hoặc viết tài liệu. Mỗi mục mô tả **ai cần làm gì, việc đó bao gồm những gì và làm sao biết nó hoạt động đúng**. Khi dự án đã có tính năng, PBI có thể mô tả hành vi đã có. Khi dự án mới bắt đầu, PBI mô tả hành vi cần xây dựng.

Ví dụ, tính năng **Tìm kiếm tài liệu** có thể chia thành ba phần việc. Mỗi phần mang lại một kết quả riêng mà người dùng có thể thử.

| PBI | Người dùng làm gì? | Kết quả kiểm tra được |
| --- | --- | --- |
| `PBI-001` | Tìm tài liệu theo tên. | Nhập một từ khóa và thấy các tài liệu có tên khớp. |
| `PBI-002` | Lọc kết quả theo ngày. | Chọn khoảng ngày và chỉ thấy các tài liệu được cập nhật trong khoảng đó. |
| `PBI-003` | Tải danh sách kết quả. | Tải được tệp chứa kết quả theo từ khóa và bộ lọc đang chọn. |

Mã như `PBI-002` giúp bạn chọn đúng phần việc khi nhắn cho trợ lý. Danh sách các phần việc gọi là **backlog**. Bạn có thể xem danh sách này trong `.temp/product-backlog.md` sau khi trợ lý lập xong.

### Round là một đợt gồm một hoặc nhiều PBI

**Round** cho biết nhóm phần việc nào được xếp trước, nhóm nào được xếp sau. Trợ lý nhóm các PBI theo mục tiêu của đợt và xem phần nào cần dựa vào kết quả của phần khác. Mỗi PBI đã xếp đợt chỉ thuộc một Round. Trong ví dụ tìm kiếm tài liệu, trợ lý có thể đề xuất hai đợt.

- **`R1` — Đợt đầu.** Gom `PBI-001` và `PBI-002` để người dùng tìm được tài liệu rồi thu hẹp danh sách kết quả.
- **`R2` — Đợt tiếp theo.** Đặt `PBI-003` ở đây vì việc tải danh sách sử dụng kết quả tìm kiếm đã lọc ở đợt đầu.

Với dự án đã có tính năng, Round có thể dùng để sắp xếp thứ tự viết tài liệu. Với dự án mới, Round có thể dùng để đề xuất thứ tự phát triển. Khi chưa có ước lượng, trợ lý ghi đây là kế hoạch đề xuất. Sau khi lập kế hoạch, mở `.temp/round-plan.md` để xem từng Round gồm những PBI nào và lý do sắp xếp.

## Kết quả nằm ở đâu?

```text
your-project/
├── .temp/                         # Cấu hình và hồ sơ làm việc
└── .specify/
    ├── R1/
    │   ├── PBI-001-tim-tai-lieu-theo-ten/
    │   │   ├── business.md
    │   │   └── spec.md
    │   └── PBI-002-loc-ket-qua-theo-ngay/
    │       ├── business.md
    │       └── spec.md
    └── R2/
        └── PBI-003-tai-danh-sach-ket-qua/
            ├── business.md
            └── spec.md
```

- **`business.md`** giải thích ai dùng tính năng, dùng để làm gì và nghiệp vụ diễn ra thế nào.
- **`spec.md`** mô tả thao tác, phản hồi của phần mềm và các tình huống cần kiểm thử.

Mỗi thư mục PBI trong `.specify` chỉ có hai file Markdown dành cho người đọc. Cấu hình, báo cáo khảo sát, danh sách PBI, bản nháp và thông tin kỹ thuật để quản lý tài liệu nằm trong `.temp`. Giữ thư mục này để trợ lý có thể tiếp tục công việc ở lượt sau.

## Thuật ngữ thường gặp

| Thuật ngữ | Hiểu đơn giản |
| --- | --- |
| **BA — Business Analyst** | Người làm rõ nhu cầu của người dùng và cách phần mềm cần hoạt động. |
| **Skill** | Bộ hướng dẫn để trợ lý làm một việc cụ thể, như khảo sát dự án hoặc viết PBI. |
| **Điều kiện nghiệm thu (AC)** | Kết quả dùng để kiểm tra tính năng. Ví dụ, khi tìm theo tên, người dùng thấy những tài liệu có tên khớp từ khóa. |
| **Bản nháp (Draft)** | Phiên bản làm việc có thể chứa giả định hoặc câu hỏi cần làm rõ. |
| **Xuất tài liệu (Publish)** | Lưu hai file PBI vào thư mục `.specify` của dự án. |

[Danh sách đầy đủ các skill](SKILL.md)
