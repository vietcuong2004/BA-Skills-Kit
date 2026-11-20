"""Render validated working documents as readable PBI handover Markdown.

Metadata, source hashes and BA-DATA remain in canonical drafts under .temp.
The public view is deterministic so validation can detect edits or stale sources.
"""
import re

from ba_core import BAError, walk


SPEC_SECTIONS = [
    "Thông tin PBI", "Mục tiêu", "Phạm vi", "User Story", "Actor, Trigger và điều kiện",
    "Main Flow — Luồng chính", "Alternative Flows — Luồng thay thế", "Exception Flows — Luồng ngoại lệ",
    "Business Rules", "Validation, dữ liệu và trạng thái", "Edge Cases — Tình huống đặc biệt",
    "Acceptance Criteria — Given / When / Then", "Dependencies", "Non-functional Considerations",
    "Open Questions", "Traceability Matrix", "Change Log", "Readiness Checklist",
]
EMPTY = "Chưa ghi nhận trong tài liệu nguồn."
STATES = {"draft": "Bản nháp", "in_review": "Đang review", "approved": "Đã phê duyệt",
          "Confirmed": "Đã xác nhận", "Proposed": "Đề xuất", "Open Question": "Cần làm rõ"}
SPEC_STATUS = {"draft": "Draft", "in_review": "In Review", "approved": "Approved"}
UNCONFIRMED = "[CẦN XÁC NHẬN]"


def cell(value):
    if isinstance(value, list):
        value = ", ".join(map(str, value)) or "—"
    return str(value).replace("&", "&amp;").replace("|", "&#124;").replace("\r", "").replace("\n", "<br>")


def table(headers, rows):
    rows = list(rows)
    if not rows:
        return EMPTY
    return ("| " + " | ".join(map(cell, headers)) + " |\n| " + " | ".join("---" for _ in headers) + " |\n" +
            "\n".join("| " + " | ".join(cell(value) for value in row) + " |" for row in rows))


def fact(value):
    if isinstance(value, dict):
        return value["text"] + " (" + STATES.get(value["confirmation_status"], value["confirmation_status"]) + ")"
    return str(value)


def bullets(values):
    return "\n".join("- " + fact(value) for value in values) if values else EMPTY


def unique(values):
    return list(dict.fromkeys(values))


def info(doc, pbi, actors):
    data = doc.data
    return table(["Trường", "Giá trị"], [
        ("PBI ID", data["pbi_id"]), ("Tên", data["title"]),
        ("Epic / Feature", data["epic_id"] + " / " + data["feature_id"]),
        ("Requirement", data["requirement_refs"]), ("Round", data.get("round_id", "Chưa phân bổ")),
        ("Actor", actors), ("Trạng thái", STATES[doc.metadata["status"]]),
        ("Mức độ ưu tiên (đề xuất)", pbi.get("priority_proposal", "Chưa ghi nhận đề xuất ưu tiên")),
    ])


def flows(items):
    rendered = []
    for flow in items:
        details = [
            ("Điểm rẽ nhánh", flow["branch_point"]), ("Trigger", flow["trigger"]),
            ("Kết thúc", flow["termination"]), ("Kết quả", flow["expected_outcome"]),
            ("Dữ liệu / trạng thái", flow["data_state"]), ("Phản hồi", flow["feedback"]),
            ("Phục hồi", flow["recovery"]), ("Liên kết yêu cầu", ", ".join(flow["requirement_refs"])),
            ("Quy tắc liên quan", ", ".join(flow["related_br_refs"]) or "Chưa ghi nhận"),
            ("Trạng thái", STATES[flow["confirmation_status"]]),
        ]
        steps = table(["Bước", "Người dùng", "Hệ thống", "Dữ liệu vào", "Kết quả"], [
            (s["step"], s["actor_action"], s["system_action"], s["input"], s["result"]) for s in flow["steps"]])
        rendered.append(f"### {flow['flow_id']} — {flow['title']}\n\n" +
                        "\n".join(f"- **{label}:** {value}" for label, value in details[:2]) +
                        "\n\n" + steps + "\n\n" +
                        "\n".join(f"- **{label}:** {value}" for label, value in details[2:]))
    return "\n\n".join(rendered) if rendered else EMPTY


