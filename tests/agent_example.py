"""Replay of the primary agent's in-session BA example, not an independent model eval.

Stages are invoked separately; each validates and reads actual upstream Markdown.
All decisions/approvals are synthetic test scenario data.
"""
import argparse
import json
from pathlib import Path
import yaml
from fixture_pipeline import write_document, source, approve_fixture
from ba_core import HEADINGS, Project, Validator, sha, parse
from publish_ba import prepare, publish

ROOT = Path(__file__).resolve().parent / "fixtures" / "agent-notes"


def fact(text, status="Proposed"):
    return {"text": text, "confirmation_status": status, "source_refs": ["idea.txt", "scenario.txt"]}


def brainstorm():
    ROOT.mkdir(parents=True, exist_ok=True)
    config = yaml.safe_load((Path(__file__).resolve().parents[1] / "templates/ba-project.example.yaml").read_text(encoding="utf-8"))
    config.update(project_id="agent-notes", project_name="Example Notes — in-session BA exercise")
    (ROOT / "ba-project.yaml").write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False), encoding="utf-8")
    (ROOT / "idea.txt").write_text("Tôi muốn website ghi chú cá nhân, ghi chú công ty, tạo tài liệu từ mẫu và tìm kiếm.", encoding="utf-8")
    (ROOT / "scenario.txt").write_text(
        "SYNTHETIC TEST ONLY. Không phải quyết định người dùng thật. Actor: người dùng đã đăng nhập. "
        "Cho lát cắt tạo ghi chú cá nhân: chỉ chủ sở hữu được xem; ghi chú gồm tiêu đề và nội dung, cả hai phải có ít nhất một ký tự không phải khoảng trắng. "
        "Chưa đặt giới hạn độ dài. Khi hủy, không tạo ghi chú. Khi quyền/phiên hết hiệu lực lúc gửi, không lưu và không lộ nội dung. "
        "Một yêu cầu gửi lại cùng thao tác không được tạo bản sao; khi chưa biết kết quả, giữ nội dung và cho kiểm tra kết quả thao tác cũ trước khi gửi lại. "
        "Chính sách công ty, mẫu và tìm kiếm chưa chốt, để Proposed. Test checkpoint: duyệt backlog fixture; "
        "cho phép Round Proposed vì chưa có capacity; chỉ cho phép xuất draft PBI-001 khi review không FAIL. "
        "Đây là test double, tuyệt đối không tái sử dụng cho project thật.", encoding="utf-8")
    p = Project.load(ROOT / "ba-project.yaml")
    names = ["Tạo ghi chú cá nhân", "Ghi chú trong không gian công ty", "Tạo tài liệu từ mẫu", "Tìm kiếm tài liệu"]
    caps = [{"capability_id": f"CAP-{i:03d}", "name": name, "description": name, "target_users": ["Người dùng đã đăng nhập"],
             "business_value": "Lưu và tái sử dụng thông tin theo ngữ cảnh", "source_refs": ["idea.txt"], "confirmation_status": "Confirmed"}
            for i, name in enumerate(names, 1)]
    d = {"product_overview": fact((ROOT / "idea.txt").read_text(encoding="utf-8"), "Confirmed"),
         "vision": fact("Lưu tri thức cá nhân và tổ chức, sau đó tìm lại khi cần."), "target_users": ["Người dùng cá nhân", "Thành viên công ty"],
         "problems": [fact("Ghi chú phân tán làm khó tái sử dụng thông tin.")], "jobs_to_be_done": [fact("Ghi lại thông tin trong không gian phù hợp rồi tìm lại.")],
         "capabilities": caps, "goals": [fact("Kiểm chứng tạo và đọc lại ghi chú cá nhân trước khi mở rộng.")],
         "scope": [fact(", ".join(names), "Confirmed")], "exclusions": [fact("Cộng tác thời gian thực chưa nằm trong ý tưởng đầu vào.")],
         "constraints": [fact("Quy tắc cá nhân được cung cấp trong scenario.txt.", "Confirmed")],
         "assumptions": [fact("Một tài khoản có thể tham gia không gian công ty, cần xác minh.")],
         "open_questions": ["Ai cấp quyền công ty?", "Ai quản lý mẫu?", "Tìm kiếm hỗ trợ phạm vi nào?"], "metrics": [], "change_history": []}
    s = dict(zip(HEADINGS["brainstorm"], [
        "Website ghi chú với bốn nhu cầu được lưu nguyên văn trong idea.txt.",
        "Đề xuất một nơi lưu và tái sử dụng tri thức; chưa có nghiên cứu xác nhận mức độ nhu cầu.",
        "Người dùng cá nhân và thành viên công ty. Vai trò quản trị công ty cần làm rõ.",
        "Giả thuyết: thông tin phân tán khiến khó tìm lại; không phải kết quả nghiên cứu.",
        "Bốn capability: cá nhân, công ty, mẫu và tìm kiếm; không bỏ sót nhu cầu.",
        "Ưu tiên tạo/đọc lại ghi chú cá nhân là đề xuất cần backlog checkpoint.",
        "Bao gồm bốn nhu cầu đã nêu. Cộng tác thời gian thực chưa được yêu cầu.",
        "Chính sách đa không gian cần xác minh; quy tắc fixture cá nhân được cung cấp riêng.",
        "Cần làm rõ quyền công ty, quản lý mẫu và phạm vi tìm kiếm.",
        "Chưa có baseline hoặc KPI; không tự đặt số."]))
    return write_document(p, "brainstorm", d, [ROOT / "idea.txt", ROOT / "scenario.txt"], sections=s)


