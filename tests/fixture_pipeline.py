"""Deterministic integration driver. Test decisions are synthetic, never human approvals.

Each stage reads the previous stage's validated file. This is NOT an LLM invocation.
"""
import json
import sys
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from ba_core import HEADINGS, Project, Validator, parse, render, sha
from publish_ba import prepare, publish

IDEA = "Tôi muốn xây dựng website ghi chú cá nhân, ghi chú công ty, tạo tài liệu từ mẫu và tìm kiếm."


def fact(text, status="Proposed"):
    return {"text": text, "confirmation_status": status, "source_refs": ["idea.txt: yêu cầu người dùng giả lập"]}


def flow(identifier, kind, requirement, title, trigger, outcome):
    return {"flow_id": identifier, "kind": kind, "title": title, "trigger": trigger,
            "branch_point": "Bắt đầu" if kind == "main" else "MF-001 bước 1",
            "steps": [{"step": 1, "actor_action": trigger, "system_action": outcome,
                       "input": "Nội dung hoặc từ khóa người dùng nhập", "result": outcome}],
            "termination": "Kết thúc với phản hồi rõ ràng", "expected_outcome": outcome,
            "data_state": "Chỉ cập nhật khi thao tác thành công", "feedback": outcome,
            "recovery": "Giữ nội dung để thử lại khi lỗi", "requirement_refs": [requirement],
            "related_br_refs": ["BR-001"], "confirmation_status": "Proposed"}


def write_document(project, kind, data, sources, relative=None, sections=None):
    path = project.path(relative or project.planning / f"{kind}.md")
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = {"schema_version": "1.0", "document_type": kind, "project_id": project.config["project_id"],
            "status": "draft", "source_documents": [{"path": project.relative(p), "sha256": sha(p)} for p in sources],
            "generated_by": "ba-workflow" if kind == "workflow-state" else "ba-" + kind}
    for field in ("pbi_id", "epic_id", "feature_id", "round_id", "requirement_refs"):
        if field in data:
            meta[field] = data[field]
    if sections is None:
        sections = {h: f"Fixture {kind}: {data.get('title', 'Example Notes')}. Các nội dung Proposed cần quyết định của người dùng giả lập."
                    for h in HEADINGS[kind]}
    path.write_text(render(meta, data, sections), encoding="utf-8")
    Validator(project).require_valid(path, kind, data.get("pbi_id"))
    return path


def source(project, kind):
    return Validator(project).require_valid(project.planning / f"{kind}.md", kind)


def brainstorm(project):
    idea = project.path("idea.txt").read_text(encoding="utf-8")
    data = {"product_overview": fact(idea, "Confirmed"), "vision": fact("Tìm lại tài liệu cá nhân và công ty trong cùng sản phẩm"),
        "target_users": ["Cá nhân", "Thành viên công ty"], "problems": [fact("Tài liệu phân tán khó tìm lại")],
        "jobs_to_be_done": [fact("Soạn và tìm tài liệu trong không gian phù hợp")],
        "capabilities": [{"capability_id": "CAP-001", "name": "Soạn và tìm tài liệu theo không gian",
            "description": idea, "target_users": ["Cá nhân", "Thành viên công ty"], "business_value": "Tái sử dụng tri thức",
            "source_refs": ["idea.txt"], "confirmation_status": "Confirmed"}],
        "goals": [fact("Tạo ghi chú từ trắng hoặc mẫu, sau đó tìm lại")],
        "scope": [fact("Ghi chú cá nhân, ghi chú công ty, tạo từ mẫu, tìm kiếm", "Confirmed")],
        "exclusions": [fact("Không xác định cộng tác thời gian thực trong vòng phân tích này")],
        "constraints": [], "assumptions": [fact("Người dùng đã đăng nhập")], "open_questions": ["Ai quản lý mẫu của công ty?"],
        "metrics": [], "change_history": []}
    return write_document(project, "brainstorm", data, [project.path("idea.txt")])


