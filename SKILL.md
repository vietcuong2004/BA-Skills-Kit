---
name: ba-skills-kit
description: Điểm vào Kit nguồn để tìm và áp dụng đúng skill phân tích nghiệp vụ, cài đặt hoặc bảo trì BA Skills Kit khi người dùng yêu cầu đọc Kit này.
---

# BA Skills Kit — Điểm vào cho agent

Đọc [AGENTS.md](AGENTS.md) trước khi làm việc trong Kit nguồn. File này chỉ đường tới chín skill chuyên trách; không thay thế hợp đồng của chúng. Installer cài chín thư mục dưới `skills/`, không đăng ký root này thành skill thứ mười.

## Chọn nhiệm vụ

| Yêu cầu | Đọc tiếp | Đầu ra chính |
| --- | --- | --- |
| Ý tưởng mới, pipeline nhiều bước, resume, một PBI/Round | [ba-workflow](skills/ba-workflow/SKILL.md) | Điều phối và workflow-state.md |
| Làm rõ ý tưởng/sản phẩm | [ba-brainstorm](skills/ba-brainstorm/SKILL.md) | brainstorm.md |
| Phân tích yêu cầu từ discovery | [ba-requirements](skills/ba-requirements/SKILL.md) | requirements.md |
| Chia Epic/Feature/PBI | [ba-product-backlog](skills/ba-product-backlog/SKILL.md) | product-backlog.md |
| Đề xuất kế hoạch các đợt | [ba-round-plan](skills/ba-round-plan/SKILL.md) | round-plan.md |
| Viết nghiệp vụ một PBI | [ba-business](skills/ba-business/SKILL.md) | drafts/PBI-ID/business.md |
| Viết đặc tả một PBI | [ba-spec](skills/ba-spec/SKILL.md) | drafts/PBI-ID/spec.md |
| Review cặp tài liệu | [ba-review](skills/ba-review/SKILL.md) | reviews/PBI-ID-review.md |
| Xem trước/xuất tài liệu đã kiểm tra | [ba-publish](skills/ba-publish/SKILL.md) | Round/PBI-ID-slug/{business,spec}.md |
| Cài/cập nhật Kit cho công cụ AI | [INSTALL.md](INSTALL.md) | Skill folders theo runtime |
| Sửa Kit/contracts/helpers | [AGENTS.md](AGENTS.md), conventions và file liên quan | Thay đổi Kit đã kiểm tra |

## Trình tự sử dụng

1. Xác định project đích, config, ý tưởng hoặc PBI ID thật theo yêu cầu. Thiếu thông tin quyết định thì hỏi đúng phần thiếu, không tự chọn project fixture.
2. Đọc [quy ước](conventions/BA-CONVENTIONS.md), SKILL.md đã chọn và schema liên quan. Chỉ đọc references của mode cần thực hiện.
3. Thực hiện Input Validation → Data Extraction → Processing → Output Validation theo skill. Công cụ validate/publish/state ở `scripts/`; chúng không tự gọi model để sinh nội dung.
4. Ghi output theo repository root trong config. Validate bằng `validate_ba_document.py --project-config <config> --file <output> --check-refs`; PBI thêm expected type và requested PBI ID.
5. Báo path, schema/hash/result, Proposed/Open Questions/blockers và checkpoint còn chờ. Không coi PASS là phê duyệt.

## Khi Kit chưa được cài vào runtime

Người dùng có thể chỉ định đọc root này bằng đường dẫn, ví dụ:

```text
Đọc D:/BA-Skills-Kit/AGENTS.md và D:/BA-Skills-Kit/SKILL.md.
Dùng hướng dẫn ba-workflow trong Kit để phân tích project đang mở,
với config ./ba-project.yaml và nhu cầu: [mô tả].
Đi đến backlog và dừng để tôi duyệt phạm vi.
```

Đây là thực hiện instructions từ file được chỉ định; không tuyên bố runtime đã discovery skill. Phải đọc được Kit và chạy được Python đã có dependencies. Muốn gọi skill qua selector/tên trong các phiên sau, cài theo INSTALL.