def requirements(p):
    discovery = source(p, "brainstorm")
    reqs = [{"requirement_id": f"REQ-{i:03d}", "title": cap["name"], "description": cap["description"], "actor": "ACT-001",
             "trigger": ["Chọn tạo ghi chú cá nhân", "Chọn không gian công ty", "Chọn mẫu", "Nhập từ khóa"][i-1],
             "preconditions": ["Người dùng đã đăng nhập"],
             "expected_outcome": ["Ghi chú được lưu riêng cho chủ sở hữu và có thể đọc lại", "Ghi chú thuộc đúng không gian được phép",
                                  "Tài liệu khởi tạo từ mẫu được phép", "Hiển thị tài liệu phù hợp trong phạm vi được phép"][i-1],
             "capability_refs": [cap["capability_id"]], "source_refs": ["brainstorm.md#" + cap["capability_id"], "scenario.txt"],
             "confirmation_status": "Confirmed" if i == 1 else "Proposed", "business_rule_refs": ["BR-001", "BR-002", "BR-003"] if i == 1 else []}
            for i, cap in enumerate(discovery.data["capabilities"], 1)]
    rules = [{"br_id": f"BR-{i:03d}", "title": title, "rule": text, "requirement_refs": [reqs[0]["requirement_id"]],
              "source_refs": ["scenario.txt"], "confirmation_status": "Confirmed"} for i, (title, text) in enumerate([
        ("Sở hữu cá nhân", "Chỉ chủ sở hữu được đọc; kiểm tra phiên/quyền khi gửi, hết quyền thì không lưu."),
        ("Thông tin bắt buộc", "Tiêu đề và nội dung đều có ít nhất một ký tự không phải khoảng trắng; chưa chốt giới hạn độ dài."),
        ("Không lặp tác dụng", "Gửi lại cùng thao tác không tạo bản sao; kết quả chưa rõ thì giữ nội dung và kiểm tra thao tác cũ trước khi gửi lại.")], 1)]
    main = make_flow("MF-001", "main", "Tạo và đọc lại ghi chú", "Gửi nội dung hợp lệ", "Một ghi chú được lưu cho chủ sở hữu và đọc lại được", ["BR-001", "BR-002", "BR-003"])
    d = {"actors": [{"actor_id": "ACT-001", "name": "Người dùng đã đăng nhập", "role": "Chủ sở hữu ghi chú cá nhân hoặc thành viên công ty"}],
         "requirements": reqs, "business_rules": rules, "data": [fact("Ghi chú cá nhân có tiêu đề, nội dung và chủ sở hữu.", "Confirmed")],
         "permissions": [fact(rules[0]["rule"], "Confirmed")], "as_is": [], "flows": [main,
             make_flow("AF-001", "alternative", "Hủy tạo", "Hủy trước khi gửi", "Không tạo ghi chú", []),
             make_flow("EF-001", "exception", "Phiên hết hiệu lực", "Gửi sau khi phiên hết hiệu lực", "Không lưu và không lộ nội dung", ["BR-001"])],
         "edge_cases": [{"ec_id": "EC-001", "title": "Gửi lại khi chưa rõ kết quả", "scenario": "Mất phản hồi sau khi server đã nhận thao tác",
             "preconditions": ["Đã gửi thao tác tạo"], "expected_behavior": rules[2]["rule"], "requirement_refs": ["REQ-001"],
             "related_br_refs": ["BR-003"], "related_ac_refs": [], "confirmation_status": "Confirmed"}],
         "nonfunctional": [fact("Cần đo nhu cầu tải và thời gian phản hồi trước khi chốt chỉ tiêu.")],
         "open_questions": discovery.data["open_questions"], "change_history": []}
    s = dict(zip(HEADINGS["requirements"], [
        "Actor là người dùng đã đăng nhập; vai trò công ty chưa xác định chi tiết.",
        "Bốn REQ tương ứng bốn CAP. Tạo ghi chú cá nhân có hành vi fixture xác nhận; ba nhu cầu còn lại Proposed.",
        "Ba rule cá nhân từ scenario: quyền sở hữu, nội dung bắt buộc và không lặp tác dụng khi gửi lại.",
        "Ghi chú có tiêu đề/nội dung/chủ sở hữu. Không quyết định bảng DB hay API.",
        "Chỉ chủ sở hữu đọc ghi chú cá nhân; kiểm tra lại phiên khi ghi. Quyền công ty còn mở.",
        "Chưa có evidence hệ thống As-Is. To-Be cho phép lưu rồi đọc lại ghi chú của mình.",
        "Main flow tạo/đọc lại, alternative hủy và exception phiên hết hiệu lực. Các feature còn lại cần refinement trước triển khai.",
        "Inventory có timeout/retry không lặp tác dụng; spec cần thêm whitespace, phiên hết hiệu lực và rapid click. Không tự chọn ngưỡng độ dài.",
        "Chưa có capacity/SLA được cung cấp, để Proposed.",
        "Mỗi CAP có một REQ; các requirement công ty/mẫu/tìm kiếm được giữ, không bỏ vì chưa chốt policy.",
        "Ai cấp quyền công ty, quản lý mẫu và xác định phạm vi search? Những câu này chặn PBI tương ứng, không chặn lát cắt cá nhân đã xác định."]))
    return write_document(p, "requirements", d, [discovery.path, ROOT / "scenario.txt"], sections=s)