def requirements(project):
    discovery = source(project, "brainstorm")
    cap = discovery.data["capabilities"][0]
    reqs = []
    for number, title, trigger, outcome in [
        (1, "Tạo ghi chú cá nhân/công ty từ trắng hoặc mẫu", "Chọn không gian và cách tạo", "Ghi chú được lưu ở không gian đã chọn"),
        (2, "Tìm ghi chú được phép xem", "Nhập từ khóa", "Trả về ghi chú phù hợp trong phạm vi được phép")]:
        reqs.append({"requirement_id": f"REQ-{number:03d}", "title": title, "description": outcome,
            "actor": "ACT-001", "trigger": trigger, "preconditions": ["Đã đăng nhập"], "expected_outcome": outcome,
            "capability_refs": [cap["capability_id"]], "source_refs": [f"brainstorm.md#{cap['capability_id']}"],
            "confirmation_status": "Proposed", "business_rule_refs": ["BR-001"]})
    rule = {"br_id": "BR-001", "title": "Giới hạn theo quyền không gian", "rule": "Chỉ truy cập tài liệu trong phạm vi được cấp quyền",
            "requirement_refs": [r["requirement_id"] for r in reqs], "source_refs": ["brainstorm.md#CAP-001"], "confirmation_status": "Proposed"}
    data = {"actors": [{"actor_id": "ACT-001", "name": discovery.data["target_users"][0], "role": "Người soạn/tìm tài liệu"}],
            "requirements": reqs, "business_rules": [rule], "data": [fact("Ghi chú có nội dung và không gian sở hữu")],
            "permissions": [fact(rule["rule"])], "as_is": [],
            "flows": [flow("MF-001", "main", reqs[0]["requirement_id"], reqs[0]["title"], reqs[0]["trigger"], reqs[0]["expected_outcome"])],
            "edge_cases": [], "nonfunctional": [fact("Chưa xác định tải và mục tiêu độ trễ; cần đo trước khi chốt")],
            "open_questions": discovery.data["open_questions"], "change_history": []}
    return write_document(project, "requirements", data, [discovery.path])


def backlog(project):
    discovery, reqdoc = source(project, "brainstorm"), source(project, "requirements")
    reqs = reqdoc.data["requirements"]
    pbis = []
    for index, req in enumerate(reqs, 1):
        pbis.append({"pbi_id": f"{project.config['pbi_prefix']}-{index:03d}", "epic_id": "EPIC-001", "feature_id": "FEAT-001",
            "title": req["title"], "user_story": f"Là người dùng, tôi muốn {req['title'].lower()} để tái sử dụng tri thức.",
            "business_value": "Tạo hoặc tìm lại tri thức trong phạm vi được phép", "scope": [req["expected_outcome"]],
            "out_of_scope": ["Cộng tác thời gian thực"], "requirement_refs": [req["requirement_id"]],
            "dependencies": [] if index == 1 else [f"{project.config['pbi_prefix']}-001"],
            "priority_proposal": "Tạo trước, tìm sau để kiểm chứng hành trình", "estimation_status": "Unestimated",
            "confirmation_status": req["confirmation_status"], "open_questions": [],
            "invest": {k: v for k, v in zip(["independent", "negotiable", "valuable", "estimable", "small", "testable"],
                ["Nêu dependency rõ", "Phạm vi còn thương lượng", "Có kết quả người dùng nhận được", "Cần refinement trước ước lượng", "Một kết quả đầu cuối", "Có thể quan sát kết quả"])} })
    data = {"epics": [{"epic_id": "EPIC-001", "title": "Tri thức theo không gian", "business_value": discovery.data["capabilities"][0]["business_value"]}],
            "features": [{"feature_id": "FEAT-001", "epic_id": "EPIC-001", "title": "Vòng đời ghi chú",
                          "requirement_refs": [r["requirement_id"] for r in reqs]}],
            "pbis": pbis, "unassigned_requirements": [], "change_history": []}
    return write_document(project, "product-backlog", data, [discovery.path, reqdoc.path])


def round_plan(project):
    backlog_doc, reqdoc = source(project, "product-backlog"), source(project, "requirements")
    data = {"rounds": [{"round_id": project.config["round_prefix"] + "1", "goal": "Kiểm chứng hành trình tạo và tìm ghi chú",
            "status": "Proposed", "pbi_refs": [p["pbi_id"] for p in backlog_doc.data["pbis"]], "dependencies": [],
            "risks": ["Chưa rõ capacity"], "capacity_assumptions": [], "capacity_gaps": ["Cần capacity trước cam kết"],
            "allocation_rationale": "Tạo tài liệu trước khi tìm; không cam kết số ngày", "approval_status": "Pending"}],
            "unassigned_pbis": [], "change_history": []}
    return write_document(project, "round-plan", data, [backlog_doc.path, reqdoc.path])


