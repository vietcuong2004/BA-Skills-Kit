# BA Skills Kit

**Bộ hướng dẫn cho AI giúp bạn làm rõ nhu cầu phần mềm và tạo tài liệu để nhóm phát triển cùng sử dụng.**

Bạn có thể bắt đầu từ một ý tưởng còn mơ hồ hoặc một dự án đã có giao diện và chức năng nhưng thiếu tài liệu. BA Skills Kit hướng dẫn agent khảo sát, phân tích, chia nhỏ phạm vi và viết tài liệu nghiệp vụ cùng đặc tả cho từng phần việc.

Kit gồm **11 skill**, dùng với các coding agent như Codex, Claude Code và Antigravity. Bạn trò chuyện với agent ngay trong thư mục `your-project`; không cần biết trước cách viết tài liệu BA.

## Bộ Kit giúp bạn làm gì?

- Hiểu sản phẩm phục vụ ai, giải quyết vấn đề gì và cần những chức năng nào.
- Khảo sát tính năng hiện có, chỉ ra bằng chứng và phần chưa xác minh được.
- Chuyển nhu cầu thành yêu cầu cụ thể và các phần việc có thể nghiệm thu.
- Đề xuất thứ tự thực hiện hoặc tài liệu hóa theo từng đợt.
- Tạo cặp `business.md` và `spec.md` cho mỗi PBI được chọn, rồi review trước khi bàn giao.
- Bổ sung một PBI khi muốn phát triển thêm tính năng cho dự án hiện hữu.

Bạn vẫn quyết định phạm vi và các quy tắc nghiệp vụ. AI ghi rõ đề xuất/câu hỏi còn mở và dừng ở các điểm cần bạn duyệt. Kết quả của Kit là **hồ sơ phân tích và đặc tả**; nhóm phát triển dùng chúng để triển khai và kiểm thử.

## Thuật ngữ dễ hiểu

| Thuật ngữ | Hiểu đơn giản |
| --- | --- |
| **Agent** | Trợ lý AI có thể đọc và làm việc với file dự án, ví dụ Codex hoặc Claude Code. |
| **Skill** | Bộ hướng dẫn để agent làm một loại công việc theo quy trình nhất quán. |
| **BA — Business Analyst** | Người phân tích nhu cầu, quy trình và cách phần mềm cần hoạt động. |
| **Capability / CAP** | Một khả năng sản phẩm cần có, ví dụ quản lý hồ sơ. |
| **Requirement / REQ** | Một yêu cầu cụ thể, ví dụ người có quyền có thể tạo hồ sơ mới. |
| **Epic / Feature** | Nhóm nhu cầu lớn / nhóm chức năng nhỏ hơn bên trong. |
| **PBI — Product Backlog Item** | Một phần việc có giá trị người dùng, phạm vi rõ và kết quả kiểm chứng được. |
| **Backlog** | Danh sách các PBI cần xem xét, ưu tiên và thực hiện hoặc tài liệu hóa. |
| **Round — R1, R2…** | Một đợt gồm các PBI được chọn; có thể là đợt phát triển hoặc đợt tài liệu hóa. |
| **Flow** | Chuỗi thao tác người dùng và phản hồi hệ thống, gồm cả nhánh khác hoặc lỗi. |
| **Edge Case** | Tình huống đặc biệt cần làm rõ, như bấm Lưu hai lần hoặc mất mạng khi lưu. |
| **AC — Acceptance Criteria** | Điều kiện nghiệm thu để biết một PBI đáp ứng yêu cầu; thường viết theo Given — When — Then: trước đó thế nào, khi làm gì, kết quả ra sao. |
| **Review / Finding / Blocker** | Kiểm tra tài liệu / vấn đề được phát hiện / vấn đề bắt buộc giải quyết trước khi đi tiếp. |
| **Draft / Proposed** | Bản nháp / đề xuất, còn cần xem xét. |
| **Publish** | Xuất cặp tài liệu vào thư mục bàn giao của dự án. |

`Round` không bắt buộc là Sprint Scrum. `Publish` ở đây là xuất file tài liệu, không phải đưa ứng dụng lên Internet.

## Các skill trong Kit