def make_flow(identifier, kind, title, trigger, outcome, rules):
    return {"flow_id": identifier, "kind": kind, "title": title, "trigger": trigger,
            "branch_point": "Bắt đầu" if kind == "main" else "MF-001 tại bước gửi",
            "steps": [{"step": 1, "actor_action": trigger, "system_action": outcome, "input": "Tiêu đề và nội dung đang soạn", "result": outcome}],
            "termination": "Kết thúc tại phản hồi được mô tả", "expected_outcome": outcome,
            "data_state": outcome, "feedback": outcome, "recovery": "Giữ nội dung nếu kết quả chưa rõ; kiểm tra thao tác cũ trước khi gửi lại",
            "requirement_refs": ["REQ-001"], "related_br_refs": rules, "confirmation_status": "Confirmed"}


def backlog(p):
    discovery, reqdoc = source(p, "brainstorm"), source(p, "requirements")
    pbis = []
    for index, req in enumerate(reqdoc.data["requirements"], 1):
        pbis.append({"pbi_id": f"PBI-{index:03d}", "epic_id": "EPIC-001", "feature_id": f"FEAT-{index:03d}",
            "title": req["title"], "user_story": f"Là người dùng, tôi muốn {req['title'].lower()} để lưu và tái sử dụng thông tin.",
            "business_value": req["expected_outcome"], "scope": [req["expected_outcome"]],
            "out_of_scope": [r["title"] for r in reqdoc.data["requirements"] if r is not req], "requirement_refs": [req["requirement_id"]],
            "dependencies": [] if index == 1 else ["PBI-001"], "priority_proposal": "Lát cắt cá nhân trước; mở rộng sau khi chốt policy",
            "estimation_status": "Unestimated", "confirmation_status": "Proposed", "open_questions": [] if index == 1 else ["Cần refinement chính sách trước triển khai"],
            "invest": {"independent": "Lát cắt cá nhân chạy độc lập; các mở rộng phụ thuộc tạo tài liệu.", "negotiable": "UI chưa chốt; outcome đã mô tả.",
                       "valuable": req["expected_outcome"], "estimable": "Cần team refinement, chưa gán story point.",
                       "small": "Một kết quả người dùng, tách theo không gian/cách tạo/tìm lại.", "testable": "Quan sát tài liệu/kết quả và phạm vi được phép."}})
    d = {"epics": [{"epic_id": "EPIC-001", "title": "Lưu và tái sử dụng tri thức", "business_value": discovery.data["capabilities"][0]["business_value"]}],
         "features": [{"feature_id": f"FEAT-{i:03d}", "epic_id": "EPIC-001", "title": r["title"], "requirement_refs": [r["requirement_id"]]}
                      for i, r in enumerate(reqdoc.data["requirements"], 1)], "pbis": pbis, "unassigned_requirements": [], "change_history": []}
    s = dict(zip(HEADINGS["product-backlog"], [
        "Một Epic, bốn Feature/PBI theo kết quả người dùng. Scope/ưu tiên chưa phải cam kết triển khai.",
        "Epic lưu và tái sử dụng tri thức bao gồm cả cá nhân và tổ chức.",
        "Tách bốn Feature theo nhu cầu; không chia frontend/backend.",
        "PBI-001 tạo/đọc lại cá nhân là lát cắt nhỏ đầu tiên; các PBI còn lại cần refinement policy.",
        "Mỗi PBI có phân tích INVEST; chưa estimate, không gán story points.",
        "Bốn REQ được bao phủ; không unassigned requirement. Một REQ vẫn có thể được nhiều PBI nếu sau này split.",
        "Các mở rộng dựa trên khả năng tạo tài liệu; không có vòng lặp.",
        "Công ty/mẫu/search cần chốt policy trước triển khai. Backlog sẽ qua checkpoint test riêng."]))
    return write_document(p, "product-backlog", d, [discovery.path, reqdoc.path], sections=s)