def identity(project, pbi_id):
    b = source(project, "product-backlog")
    pbi = next(p for p in b.data["pbis"] if p["pbi_id"] == pbi_id)
    rnd = next(r for r in source(project, "round-plan").data["rounds"] if pbi_id in r["pbi_refs"])
    return pbi, {k: pbi[k] for k in ("pbi_id", "epic_id", "feature_id", "title", "requirement_refs")} | {"round_id": rnd["round_id"]}


def business(project, pbi_id):
    pbi, fields = identity(project, pbi_id)
    data = {**fields, "business_story": fact(pbi["user_story"]), "problems": [fact("Khó lưu lại và tìm lại tri thức đúng không gian")],
            "target_users": source(project, "brainstorm").data["target_users"], "goals": [fact(pbi["scope"][0])],
            "business_value": fact(pbi["business_value"]), "as_is": [], "to_be": [fact(pbi["scope"][0])],
            "solution": [{"entry_point": "Không gian đã chọn", "ui_components": ["Bộ chọn không gian", "Trình soạn thảo hoặc tìm kiếm (Proposed)"],
                "actions": [pbi["title"]], "data_state": "Lưu kết quả chỉ sau khi kiểm tra quyền", "feedback": pbi["scope"][0],
                "permission": "Kiểm tra quyền tại lúc thực hiện", "business_rule_refs": ["BR-001"],
                "confirmation_status": "Proposed", "source_refs": ["requirements.md#" + pbi["requirement_refs"][0]]}],
            "scope": pbi["scope"], "out_of_scope": pbi["out_of_scope"], "business_rule_refs": ["BR-001"],
            "dependencies": pbi["dependencies"], "risks": ["Cần xác nhận chi tiết UI"], "open_questions": [], "blockers": [], "change_history": []}
    return write_document(project, "business", data, [source(project, t).path for t in ("brainstorm", "requirements", "product-backlog", "round-plan")],
                          project.planning / "drafts" / pbi_id / "business.md")


def spec(project, pbi_id):
    bus = Validator(project).require_valid(project.planning / "drafts" / pbi_id / "business.md", "business", pbi_id)
    reqdoc = source(project, "requirements")
    pbi, fields = identity(project, pbi_id)
    requirement = next(r for r in reqdoc.data["requirements"] if r["requirement_id"] in bus.data["requirement_refs"])
    rid = requirement["requirement_id"]
    flows = [flow("MF-001", "main", rid, "Hoàn thành thao tác", requirement["trigger"], requirement["expected_outcome"]),
             flow("AF-001", "alternative", rid, "Hủy thao tác", "Người dùng chọn hủy", "Không thay đổi dữ liệu"),
             flow("EF-001", "exception", rid, "Quyền thay đổi", "Quyền không còn hợp lệ lúc thực hiện", "Từ chối và không lộ nội dung không được phép")]
    ec = {"ec_id": "EC-001", "title": "Quyền bị thu hồi", "scenario": "Quyền thay đổi sau khi mở màn hình",
          "preconditions": ["Đã mở màn hình với quyền hợp lệ"], "expected_behavior": flows[2]["expected_outcome"],
          "requirement_refs": [rid], "related_br_refs": ["BR-001"], "related_ac_refs": ["AC-003"], "confirmation_status": "Proposed"}
    acs = [{"ac_id": f"AC-{i:03d}", "title": f["title"], "given": "Đã chọn không gian và đăng nhập",
            "when": f["trigger"], "then": f["expected_outcome"], "requirement_refs": [rid], "flow_refs": [f["flow_id"]],
            "edge_case_refs": [ec["ec_id"]] if i == 3 else [], "confirmation_status": "Proposed"} for i, f in enumerate(flows, 1)]
    rules = [dict(rule, requirement_refs=[rid]) for rule in reqdoc.data["business_rules"] if rid in rule["requirement_refs"]]
    data = {**fields, "user_stories": [{"as_a": bus.data["target_users"][0], "i_want": pbi["title"], "so_that": pbi["business_value"]}],
            "preconditions": requirement["preconditions"], "postconditions": [requirement["expected_outcome"]], "flows": flows,
            "business_rules": rules, "permissions": reqdoc.data["permissions"], "data_states": [fact("Không thay đổi dữ liệu khi hủy hoặc bị từ chối")],
            "edge_cases": [ec], "acceptance_criteria": acs,
            "traceability": [{"requirement_id": rid, "br_refs": [r["br_id"] for r in rules], "flow_refs": [f["flow_id"] for f in flows],
                              "ec_refs": [ec["ec_id"]], "ac_refs": [a["ac_id"] for a in acs]}],
            "scope": bus.data["scope"], "out_of_scope": bus.data["out_of_scope"], "open_questions": [], "blockers": [], "change_history": []}
    return write_document(project, "spec", data, [bus.path, reqdoc.path, source(project, "product-backlog").path],
                          project.planning / "drafts" / pbi_id / "spec.md")


