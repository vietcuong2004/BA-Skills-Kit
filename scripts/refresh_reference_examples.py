"""Refresh skill examples from the checked-in in-session fixture; not project generation."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/agent-notes/.specify/_planning"
MAPPING = {
    "ba-brainstorm": ("brainstorm.md", "brainstorm-template.md"),
    "ba-requirements": ("requirements.md", "requirements-template.md"),
    "ba-product-backlog": ("product-backlog.md", "backlog-template.md"),
    "ba-round-plan": ("round-plan.md", "round-plan-template.md"),
    "ba-business": ("drafts/PBI-001/business.md", "business-template.md"),
    "ba-spec": ("drafts/PBI-001/spec.md", "spec-template.md"),
    "ba-review": ("reviews/PBI-001-review.md", "review-template.md"),
}


def main():
    for skill, (source, filename) in MAPPING.items():
        content = (FIXTURE / source).read_text(encoding="utf-8")
        target = ROOT / "skills" / skill / "references" / filename
        target.write_text(
            "> Ví dụ đầy đủ từ fixture giả lập. Không sao chép IDs, hashes, policy hay approval sang project thật. "
            "Khi dùng như template, thay dữ liệu bằng nguồn project đích; đọc schema và giữ headings.\n\n" + content,
            encoding="utf-8")


if __name__ == "__main__":
    main()