def round_plan(p):
    b, r = source(p, "product-backlog"), source(p, "requirements")
    record_checkpoint(p, "backlog", "Approved", [b.path])
    d = {"rounds": [{"round_id": "R1", "goal": "Kiểm chứng tạo và đọc lại ghi chú cá nhân", "status": "Proposed",
            "pbi_refs": [b.data["pbis"][0]["pbi_id"]], "dependencies": [], "risks": ["Chưa có capacity; UI còn Proposed"],
            "capacity_assumptions": [], "capacity_gaps": ["Chưa có ước lượng hoặc năng lực nhóm"],
            "allocation_rationale": "Chọn lát cắt có quy tắc rõ; các PBI mở rộng chưa ready", "approval_status": "Pending"}],
         "unassigned_pbis": [item["pbi_id"] for item in b.data["pbis"][1:]], "change_history": []}
    s = dict(zip(HEADINGS["round-plan"], ["R1 kiểm chứng hành trình cá nhân, không mặc định Sprint.",
        "Chỉ PBI-001 ở R1; ba PBI còn lại unassigned vì policy còn mở.", "PBI-001 không có dependency; mở rộng chưa được phân bổ.",
        "Thiếu capacity và estimate: allocation Proposed, không cam kết số ngày.", "Chưa gắn Approved; test checkpoint cho phép Proposed có evidence riêng.",
        "Kế hoạch đầu tiên, chưa chuyển PBI giữa Round."]))
    return write_document(p, "round-plan", d, [b.path, r.path], sections=s)


def record_checkpoint(p, name, decision, paths):
    path = p.planning / "approvals.json"
    document = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"schema_version": "1.0", "project_id": p.config["project_id"], "approvals": []}
    record = {"checkpoint": name, "decision": decision, "actor": "TEST HUMAN DOUBLE", "evidence": "scenario.txt — synthetic scripted decision, not a real user approval",
        "decided_at": "2026-11-17T00:00:00+07:00", "pbi_refs": ["PBI-001"],
        "documents": [{"path": p.relative(file), "sha256": sha(file)} for file in paths], "resolved_decisions": ["Personal-note behavior specified in scenario.txt"]}
    document["approvals"] = [a for a in document["approvals"] if a["checkpoint"] != name] + [record]
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2), encoding="utf-8")


def identity(p):
    backlog_doc = source(p, "product-backlog")
    pbi = next(item for item in backlog_doc.data["pbis"] if item["pbi_id"] == "PBI-001")
    rnd = next(r for r in source(p, "round-plan").data["rounds"] if pbi["pbi_id"] in r["pbi_refs"])
    return pbi, {k: pbi[k] for k in ("pbi_id", "epic_id", "feature_id", "title", "requirement_refs")} | {"round_id": rnd["round_id"]}


def business(p):
    rnd = source(p, "round-plan")
    record_checkpoint(p, "round-plan", "Proposed Allowed", [rnd.path])
    pbi, fields = identity(p)
    reqdoc = source(p, "requirements")
    rule_ids = [r["br_id"] for r in reqdoc.data["business_rules"] if "REQ-001" in r["requirement_refs"]]
    d = {**fields, "business_story": fact(pbi["user_story"], "Confirmed"),
        "problems": [fact("Thông tin cá nhân cần lưu lại thay vì nằm rải rác trong các đoạn chat.")], "target_users": ["Người dùng đã đăng nhập"],
        "goals": [fact(pbi["scope"][0], "Confirmed")], "business_value": fact(pbi["business_value"], "Confirmed"), "as_is": [],
        "to_be": [fact("Chủ sở hữu tạo ghi chú riêng và mở lại để đọc.", "Confirmed")],
        "solution": [{"entry_point": "Không gian cá nhân, hành động tạo mới (UI Proposed)", "ui_components": ["Trường tiêu đề", "Trường nội dung", "Lưu", "Hủy"],
            "actions": ["Mở form", "Nhập tiêu đề và nội dung", "Gửi tạo hoặc hủy", "Đọc lại ghi chú đã lưu"],
            "data_state": "Chỉ tạo khi dữ liệu hợp lệ và phiên có quyền; cùng thao tác không tạo bản sao",
            "feedback": "Thành công mở ghi chú; lỗi trả nguyên nhân; chưa rõ kết quả giữ nội dung và kiểm tra thao tác cũ",
            "permission": reqdoc.data["business_rules"][0]["rule"], "business_rule_refs": rule_ids,
            "confirmation_status": "Proposed", "source_refs": ["requirements.md#REQ-001", "scenario.txt"]}],
        "scope": pbi["scope"], "out_of_scope": pbi["out_of_scope"], "business_rule_refs": rule_ids, "dependencies": pbi["dependencies"],
        "risks": ["Chưa có capacity hoặc chính sách giới hạn độ dài; chưa dùng làm cam kết production"],
        "open_questions": ["Nhãn hành động và bố cục UI cần refinement"], "blockers": [], "change_history": []}
    s = dict(zip(HEADINGS["business"], [
        "PBI-001 thuộc FEAT-001/EPIC-001, R1 Proposed; phạm vi là tạo và đọc lại ghi chú cá nhân.",
        "Người dùng ghi lại thông tin cho bản thân và mở lại sau; không chia sẻ sang không gian công ty trong PBI này.",
        "Phân tán thông tin là giả thuyết, chưa có research xác nhận. Không gán KPI tiết kiệm thời gian.",
        "Người dùng đã đăng nhập là chủ sở hữu của ghi chú mới.", "Lưu rồi đọc lại đúng nội dung trong phạm vi cá nhân.",
        "Giá trị là bảo toàn thông tin cá nhân để tái sử dụng.", "As-Is chưa xác minh. To-Be tạo ghi chú riêng rồi đọc lại.",
        "Đề xuất vào không gian cá nhân và chọn tạo mới, nhập tiêu đề/nội dung, Lưu hoặc Hủy. Khi Lưu, kiểm dữ liệu và phiên hiện tại; thành công mở ghi chú. Lỗi không tạo bản ghi; kết quả chưa rõ giữ nội dung và kiểm tra thao tác cũ trước khi gửi lại. Tên nhãn và bố cục là Proposed.",
        "Chỉ tạo/đọc lại cá nhân; công ty, mẫu và search nằm ngoài PBI này.",
        "BR-001 kiểm quyền sở hữu/phiên; BR-002 yêu cầu dữ liệu có ký tự không trắng; BR-003 không lặp tác dụng khi retry.",
        "Không có dependency PBI. Phiên đăng nhập là precondition của fixture, không tự tạo feature authentication.",
        "Thiếu capacity/giới hạn độ dài cần refinement trước triển khai production; bản này chỉ draft.",
        "Nhãn UI chưa chốt, không ảnh hưởng outcome đã được scenario xác định.",
        "Nguồn: brainstorm, requirements, backlog, Round và scenario fixture. SHA-256 ở metadata."]))
    return write_document(p, "business", d, [source(p, kind).path for kind in ("brainstorm", "requirements", "product-backlog", "round-plan")] + [ROOT / "scenario.txt"],
                          p.planning / "drafts/PBI-001/business.md", s)