def review(project, pbi_id):
    bus = Validator(project).require_valid(project.planning / "drafts" / pbi_id / "business.md", "business", pbi_id)
    specdoc = Validator(project).require_valid(project.planning / "drafts" / pbi_id / "spec.md", "spec", pbi_id)
    _, fields = identity(project, pbi_id)
    data = {**fields, "result": "PASS", "readiness": "Ready", "blockers": [], "findings": [],
            "coverage_notes": [f"Synthetic contract fixture: {len(specdoc.data['acceptance_criteria'])} AC, GWT and refs valid. Not an independent BA quality verdict."],
            "change_history": []}
    return write_document(project, "review", data, [bus.path, specdoc.path, source(project, "requirements").path, source(project, "product-backlog").path],
                          project.planning / "reviews" / f"{pbi_id}-review.md")


def approve_fixture(project, pbi_id):
    """Test double ONLY. Do not use this to approve a real project."""
    b, r = source(project, "product-backlog").path, source(project, "round-plan").path
    pair = [project.planning / "drafts" / pbi_id / f"{t}.md" for t in ("business", "spec")]
    rev = project.planning / "reviews" / f"{pbi_id}-review.md"
    approvals = []
    for phase, decision, paths in [("backlog", "Approved", [b]), ("round-plan", "Proposed Allowed", [r]),
                                   ("publish", "Draft Publication", [b, r, *pair, rev])]:
        approvals.append({"checkpoint": phase, "decision": decision, "actor": "TEST HUMAN DOUBLE",
            "evidence": "Synthetic approval for automated tests only; no real user approval is asserted.",
            "decided_at": "2026-11-17T00:00:00+07:00", "pbi_refs": [pbi_id],
            "documents": [{"path": project.relative(p), "sha256": sha(p)} for p in paths], "resolved_decisions": []})
    target = project.planning / "approvals.json"
    target.write_text(json.dumps({"schema_version": "1.0", "project_id": project.config["project_id"], "approvals": approvals},
                                 ensure_ascii=False, indent=2), encoding="utf-8")
    return target


def workflow(project, pbi_id, paths):
    data = {"mode": "DRAFT", "current_phase": "publish-checkpoint", "completed": ["ba-" + parse(p).metadata["document_type"] for p in paths],
            "pending": ["human-publish-checkpoint"], "blockers": [],
            "artifacts": [{"path": project.relative(p), "sha256": sha(p)} for p in paths], "approvals": [],
            "last_updated": "2026-11-17T00:00:00+07:00", "selected_pbis": [pbi_id], "change_history": []}
    return write_document(project, "workflow-state", data, [])


def build(root, *, publish_pair=False, pbi_prefix="PBI", round_prefix="R"):
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    if (root / "ba-project.yaml").exists():
        raise ValueError("Fixture destination already exists; use a fresh isolated directory")
    cfg = yaml.safe_load((Path(__file__).resolve().parents[1] / "templates" / "ba-project.example.yaml").read_text(encoding="utf-8"))
    cfg.update(pbi_prefix=pbi_prefix, round_prefix=round_prefix)
    (root / "ba-project.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    (root / "idea.txt").write_text(IDEA, encoding="utf-8")
    project = Project.load(root / "ba-project.yaml")
    paths = [brainstorm(project), requirements(project), backlog(project), round_plan(project)]
    pbi_id = pbi_prefix + "-001"
    paths += [business(project, pbi_id), spec(project, pbi_id), review(project, pbi_id)]
    workflow(project, pbi_id, paths)
    approve_fixture(project, pbi_id)
    if publish_pair:
        publish(project, prepare(project, pbi_id))
    return project


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    parser.add_argument("--publish-fixture", action="store_true")
    args = parser.parse_args()
    project = build(args.output, publish_pair=args.publish_fixture)
    print(project.config_path)