def rules(items):
    return table(["ID", "Quy tắc", "Yêu cầu", "Trạng thái"], [
        (x["br_id"], x["title"] + ": " + x["rule"], x["requirement_refs"], STATES[x["confirmation_status"]]) for x in items])


def history(items):
    return table(["Thời điểm", "Thay đổi", "ID bị ảnh hưởng", "Lý do"], [
        (x["at"], x["change"], x["affected_ids"], x["reason"]) for x in items])


def render_legacy_spec(doc, sources):
    data = doc.data
    business = sources.get("business", {})
    requirements = sources.get("requirements", {})
    backlog = sources.get("product-backlog", {})
    pbi = next((p for p in backlog.get("pbis", []) if p["pbi_id"] == data["pbi_id"]), {})
    actors = unique([story["as_a"] for story in data["user_stories"]])
    main = [flow for flow in data["flows"] if flow["kind"] == "main"]
    goals = bullets(business.get("goals", []))
    if business.get("business_value"):
        goals += "\n\n**Giá trị kỳ vọng:** " + fact(business["business_value"])
    scope = "### 3.1. In Scope\n\n" + bullets(data["scope"]) + "\n\n### 3.2. Out of Scope\n\n" + bullets(data["out_of_scope"])
    stories = "\n\n".join(f"Là {s['as_a']}, tôi muốn {s['i_want']} để {s['so_that']}." for s in data["user_stories"])
    conditions = ("**Actor:** " + ", ".join(actors) + "\n\n**Trigger:**\n\n" + bullets(unique([f["trigger"] for f in main])) +
                  "\n\n**Preconditions — Điều kiện trước:**\n\n" + bullets(data["preconditions"]) +
                  "\n\n**Postconditions — Điều kiện sau:**\n\n" + bullets(data["postconditions"]))
    states = ("### Dữ liệu và trạng thái\n\n" + bullets(data["data_states"]) +
              "\n\n### Quyền thực hiện\n\n" + bullets(data["permissions"]))
    edge_cases = table(["ID", "Tình huống / điều kiện", "Kết quả mong đợi / câu hỏi", "Rule", "AC", "Trạng thái"], [
        (x["ec_id"], x["title"] + ": " + x["scenario"] + ("; " + "; ".join(x["preconditions"]) if x["preconditions"] else ""),
         "\n".join(x[k] for k in ("expected_behavior", "open_question") if k in x), x["related_br_refs"],
         x["related_ac_refs"], STATES[x["confirmation_status"]]) for x in data["edge_cases"]])
    acceptance = "\n\n".join(
        f"### {x['ac_id']} — {x['title']}\n\n- **Given:** {x['given']}\n- **When:** {x['when']}\n- **Then:** {x['then']}\n\n"
        f"**Trạng thái:** {STATES[x['confirmation_status']]}\n\n"
        f"**Liên kết:** {', '.join(x['requirement_refs'] + x['flow_refs'] + x['edge_case_refs'])}"
        for x in data["acceptance_criteria"])
    questions = unique(data["open_questions"] + business.get("open_questions", []))
    trace = table(["Requirement", "Business Rule", "Flow", "Edge Case", "Acceptance Criteria"], [
        (x["requirement_id"], x["br_refs"], x["flow_refs"], x["ec_refs"], x["ac_refs"]) for x in data["traceability"]])
    unconfirmed = any(value != "Confirmed" for source in (data, business)
                      for key, value, _ in walk(source) if key == "confirmation_status")
    blockers = unique(data["blockers"] + business.get("blockers", []))
    checks = [(bool(stories and data["scope"]), "Có User Story và phạm vi."),
              (bool(main), "Có luồng chính với các bước xử lý."),
              (any(f["kind"] == "alternative" for f in data["flows"]), "Có luồng thay thế."),
              (any(f["kind"] == "exception" for f in data["flows"]), "Có luồng ngoại lệ."),
              (bool(data["acceptance_criteria"]), "Có Acceptance Criteria dạng Given / When / Then."),
              (bool(data["traceability"]), "Có bảng truy vết."),
              (bool(business) and not unconfirmed and not questions, "Đã xác nhận các nội dung nghiệp vụ và câu hỏi mở."),
              (bool(business) and not blockers, "Không có vấn đề chặn được ghi nhận.")]
    readiness = "\n".join(f"- [{'x' if done else ' '}] {text}" for done, text in checks)
    readiness += "\n\n**Trạng thái tài liệu:** " + STATES[doc.metadata["status"]] + "."
    if not business:
        readiness += "\n\nChưa đối chiếu với tài liệu nghiệp vụ của PBI."
    if unconfirmed or questions:
        readiness += "\n\nCác nội dung Đề xuất / Cần làm rõ phải được xác nhận trước khi cam kết triển khai."
    if blockers:
        readiness += "\n\n**Vấn đề chặn:**\n\n" + bullets(blockers)
    contents = [info(doc, pbi, actors), goals, scope, stories, conditions,
                flows(main), flows([f for f in data["flows"] if f["kind"] == "alternative"]),
                flows([f for f in data["flows"] if f["kind"] == "exception"]), rules(data["business_rules"]), states,
                edge_cases, acceptance, bullets(unique(business.get("dependencies", []) + pbi.get("dependencies", []))),
                bullets(requirements.get("nonfunctional", [])), bullets(questions), trace, history(data["change_history"]), readiness]
    return f"# {data['pbi_id']} — {data['title']}\n\n" + "\n\n".join(
        f"## {i}. {heading}\n\n{body}" for i, (heading, body) in enumerate(zip(SPEC_SECTIONS, contents), 1)) + "\n"