| Bạn cần | Skill phù hợp |
| --- | --- |
| Khám phá dự án đã có tính năng nhưng thiếu tài liệu | `ba-explore-project` |
| Đi qua nhiều bước hoặc tiếp tục công việc đang dở | `ba-workflow` |
| Làm rõ ý tưởng sản phẩm | `ba-brainstorm` |
| Phân tích yêu cầu và quy tắc | `ba-requirements` |
| Chia yêu cầu thành Epic, Feature và PBI | `ba-product-backlog` |
| Đề xuất các đợt thực hiện | `ba-round-plan` |
| Viết bối cảnh, giá trị và giải pháp nghiệp vụ cho một PBI | `ba-business` |
| Viết hành vi chi tiết và điều kiện nghiệm thu | `ba-spec` |
| Kiểm tra chất lượng tài liệu | `ba-review` |
| Xuất cặp tài liệu đủ điều kiện | `ba-publish` |
| Thêm một PBI mới cho tính năng muốn phát triển thêm | `ba-pbi` |

Người mới chỉ cần chọn một trong hai hướng dẫn bên dưới; agent sẽ điều phối các skill cần thiết.

## Cài đặt

Chuẩn bị công cụ AI đã đăng nhập, Python 3.10 trở lên và thư mục `your-project`. Dự án có thể đã có mã nguồn hoặc mới chỉ là một thư mục trống.

1. Tải/clone [BA-Skills-Kit](https://github.com/vietcuong2004/BA-Skills-Kit) về máy.
2. Làm theo **[INSTALL.md — Cài cho Claude Code, Codex và Antigravity](INSTALL.md)** để tạo môi trường Python, cài thư viện và cài các skill vào đúng công cụ. Có thể cài cá nhân một lần cho nhiều project hoặc cài riêng từng project.
3. Mở agent tại thư mục gốc `your-project`, kiểm tra nhận diện được `ba-workflow`, `ba-explore-project` và `ba-pbi`. Nếu chưa thấy sau khi cài, mở phiên mới.
4. Chuẩn bị `.temp/ba-project.yaml` theo mẫu trong INSTALL. Nếu chưa biết cấu hình, yêu cầu agent đề xuất và hỏi bạn xác nhận tên dự án cùng nơi lưu output.

Chỉ đặt Kit trên ổ đĩa chưa có nghĩa agent đã nhận diện skill. Hướng dẫn cài đặt cũng chỉ rõ cách cập nhật và xử lý lỗi thiếu thư viện.

**Cách gọi trong chat:** Codex dùng `$ba-workflow`, Claude Code dùng `/ba-workflow`; Antigravity có thể nhận câu “Dùng skill ba-workflow”. Tham số và lời mô tả gửi trong chat, không chạy như lệnh PowerShell.

## Chọn hướng dẫn phù hợp

| Tình huống của bạn | Mở hướng dẫn |
| --- | --- |
| Dự án đã có giao diện và tính năng; bạn chưa hiểu hiện trạng hoặc muốn bổ sung bộ tài liệu | **[Dự án hiện có: khảo sát bằng ba-explore-project rồi viết tài liệu PBI](GUIDE_EXISTING_PROJECT.md)** |
| Dự án mới; bạn chỉ có một nhu cầu hoặc ý tưởng chưa rõ phạm vi | **[Dự án mới: từ ý tưởng mơ hồ đến bộ tài liệu PBI](GUIDE_NEW_PROJECT.md)** |

Hai hướng dẫn có câu nhắn để copy vào agent, thứ tự thực hiện, file đầu ra và các điểm cần bạn duyệt. Tên `your-project`, các ID PBI và nội dung trong ngoặc vuông là ví dụ để thay bằng dự án thực tế.

## Kết quả được lưu ở đâu?

```text
your-project/
├── .temp/                         # Cấu hình và hồ sơ làm việc
│   ├── ba-project.yaml
│   └── ...                        # Khảo sát, yêu cầu, backlog, Round plan,
│                                  # drafts, reviews và tiến độ
└── .specify/                      # Tài liệu được phép bàn giao
    └── R1/
        └── PBI-001-ten-tinh-nang/
            ├── business.md
            └── spec.md
```

- **`business.md`** giải thích vì sao cần PBI, ai sử dụng, giá trị, phạm vi và giải pháp nghiệp vụ.
- **`spec.md`** mô tả phần mềm phải hoạt động thế nào: luồng, quy tắc, quyền, dữ liệu, lỗi và điều kiện nghiệm thu.

`.specify` chỉ chứa Round/PBI với đúng hai file trên trong mỗi PBI. Tất cả hồ sơ trung gian nằm dưới `.temp`; cần giữ chúng để tiếp tục công việc và kiểm tra nguồn sau này.

Chi tiết kỹ thuật dành cho người bảo trì: [quy ước tài liệu](conventions/BA-CONVENTIONS.md) và [điểm vào cho agent](SKILL.md). `tests/` chỉ giữ local để bảo trì, được Git bỏ qua và không nằm trong gói cài đặt.
