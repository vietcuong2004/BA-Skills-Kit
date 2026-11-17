"""Maintenance only: refresh examples from local test fixtures (not shipped in the Kit)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests/fixtures/agent-notes/.temp"
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
    if not FIXTURE.is_dir():
        raise SystemExit("NOT RUN: local tests/fixtures are not included in the distributed Kit. This maintenance helper is optional; skill installation does not need fixtures.")
    for skill, (source, filename) in MAPPING.items():
        content = (FIXTURE / source).read_text(encoding="utf-8")
        target = ROOT / "skills" / skill / "references" / filename
        notice = ("> Ví dụ đầy đủ từ fixture giả lập. Không sao chép IDs, hashes, policy hay approval sang project thật. "
                  "Khi dùng như template, thay dữ liệu bằng nguồn project đích; đọc schema và giữ headings. "
                  "Đây là mẫu hồ sơ làm việc nội bộ, chỉ lưu dưới .temp.")
        if skill in ("ba-business", "ba-spec"):
            notice += ("\n\n> Không copy nguyên mẫu có metadata này vào thư mục PBI. "
                       "Dùng ba_public.py để preview và ba-publish để xuất bản đọc được; "
                       "metadata/BA-DATA/Contract Summary giữ trong .temp/drafts.")
        target.write_text(notice + "\n\n" + content, encoding="utf-8")


if __name__ == "__main__":
    main()