def render_legacy_business(doc, sources):
    data = doc.data
    pbi = next((p for p in sources.get("product-backlog", {}).get("pbis", []) if p["pbi_id"] == data["pbi_id"]), {})
    selected_rules = [r for r in sources.get("requirements", {}).get("business_rules", []) if r["br_id"] in data["business_rule_refs"]]
    solution = []
    for item in data["solution"]:
        solution.append(table(["Nội dung", "Mô tả"], [
            ("Điểm vào", item["entry_point"]), ("Thành phần giao diện", item["ui_components"]),
            ("Thao tác", item["actions"]), ("Dữ liệu / trạng thái", item["data_state"]),
            ("Phản hồi", item["feedback"]), ("Quyền", item["permission"]),
            ("Quy tắc liên quan", item["business_rule_refs"]), ("Trạng thái", STATES[item["confirmation_status"]]),
        ]))
    sections = [
        ("Thông tin PBI", info(doc, pbi, data["target_users"])), ("Câu chuyện nghiệp vụ", fact(data["business_story"])),
        ("Vấn đề", bullets(data["problems"])), ("Đối tượng", bullets(data["target_users"])),
        ("Mục tiêu và giá trị", bullets(data["goals"]) + "\n\n**Giá trị:** " + fact(data["business_value"])),
        ("As-Is / To-Be", "### Hiện tại\n\n" + bullets(data["as_is"]) + "\n\n### Mong muốn\n\n" + bullets(data["to_be"])),
        ("Giải pháp phần mềm chi tiết", "\n\n".join(solution)),
        ("Phạm vi", "### In Scope\n\n" + bullets(data["scope"]) + "\n\n### Out of Scope\n\n" + bullets(data["out_of_scope"])),
        ("Business Rules", rules(selected_rules)), ("Dependencies", bullets(data["dependencies"])),
        ("Risks", bullets(data["risks"])), ("Open Questions", bullets(data["open_questions"])),
        ("Vấn đề chặn", bullets(data["blockers"])), ("Change Log", history(data["change_history"])),
    ]
    return f"# {data['pbi_id']} — {data['title']}\n\n**Tài liệu nghiệp vụ**\n\n" + "\n\n".join(
        f"## {i}. {heading}\n\n{body}" for i, (heading, body) in enumerate(sections, 1)) + "\n"


def qualified(text, status):
    if status != "Confirmed":
        return f"{text} {UNCONFIRMED} ({STATES[status]})"
    return text


