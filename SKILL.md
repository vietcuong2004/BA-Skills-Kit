BA Skills Kit — Điểm vào cho agent

Đọc [AGENTS.md](AGENTS.md) trước khi làm việc trong Kit nguồn. File này chỉ đường tới chín skill pipeline và hai skill phụ khám phá hiện trạng/thêm PBI; không thay thế hợp đồng của chúng. Installer cài các thư mục dưới `skills/`, không đăng ký root này thành skill riêng.

## Chọn nhiệm vụ

| Yêu cầu                                                                          | Đọc tiếp                                             | Đầu ra chính                                         |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- |
| Thêm một tính năng/PBI mới vào dự án hiện hữu | [ba-pbi](skills/ba-pbi/SKILL.md) | Cặp business.md/spec.md của PBI mới |
| Viết PBI cho dự án đã có tính năng | [ba-workflow](skills/ba-workflow/SKILL.md) | Khảo sát bằng ba-explore-project và xuất các PBI |
| Chỉ khảo sát hiện trạng | [ba-explore-project](skills/ba-explore-project/SKILL.md) | Báo cáo và brief trong .temp |
| Ý tưởng mới, pipeline nhiều bước, resume, một PBI/Round                    | [ba-workflow](skills/ba-workflow/SKILL.md)               | Điều phối và workflow-state.md                      |
| Làm rõ ý tưởng/sản phẩm                                                     | [ba-brainstorm](skills/ba-brainstorm/SKILL.md)           | brainstorm.md                                           |
| Phân tích yêu cầu từ discovery                                                | [ba-requirements](skills/ba-requirements/SKILL.md)       | requirements.md                                         |
| Chia Epic/Feature/PBI                                                              | [ba-product-backlog](skills/ba-product-backlog/SKILL.md) | product-backlog.md                                      |
| Đề xuất kế hoạch các đợt                                                   | [ba-round-plan](skills/ba-round-plan/SKILL.md)           | round-plan.md                                           |
| Viết nghiệp vụ một PBI                                                         | [ba-business](skills/ba-business/SKILL.md)               | drafts/PBI-ID/business.md                               |
| Viết đặc tả một PBI                                                           | [ba-spec](skills/ba-spec/SKILL.md)                       | drafts/PBI-ID/spec.md                                   |
| Review cặp tài liệu                                                             | [ba-review](skills/ba-review/SKILL.md)                   | reviews/PBI-ID-review.md                                |
| Xem trước/xuất tài liệu đã kiểm tra                                        | [ba-publish](skills/ba-publish/SKILL.md)                 | Round/PBI-ID-slug/{business,spec}.md                    |
| Cài/cập nhật Kit cho công cụ AI                                               | [INSTALL.md](INSTALL.md)                                 | Skill folders theo runtime                              |
| Sửa Kit/contracts/helpers                                                         | [AGENTS.md](AGENTS.md), conventions và file liên quan  | Thay đổi Kit đã kiểm tra                           |

## Trình tự sử dụng

1. Xác định dự án đích và mục tiêu từ yêu cầu cùng tài liệu hiện có. Khi thiếu cấu hình, tạo .temp/ba-project.yaml theo quy ước chung. Dùng các mặc định hợp lý và ghi phần còn chưa rõ vào hồ sơ.
2. Đọc [quy ước](conventions/BA-CONVENTIONS.md), SKILL.md đã chọn và schema liên quan. Chỉ đọc references của mode cần thực hiện.
3. Thực hiện Input Validation → Data Extraction → Processing → Output Validation theo skill. Công cụ validate/publish/state ở `scripts/`; chúng không tự gọi model để sinh nội dung.
4. Ghi output theo repository root trong config. Validate bằng `validate_ba_document.py --project-config <config> --file <output> --check-refs`; PBI thêm expected type và requested PBI ID.
   `planning_dir` phải dưới `.temp`. `.specify` chỉ chứa các Round/PBI với đúng hai file business.md/spec.md đọc được, không có metadata/BA-DATA/Contract Summary. Metadata và toàn bộ hồ sơ phân tích, draft, review, preview, tiến độ nằm trong `.temp`. Dùng ba_public.py để preview và ba-publish để xuất; cặp tài liệu theo [mẫu business](templates/business-handover.md) và [mẫu spec](templates/spec-handover.md). Nếu gặp cấu hình cũ dưới output_root, báo migration cần thiết, không tiếp tục ghi vào `_planning`.
5. Với yêu cầu tạo PBI, thực hiện tới khi xuất file trong cùng lượt. Trả đường dẫn hai file, kết quả kiểm tra và điểm còn mở.

## Khi Kit chưa được cài vào runtime

Người dùng có thể chỉ định đọc root này bằng đường dẫn, ví dụ:

```text
Đọc D:/BA-Skills-Kit/AGENTS.md và D:/BA-Skills-Kit/SKILL.md.
Dùng hướng dẫn ba-workflow trong Kit để phân tích project đang mở,
với config ./.temp/ba-project.yaml và nhu cầu: [mô tả].
Hãy phân tích và xuất các cặp business.md/spec.md cho các PBI.
```

Đây là thực hiện instructions từ file được chỉ định; không tuyên bố runtime đã discovery skill. Phải đọc được Kit và chạy được Python đã có dependencies. Muốn gọi skill qua selector/tên trong các phiên sau, cài theo INSTALL.