def spec(p):
    bus = Validator(p).require_valid(p.planning / "drafts/PBI-001/business.md", "business", "PBI-001")
    reqdoc = source(p, "requirements")
    pbi, fields = identity(p)
    rules = [r for r in reqdoc.data["business_rules"] if "REQ-001" in r["requirement_refs"]]
    flows = [make_flow("MF-001", "main", "Tạo và đọc lại", "Gửi tiêu đề và nội dung hợp lệ", "Một ghi chú thuộc chủ sở hữu được lưu và đọc lại đúng nội dung", [r["br_id"] for r in rules]),
        make_flow("AF-001", "alternative", "Hủy tạo", "Chọn hủy trước khi gửi", "Không tạo ghi chú", []),
        make_flow("EF-001", "exception", "Dữ liệu trống", "Gửi tiêu đề hoặc nội dung rỗng/whitespace", "Không lưu; chỉ rõ trường thiếu để sửa", ["BR-002"]),
        make_flow("EF-002", "exception", "Phiên không hợp lệ", "Phiên hết hiệu lực trước khi gửi", "Không lưu và không lộ nội dung", ["BR-001"]),
        make_flow("EF-003", "exception", "Kết quả chưa rõ", "Mất phản hồi sau thao tác gửi", "Giữ nội dung; kiểm tra thao tác cũ trước khi gửi lại, không tạo bản sao", ["BR-003"]),
        make_flow("EF-004", "exception", "Người khác đọc", "Tài khoản khác mở ghi chú cá nhân", "Không hiển thị nội dung của chủ sở hữu khác", ["BR-001"])]
    flows[0]["steps"] = [
        {"step": 1, "actor_action": "Mở tạo ghi chú cá nhân", "system_action": "Hiện chỗ nhập tiêu đề và nội dung", "input": "Phiên người dùng", "result": "Form sẵn sàng"},
        {"step": 2, "actor_action": "Nhập và gửi tạo", "system_action": "Kiểm dữ liệu, quyền hiện tại và thao tác đã xử lý", "input": "Tiêu đề/nội dung", "result": "Đủ điều kiện hoặc nhánh exception"},
        {"step": 3, "actor_action": "Chờ kết quả", "system_action": "Lưu một ghi chú với chủ sở hữu hiện tại", "input": "Dữ liệu hợp lệ", "result": "Một ghi chú được tạo"},
        {"step": 4, "actor_action": "Đọc lại ghi chú", "system_action": "Hiển thị đúng nội dung cho chủ sở hữu", "input": "Ghi chú đã lưu", "result": "Người dùng đọc lại được"}]
    for flow in flows[1:]:
        flow["branch_point"] = "MF-001 bước 1 trước khi gửi" if flow["kind"] == "alternative" else "MF-001 bước 4" if flow["flow_id"] == "EF-004" else "MF-001 bước 2"
    cases = [
        ("Trống hoặc whitespace", "Tiêu đề/nội dung không có ký tự hữu ích", "Không lưu, nêu trường thiếu", "BR-002", "AC-003"),
        ("Phiên thay đổi", "Phiên hết hiệu lực sau khi form mở", "Không lưu và không lộ nội dung", "BR-001", "AC-004"),
        ("Timeout sau thành công", "Server lưu nhưng phản hồi bị mất", "Kiểm tra thao tác cũ; hiển thị kết quả đã lưu và không tạo bản sao", "BR-003", "AC-005"),
        ("Rapid click", "Cùng thao tác được gửi nhiều lần liên tiếp", "Chỉ một ghi chú cho cùng thao tác", "BR-003", "AC-007")]
    ecs = [{"ec_id": f"EC-{i:03d}", "title": title, "scenario": scenario, "preconditions": ["Form tạo cá nhân đã mở"],
            "expected_behavior": outcome, "requirement_refs": fields["requirement_refs"], "related_br_refs": [rule], "related_ac_refs": [ac], "confirmation_status": "Confirmed"}
           for i, (title, scenario, outcome, rule, ac) in enumerate(cases, 1)]
    acs = [{"ac_id": f"AC-{i:03d}", "title": f["title"], "given": "Người dùng đã mở form tạo cá nhân với dữ liệu đang nhập",
            "when": f["trigger"], "then": f["expected_outcome"], "requirement_refs": fields["requirement_refs"], "flow_refs": [f["flow_id"]],
            "edge_case_refs": [ec["ec_id"] for ec in ecs if f"AC-{i:03d}" in ec["related_ac_refs"]], "confirmation_status": "Confirmed"}
           for i, f in enumerate(flows, 1)]
    acs[5]["given"] = "Một ghi chú cá nhân đã được tài khoản A tạo; tài khoản B không phải chủ sở hữu"
    acs.append({"ac_id": "AC-007", "title": "Gửi lặp cùng thao tác", "given": "Một thao tác tạo với dữ liệu hợp lệ",
                "when": "Gửi lặp cùng thao tác khi chưa nhận phản hồi", "then": "Chỉ một ghi chú được tạo cho thao tác đó",
                "requirement_refs": fields["requirement_refs"], "flow_refs": ["MF-001", "EF-003"], "edge_case_refs": ["EC-004"], "confirmation_status": "Confirmed"})
    d = {**fields, "user_stories": [{"as_a": "Người dùng đã đăng nhập", "i_want": "Tạo và đọc lại ghi chú cá nhân", "so_that": "Lưu thông tin riêng để tái sử dụng"}],
        "preconditions": ["Người dùng đã đăng nhập"], "postconditions": ["Thành công: một ghi chú thuộc chủ sở hữu, đọc lại đúng nội dung", "Hủy/lỗi dữ liệu hoặc phiên: không tạo ghi chú"],
        "flows": flows, "business_rules": rules, "permissions": reqdoc.data["permissions"],
        "data_states": [fact("Đang soạn → đã lưu khi thành công; lỗi dữ liệu/phiên không tạo ghi chú; chưa rõ kết quả giữ nội dung để đối soát.", "Confirmed")],
        "edge_cases": ecs, "acceptance_criteria": acs,
        "traceability": [{"requirement_id": fields["requirement_refs"][0], "br_refs": [r["br_id"] for r in rules], "flow_refs": [f["flow_id"] for f in flows],
                          "ec_refs": [e["ec_id"] for e in ecs], "ac_refs": [a["ac_id"] for a in acs]}],
        "scope": bus.data["scope"], "out_of_scope": bus.data["out_of_scope"], "open_questions": bus.data["open_questions"], "blockers": [], "change_history": []}
    s = dict(zip(HEADINGS["spec"], [
        "PBI-001 / REQ-001, R1 Proposed; chỉ tạo/đọc lại ghi chú cá nhân.", "Là người dùng đã đăng nhập, tôi muốn lưu ghi chú riêng để đọc lại.",
        "Đã đăng nhập trước khi mở form; phiên vẫn phải được kiểm lại khi ghi.", "Thành công có một ghi chú đúng chủ sở hữu; hủy/lỗi không tạo.",
        "Mở form → nhập/gửi → kiểm quyền/dữ liệu/thao tác trùng → lưu → đọc lại. Steps chi tiết nằm trong BA-DATA.",
        "Hủy trước khi gửi kết thúc mà không tạo ghi chú.", "Dữ liệu trống, phiên hết hiệu lực, mất phản hồi và người khác đọc đều có outcome riêng; không gom thành lỗi chung.",
        "Giữ nguyên BR-001..003 từ requirements, không chốt API/DB hoặc thuật toán chống trùng.",
        "Chỉ chủ sở hữu được đọc. Người khác không thấy nội dung.", "Đang soạn, đã lưu hoặc chưa rõ kết quả; không tự coi timeout là thất bại lưu.",
        "EC bao phủ whitespace, phiên thay đổi, timeout sau success và rapid click. Không xét parent deletion vì PBI này không tạo trong thư mục/công ty.",
        "Bảy AC Given/When/Then bao phủ success, cancel, invalid input, auth, timeout, ownership và duplicate submission.",
        "REQ-001 → ba BR, sáu Flow, bốn EC → bảy AC, tất cả thuộc cùng PBI.", "Công ty, mẫu và tìm kiếm nằm ngoài scope PBI cá nhân.",
        "Nhãn/bố cục UI còn Proposed; giới hạn độ dài và performance chưa chốt cho production. Đây là bản draft kiểm chứng hành vi."]))
    return write_document(p, "spec", d, [bus.path, reqdoc.path, source(p, "product-backlog").path], p.planning / "drafts/PBI-001/spec.md", s)