def handover_fact(item):
    return qualified(item["text"], item["confirmation_status"])


def labeled_list(label, items):
    return f"**{label}:**\n\n{bullets(items)}" if items else ""


def blocks(*parts):
    return "\n\n".join(part for part in parts if part)


def render_business(doc, sources):
    data = doc.data
    handover = data.get("handover", {})
    requirements = sources.get("requirements", {})
    selected_rules = [qualified(f"{r['br_id']} — {r['rule']}", r["confirmation_status"])
                      for r in requirements.get("business_rules", []) if r["br_id"] in data["business_rule_refs"]]
    goals = [handover_fact(x) for x in data["goals"] if x != data["business_value"]]
    purpose = handover_fact(handover["purpose"]) if handover else blocks(
        handover_fact(data["business_story"]), labeled_list("Mục tiêu", goals),
        "**Giá trị nghiệp vụ:** " + handover_fact(data["business_value"]))
    needs = handover.get("customer_needs", data["to_be"])
    context = blocks("**Câu chuyện nghiệp vụ:** " + handover_fact(data["business_story"]),
                     labeled_list("Hiện trạng", [handover_fact(x) for x in data["as_is"]]),
                     labeled_list("Khó khăn", [handover_fact(x) for x in data["problems"]]),
                     labeled_list("Nhu cầu KH", [handover_fact(x) for x in needs]),
                     labeled_list("Quy tắc nghiệp vụ", selected_rules))
    locations = unique([x["entry_point"] for x in data["solution"]])
    if handover:
        sections = []
        for i, item in enumerate(handover["solution_sections"], 1):
            grid = item.get("table")
            sections.append(blocks(f"### 3.{i}. {qualified(item['title'], item['confirmation_status'])}",
                                   *[handover_fact(x) for x in item["paragraphs"]],
                                   table(grid["columns"], grid["rows"]) if grid else ""))
    else:
        headers = ["Vị trí / thành phần", "Thao tác", "Dữ liệu / xử lý", "Phản hồi", "Quyền / quy tắc"]
        rows = [(qualified(x["entry_point"], x["confirmation_status"]) +
                 (" — " + ", ".join(x["ui_components"]) if x["ui_components"] else ""),
                 x["actions"], x["data_state"], x["feedback"], ", ".join([x["permission"], *x["business_rule_refs"]]))
                for x in data["solution"]]
        sections = ["### 3.1. Quy định xử lý\n\n" + table(headers, rows)]
    affected = [handover_fact(x) for x in handover["affected_areas"]] if handover else data["scope"]
    solution = blocks(labeled_list("Vị trí áp dụng", locations), *sections,
                      labeled_list("Lưu ý", [handover_fact(x) for x in handover.get("notes", [])]),
                      labeled_list("Phạm vi ảnh hưởng", affected),
                      labeled_list("Ngoài phạm vi", data["out_of_scope"]),
                      labeled_list("Phụ thuộc", data["dependencies"]),
                      labeled_list("Rủi ro", data["risks"]),
                      labeled_list("Cần xác nhận", data["open_questions"] + data["blockers"]))
    quality = [handover_fact(x) for x in handover.get("quality_constraints", [])]
    return blocks("# Đặc tả yêu cầu nghiệp vụ", f"## {data['title']}",
                  f"**PBI:** {data['pbi_id']}  \n**Vòng lặp:** {data.get('round_id', 'Chưa phân bổ')}",
                  "## 1. Mục đích\n\n" + purpose, "## 2. Nghiệp vụ\n\n" + context,
                  "## 3. Giải pháp phần mềm\n\n" + solution,
                  "## 4. Yêu cầu hiệu năng, bảo mật\n\n" + bullets(quality) if quality else "") + "\n"


def acceptance_scenarios(items):
    scenarios = []
    for i, item in enumerate(items, 1):
        outcome = item["then"].rstrip()
        if not outcome.endswith((".", "!", "?")):
            outcome += "."
        scenarios.append(f"{i}. **Given** {item['given']}, **When** {item['when']}, "
                         f"**Then** {qualified(outcome, item['confirmation_status'])}")
    return "\n".join(scenarios) or UNCONFIRMED


