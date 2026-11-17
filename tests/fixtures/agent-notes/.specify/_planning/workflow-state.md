---
schema_version: '1.0'
document_type: workflow-state
project_id: agent-notes
status: draft
source_documents: []
generated_by: ba-workflow
---
# workflow-state

<!-- BA-DATA:START -->
```yaml
mode: SINGLE-PBI
current_phase: selected-pbi-published
completed:
- ba-brainstorm
- ba-requirements
- ba-product-backlog
- ba-round-plan
- ba-business
- ba-spec
- ba-review
- ba-publish
pending:
- Refine unassigned PBI-002/PBI-003/PBI-004 when requested
blockers: []
artifacts:
- path: .specify/_planning/brainstorm.md
  sha256: 938a9a472fe6d3e586528e10b8463a1ddff1e125c3f8b2cc84dd11a9724c941c
- path: .specify/_planning/requirements.md
  sha256: 6b105dd6e09ee90b872a66650ed5b2e3df8fe596f2c5e457498b3dad49284556
- path: .specify/_planning/product-backlog.md
  sha256: 9d235920a1ea615bd6420162e3812b9ae1b382bb4576d5cba6ac04c1887d8726
- path: .specify/_planning/round-plan.md
  sha256: 87b68678977c83f909b4f28b847b0d947bef9f9e9f4365f13f5a07cf45eea7e1
- path: .specify/_planning/drafts/PBI-001/business.md
  sha256: b145a0531ccf204e1ae02e21f2ffdaa70caf962bcebe7a54dbdd7bbdf0853eb7
- path: .specify/_planning/drafts/PBI-001/spec.md
  sha256: 8259f2ab88d4657f0d2b554496a99f09f5e5f1ab927747800de15b10f66652f1
- path: .specify/_planning/reviews/PBI-001-review.md
  sha256: 9fb255ad6f973d46e25a4de18f174b333df33171870a65b72841e3da262b1dfb
approvals:
- checkpoint: backlog
  decision: Approved
  actor: TEST HUMAN DOUBLE
  evidence: scenario.txt — synthetic scripted decision, not a real user approval
  decided_at: '2026-11-17T00:00:00+07:00'
  pbi_refs:
  - PBI-001
  documents:
  - path: .specify/_planning/product-backlog.md
    sha256: 9d235920a1ea615bd6420162e3812b9ae1b382bb4576d5cba6ac04c1887d8726
  resolved_decisions:
  - Personal-note behavior specified in scenario.txt
- checkpoint: round-plan
  decision: Proposed Allowed
  actor: TEST HUMAN DOUBLE
  evidence: scenario.txt — synthetic scripted decision, not a real user approval
  decided_at: '2026-11-17T00:00:00+07:00'
  pbi_refs:
  - PBI-001
  documents:
  - path: .specify/_planning/round-plan.md
    sha256: 87b68678977c83f909b4f28b847b0d947bef9f9e9f4365f13f5a07cf45eea7e1
  resolved_decisions:
  - Personal-note behavior specified in scenario.txt
- checkpoint: publish
  decision: Draft Publication
  actor: TEST HUMAN DOUBLE
  evidence: scenario.txt — synthetic scripted decision, not a real user approval
  decided_at: '2026-11-17T00:00:00+07:00'
  pbi_refs:
  - PBI-001
  documents:
  - path: .specify/_planning/product-backlog.md
    sha256: 9d235920a1ea615bd6420162e3812b9ae1b382bb4576d5cba6ac04c1887d8726
  - path: .specify/_planning/round-plan.md
    sha256: 87b68678977c83f909b4f28b847b0d947bef9f9e9f4365f13f5a07cf45eea7e1
  - path: .specify/_planning/drafts/PBI-001/business.md
    sha256: b145a0531ccf204e1ae02e21f2ffdaa70caf962bcebe7a54dbdd7bbdf0853eb7
  - path: .specify/_planning/drafts/PBI-001/spec.md
    sha256: 8259f2ab88d4657f0d2b554496a99f09f5e5f1ab927747800de15b10f66652f1
  - path: .specify/_planning/reviews/PBI-001-review.md
    sha256: 9fb255ad6f973d46e25a4de18f174b333df33171870a65b72841e3da262b1dfb
  resolved_decisions:
  - Personal-note behavior specified in scenario.txt
last_updated: '2026-11-17T00:00:00+07:00'
selected_pbis:
- PBI-001
selected_round: R1
change_history: []
```
<!-- BA-DATA:END -->

## Current Phase

Selected PBI-001 draft published; không tuyên bố hoàn tất các PBI khác.

## Completed

Tám bước được thực hiện bằng file thật trong phiên; review FAIL rồi refinement và CONDITIONAL.

## Pending

Refine unassigned PBI-002/PBI-003/PBI-004 when requested

## Blockers

Không còn blocker cho draft PBI-001; Minor UI còn trong review.

## Artifacts

Snapshot hashes trong BA-DATA, đọc lại khi RESUME.

## Approvals

Tất cả approvals ở đây là TEST HUMAN DOUBLE từ scenario.txt, không phải quyết định thật.

## Recovery

RESUME phải validate source chain; nguồn đổi làm review/approval cũ stale.

## Contract Summary

| ID | Title | State |
| --- | --- | --- |