def review(p):
    bus = Validator(p).require_valid(p.planning / "drafts/PBI-001/business.md", "business", "PBI-001")
    sp = Validator(p).require_valid(p.planning / "drafts/PBI-001/spec.md", "spec", "PBI-001")
    _, fields = identity(p)
    ac = next(a for a in sp.data["acceptance_criteria"] if a["ac_id"] == "AC-005")
    ef = next(f for f in sp.data["flows"] if f["flow_id"] == "EF-004")
    findings = [
        {"finding_id": "FIND-001", "severity": "Major", "file": p.relative(sp.path), "section": "Acceptance Criteria / AC-005",
         "evidence": ac["then"], "impact": "AC chưa chứng minh hiển thị lại kết quả server đã lưu như EC-003 yêu cầu.",
         "recommendation": "Nêu Given thao tác đã lưu nhưng mất phản hồi, Then trả đúng ghi chú đã lưu và không tạo bản sao.",
         "status": "Resolved" if "đã lưu" in ac["given"] and "hiển thị" in ac["then"] else "Open"},
        {"finding_id": "FIND-002", "severity": "Major", "file": p.relative(sp.path), "section": "Exception Flows / EF-004",
         "evidence": ef["steps"][0]["input"] + " / " + ef["recovery"],
         "impact": "Nhánh đọc trái quyền dùng input/recovery của form tạo; chưa mô tả đúng trạng thái dữ liệu cần bảo vệ.",
         "recommendation": "Đổi input thành tham chiếu ghi chú và phiên tài khoản đọc; không trả nội dung, ghi chú nguồn không đổi, kết thúc nhánh.",
         "status": "Resolved" if ef["steps"][0]["input"] == "Tham chiếu ghi chú và phiên tài khoản đọc" else "Open"},
        {"finding_id": "FIND-003", "severity": "Minor", "file": p.relative(bus.path), "section": "Giải pháp phần mềm chi tiết",
         "evidence": bus.data["solution"][0]["entry_point"], "impact": "Nhãn hành động/bố cục UI chưa được refinement; không thay outcome đã xác định.",
         "recommendation": "Giữ Proposed trong draft; chốt nhãn khi thiết kế giao diện.", "status": "Open"}]
    failure = any(f["severity"] == "Major" and f["status"] == "Open" for f in findings)
    existing = p.planning / "reviews/PBI-001-review.md"
    history = parse(existing).data["change_history"] if existing.exists() else []
    if existing.exists() and not failure:
        history = history + [{"at": "2026-11-17T00:00:00+07:00", "change": "FIND-001 và FIND-002 được giải quyết sau refinement spec; giữ FIND-003 mở.",
                              "affected_ids": ["FIND-001", "FIND-002"], "reason": "Đã kiểm chứng lại AC-005 và EF-004 theo cùng rule nguồn."}]
    d = {**fields, "result": "FAIL" if failure else "CONDITIONAL", "readiness": "Blocked" if failure else "Needs Refinement",
         "blockers": [f["finding_id"] for f in findings if f["severity"] == "Major" and f["status"] == "Open"], "findings": findings,
         "coverage_notes": ["So business goal/scope với REQ-001, ba BR, sáu flows, bốn EC và bảy AC; không lẫn công ty/mẫu/search.",
                            "Kiểm whitespace, ownership, phiên thay đổi, cancel, timeout sau success và duplicate submission; không tự đặt SLA/length cap."],
         "change_history": history}
    s = dict(zip(HEADINGS["review"], [d["result"] + ": structural PASS không thay review ngữ nghĩa hoặc human approval.",
        "\n\n".join(f"{f['finding_id']} — {f['severity']} / {f['status']}: {f['evidence']} → {f['recommendation']}" for f in findings),
        "REQ-001 trace đầy đủ. Đã đọc nội dung business/spec, không chỉ kiểm Contract Summary.", d["readiness"],
        ", ".join(d["blockers"]) or "Không còn Major/Critical; còn Minor về UI, chỉ phù hợp draft publication nếu được cho phép.",
        "Review hash đúng business/spec hiện tại; không sửa hai nguồn trong bước review."]))
    return write_document(p, "review", d, [bus.path, sp.path, source(p, "requirements").path, source(p, "product-backlog").path], existing, s)