def render_spec(doc, sources):
    data = doc.data
    handover = data.get("handover", {})
    business = sources.get("business", {})
    requirements = sources.get("requirements", {})
    created = handover.get("created", "[CHƯA CÓ]")
    branch = handover.get("feature_branch")
    specs = [("Feature Branch", f"`{branch}`" if branch else "[CHƯA CÓ]"),
             ("Created", created), ("Status", SPEC_STATUS[doc.metadata["status"]]),
             ("PBI", data["pbi_id"]), ("Platform", handover.get("platform", "[CHƯA CÓ]")),
             ("Vòng phát hành", data.get("round_id", "Chưa phân bổ"))]
    header = "  \n".join(f"**{label}:** {value}" for label, value in specs)
    header += f"\n\n**Link Figma:** {handover.get('figma_url', '[CHƯA CÓ]')}"
    acceptance = {item["ac_id"]: item for item in data["acceptance_criteria"]}
    stories = []
    for i, story in enumerate(data["user_stories"], 1):
        details = handover["stories"][i - 1] if handover else {}
        title = details.get("title", story["i_want"])
        priority = details.get("priority", UNCONFIRMED)
        if handover:
            independent_test = " → ".join(details["independent_test"])
            scenarios = [acceptance[ref] for ref in details["ac_refs"]]
        elif len(data["user_stories"]) == 1:
            main = next(flow for flow in data["flows"] if flow["kind"] == "main")
            independent_test = " → ".join([main["trigger"], *[step["actor_action"] for step in main["steps"]],
                                           qualified(main["expected_outcome"], main["confirmation_status"])])
            scenarios = list(acceptance.values())
        else:
            independent_test, scenarios = UNCONFIRMED, []
        stories.append(blocks(f"### User Story {i} — {title} (Priority: {priority})",
                              f"Là {story['as_a']}, tôi muốn {story['i_want']}, để {story['so_that']}.",
                              f"**Why this priority:** {details.get('priority_reason', UNCONFIRMED)}",
                              f"**Independent Test:** {independent_test}",
                              "**Acceptance Scenarios:**\n\n" + acceptance_scenarios(scenarios)))
    if not handover and len(stories) > 1:
        stories.append("### Acceptance Scenarios cần gắn với User Story\n\n" +
                       acceptance_scenarios(acceptance.values()))
    edges = []
    for item in data["edge_cases"]:
        conditions = item["scenario"]
        if item["preconditions"]:
            conditions += f" (Điều kiện trước: {', '.join(item['preconditions'])})"
        outcome = qualified(item["expected_behavior"], item["confirmation_status"]) if "expected_behavior" in item else ""
        question = f"{UNCONFIRMED} {item['open_question']}" if "open_question" in item else ""
        edges.append(f"**{item['title']}:** {conditions} → {outcome or question}" +
                     (f" {question}" if outcome and question else ""))
    if handover:
        functional = [f"**{x['fr_id']}:** {handover_fact(x)}" for x in handover["functional_requirements"]]
        nonfunctional = [f"**{x['nfr_id']}:** {handover_fact(x)}" for x in handover["nonfunctional_requirements"]]
        criteria = [handover_fact(x) for x in handover["success_criteria"]]
        assumptions = [handover_fact(x) for x in handover["assumptions"]]
        dependencies = [handover_fact(x) for x in handover["dependencies"]]
    else:
        selected = [r for r in requirements.get("requirements", []) if r["requirement_id"] in data["requirement_refs"]]
        functional = [f"**FR-{r['requirement_id'].split('-')[1]}:** " +
                      qualified(f"Khi {r['trigger']}: {r['expected_outcome']}", r["confirmation_status"]) for r in selected]
        functional.extend(qualified(f"**{x['br_id']}:** {x['rule']}", x["confirmation_status"])
                          for x in data["business_rules"])
        functional.extend(handover_fact(x) for x in data["permissions"] + data["data_states"])
        nonfunctional = [f"**NFR-{i:03}:** {handover_fact(x)}"
                         for i, x in enumerate(requirements.get("nonfunctional", []), 1)]
        criteria = unique([qualified(x["then"], x["confirmation_status"]) for x in acceptance.values()])
        assumptions = [handover_fact(x) for x in business.get("as_is", [])]
        dependencies = []
    assumptions.extend(f"{UNCONFIRMED} {x}" for x in unique(
        data["open_questions"] + data["blockers"] + business.get("open_questions", []) + business.get("blockers", [])))
    pbi = next((p for p in sources.get("product-backlog", {}).get("pbis", []) if p["pbi_id"] == data["pbi_id"]), {})
    for ref in unique(pbi.get("dependencies", []) + business.get("dependencies", [])):
        if not any(re.search(r"(?<![\w-])" + re.escape(ref) + r"(?![\w-])", item) for item in dependencies):
            dependencies.append(ref)
    return blocks(f"# Feature Specification: {data['title']}", header,
                  "## User Scenarios & Testing", *stories,
                  "## Edge Cases", bullets(edges),
                  "## Requirements", "### Functional Requirements", bullets(functional),
                  "### Non-Functional Requirements", bullets(nonfunctional),
                  "## Success Criteria", bullets(criteria),
                  "## Assumptions", bullets(assumptions),
                  "## Dependencies", bullets(dependencies)) + "\n"


