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
| ba-publish | Round/PBI/pair/review + human checkpoints | output_root/Round/ID-slug/{business,spec}.md |

Tám skill trên độc lập; ba-workflow là skill thứ chín điều phối bằng file thật. Nó ghi workflow-state sau mỗi handoff/checkpoint. Không coi text trả lời trong chat là thay cho input file đã validate.
