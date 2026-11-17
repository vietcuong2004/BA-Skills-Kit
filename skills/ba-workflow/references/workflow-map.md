# Workflow map

| Bước | Input đã validate | Output / checkpoint |
| --- | --- | --- |
| ba-brainstorm | idea + config | brainstorm.md |
| ba-requirements | brainstorm | requirements.md |
| ba-product-backlog | brainstorm + requirements | product-backlog.md; duyệt scope |
| ba-round-plan | backlog + requirements | round-plan.md; duyệt/cho phép Proposed |
| ba-business | selected PBI + brainstorm/requirements/backlog, Round nếu có | drafts/ID/business.md |
| ba-spec | same PBI business + requirements/backlog | drafts/ID/spec.md |
| ba-review | same PBI pair + requirements/backlog | reviews/ID-review.md |
| ba-publish | Round/PBI/pair/review + human checkpoints | output_root/Round/ID-slug/{business,spec}.md — bản đọc được, không metadata |

Tám skill trên độc lập; ba-workflow là skill thứ chín điều phối bằng file thật. Nó ghi workflow-state sau mỗi handoff/checkpoint. Không coi text trả lời trong chat là thay cho input file đã validate.

Các output từ brainstorm đến review là hồ sơ nội bộ dưới .temp. Sau business/spec, dùng ba_public.py tạo preview trong .temp/previews/PBI-ID để review cả nội dung bàn giao. Metadata giữ ở drafts; hai file cuối trong Round/PBI chỉ có ngôn ngữ tự nhiên, bảng và checklist.