def check_public_text(text, path=""):
    if (text.lstrip().startswith("---") or "<!-- BA-DATA:" in text or "## Contract Summary" in text or
            re.search(r"^\x60{3}(?:yaml|json)\b|^(?:schema_version|document_type|project_id|source_documents|generated_by|sha256):", text, re.M)):
        raise BAError("PUBLIC_METADATA", "PBI handover files must contain readable prose, not BA metadata", path,
                      fix="Giữ bản có metadata trong .temp/drafts; xuất bản đọc được bằng publish_ba.py.")


def render_public(doc, sources=None, *, legacy=False):
    kind = doc.metadata["document_type"]
    if kind not in ("business", "spec"):
        raise BAError("WRONG_DOCUMENT_TYPE", "Only business/spec have public handover views", doc.path)
    if legacy:
        renderer = render_legacy_spec if kind == "spec" else render_legacy_business
    else:
        renderer = render_spec if kind == "spec" else render_business
    text = renderer(doc, sources or {})
    check_public_text(text, doc.path)
    return text


def public_bytes(project, doc, validator, *, legacy=False):
    """Use only the draft's actual, validated direct sources as rendering context."""
    sources = {}
    for entry in doc.metadata["source_documents"]:
        path = project.path(entry["path"])
        if entry.get("kind", "ba" if path.suffix.lower() == ".md" else "raw") == "ba":
            source = validator.require_valid(path)
            sources.setdefault(source.metadata["document_type"], source.data)
    return render_public(doc, sources, legacy=legacy).encode("utf-8")


def main():
    import argparse
    import json
    from ba_core import Project, Validator

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-config", help="Path to .temp/ba-project.yaml (defaults to this path in the working directory)")
    parser.add_argument("--file", required=True, help="Canonical business/spec draft under .temp")
    parser.add_argument("--write-preview", action="store_true", help="Write only to .temp/previews/PBI-ID/")
    args = parser.parse_args()
    try:
        project = Project.load(args.project_config)
        source = project.temporary_path(args.file)
        validator = Validator(project)
        doc = validator.require_valid(source)
        content = public_bytes(project, doc, validator)
        if args.write_preview:
            target = project.temporary_path(project.temp / "previews" / doc.data["pbi_id"] / (doc.metadata["document_type"] + ".md"))
            if target in validator.fingerprints:
                raise BAError("PREVIEW_CONFLICT", "Preview would overwrite an input document", target)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            print(json.dumps({"preview": project.relative(target)}, ensure_ascii=False))
        else:
            print(content.decode("utf-8"), end="")
        return 0
    except (BAError, OSError) as exc:
        issue = exc.diagnostic if isinstance(exc, BAError) else BAError("IO_ERROR", str(exc)).diagnostic
        print(json.dumps({"diagnostics": [issue]}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