def refine_spec(p):
    import re
    path = p.planning / "drafts/PBI-001/spec.md"
    doc = Validator(p).require_valid(path, "spec", "PBI-001")
    d = doc.data
    ac = next(a for a in d["acceptance_criteria"] if a["ac_id"] == "AC-005")
    ac["given"] = "Server đã lưu một ghi chú cho thao tác của chủ sở hữu nhưng client mất phản hồi"
    ac["then"] = "Sau khi kiểm tra thao tác cũ, hiển thị đúng ghi chú đã lưu cho chủ sở hữu và không tạo bản sao"
    ef = next(f for f in d["flows"] if f["flow_id"] == "EF-004")
    ef["steps"][0]["input"] = "Tham chiếu ghi chú và phiên tài khoản đọc"
    ef["data_state"] = "Ghi chú của chủ sở hữu không thay đổi; không trả nội dung cho tài khoản khác"
    ef["recovery"] = "Kết thúc nhánh đọc bị từ chối; không cung cấp nội dung hoặc thử đọc lại dưới quyền khác"
    for flow in d["flows"]:
        if flow["flow_id"] == "EF-001":
            flow["recovery"] = "Sửa trường thiếu trước khi gửi lại"
        elif flow["flow_id"] == "EF-002":
            flow["recovery"] = "Xác lập phiên hợp lệ trước thao tác mới; không retry tự động"
        elif flow["flow_id"] == "AF-001":
            flow["recovery"] = "Kết thúc; người dùng có thể bắt đầu thao tác tạo mới"
        elif flow["flow_id"] == "MF-001":
            flow["recovery"] = "Không áp dụng khi đã thành công; mất phản hồi đi EF-003"
        elif flow["flow_id"] == "EF-003":
            flow["branch_point"] = "MF-001 bước 3 hoặc 4 sau khi gửi, chưa biết kết quả"
    d["change_history"].append({"at": "2026-11-17T00:00:00+07:00", "change": "Làm rõ AC-005 và EF-004; recovery riêng cho từng nhánh, giữ toàn bộ IDs và BR nguồn.",
                                "affected_ids": ["AC-005", "EF-004", "EF-003"], "reason": "Giải quyết FIND-001/FIND-002, không thay quyết định nghiệp vụ."})
    sections = {h: re.search(r"^## " + re.escape(h) + r"\n(.*?)(?=^## |\Z)", doc.prose, re.M | re.S).group(1).strip() for h in HEADINGS["spec"]}
    sections["Exception Flows"] += " Nhánh đọc trái quyền không trả dữ liệu và không đổi ghi chú nguồn; timeout kiểm tra kết quả đã lưu trước retry."
    sections["Acceptance Criteria"] += " AC-005 xác định server đã lưu và buộc hiển thị đúng kết quả sau đối soát."
    return write_document(p, "spec", d, [p.path(s["path"]) for s in doc.metadata["source_documents"]], path, sections)


def publish_example(p):
    rev = Validator(p).require_valid(p.planning / "reviews/PBI-001-review.md", "review", "PBI-001")
    # Scenario authorizes only draft, and only after resolving FAIL. Exercise missing-publish gate first.
    manifest = prepare(p, "PBI-001")
    before = {"blocked": manifest["blocked"], "target_exists": p.path(manifest["target"]).exists()}
    paths = [source(p, "product-backlog").path, source(p, "round-plan").path,
             p.planning / "drafts/PBI-001/business.md", p.planning / "drafts/PBI-001/spec.md", rev.path]
    record_checkpoint(p, "publish", "Draft Publication", paths)
    approved = prepare(p, "PBI-001")
    result = publish(p, approved)
    rerun = publish(p, prepare(p, "PBI-001"))
    evidence = {"execution": "Primary agent manual in-session execution, serialized by agent_example.py; synthetic approvals only",
                "before_publish_checkpoint": before, "manifest": approved, "publish": result, "rerun": rerun}
    if not (ROOT / "publish-evidence.json").exists():
        (ROOT / "publish-evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    artifacts = [source(p, kind).path for kind in ("brainstorm", "requirements", "product-backlog", "round-plan")] + paths[2:]
    approvals = json.loads((p.planning / "approvals.json").read_text(encoding="utf-8"))["approvals"]
    state = {"mode": "SINGLE-PBI", "current_phase": "selected-pbi-published", "completed": ["ba-" + parse(file).metadata["document_type"] for file in artifacts] + ["ba-publish"],
        "pending": ["Refine unassigned PBI-002/PBI-003/PBI-004 when requested"], "blockers": [],
        "artifacts": [{"path": p.relative(file), "sha256": sha(file)} for file in artifacts], "approvals": approvals,
        "last_updated": "2026-11-17T00:00:00+07:00", "selected_pbis": ["PBI-001"], "selected_round": "R1", "change_history": []}
    sections = dict(zip(HEADINGS["workflow-state"], ["Selected PBI-001 draft published; không tuyên bố hoàn tất các PBI khác.",
        "Tám bước được thực hiện bằng file thật trong phiên; review FAIL rồi refinement và CONDITIONAL.", state["pending"][0],
        "Không còn blocker cho draft PBI-001; Minor UI còn trong review.", "Snapshot hashes trong BA-DATA, đọc lại khi RESUME.",
        "Tất cả approvals ở đây là TEST HUMAN DOUBLE từ scenario.txt, không phải quyết định thật.",
        "RESUME phải validate source chain; nguồn đổi làm review/approval cũ stale."]))
    return write_document(p, "workflow-state", state, [], sections=sections)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["brainstorm", "requirements", "backlog", "round_plan", "business", "spec", "review", "refine_spec", "publish_example"])
    args = parser.parse_args()
    path = brainstorm() if args.stage == "brainstorm" else globals()[args.stage](Project.load(ROOT / "ba-project.yaml"))
    document = parse(path)
    print(json.dumps({"stage": args.stage, "path": str(path), "sha256": sha(path), "data": document.data}, ensure_ascii=False, indent=2))
