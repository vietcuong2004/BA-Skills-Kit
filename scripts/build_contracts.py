"""Maintain the kit's JSON Schemas. Run only in the kit, never a target app."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = {"type": "string", "minLength": 1, "pattern": r"\S"}
STATUS = {"enum": ["Confirmed", "Proposed", "Open Question"]}
DOC_STATUS = {"enum": ["draft", "in_review", "approved"]}


def obj(properties, optional=()):
    return {"type": "object", "properties": properties,
            "required": [k for k in properties if k not in optional], "additionalProperties": False}


def arr(item=S, minimum=0):
    return {"type": "array", "items": item, "minItems": minimum, "uniqueItems": True}


def ident(prefix):
    return {"type": "string", "pattern": rf"^{prefix}-[0-9]{{3,}}$"}


def refs(prefix, minimum=0):
    return arr(ident(prefix), minimum)


PBI = {"type": "string", "pattern": r"^[A-Z][A-Z0-9]*-[0-9]{3,}$"}
ROUND = {"type": "string", "pattern": r"^[A-Za-z][A-Za-z0-9_-]*[1-9][0-9]*$"}
FACT = obj({"text": S, "confirmation_status": STATUS, "source_refs": arr(S, 1)})
SOURCE = obj({"path": S, "sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
              "kind": {"enum": ["ba", "raw"]}}, ("kind",))
HISTORY = arr(obj({"at": S, "change": S, "affected_ids": arr(S), "reason": S}))
BR = obj({"br_id": ident("BR"), "title": S, "rule": S, "requirement_refs": refs("REQ", 1),
          "source_refs": arr(S, 1), "confirmation_status": STATUS})
FLOW = obj({"flow_id": {"type": "string", "pattern": "^(MF|AF|EF)-[0-9]{3,}$"},
            "title": S, "kind": {"enum": ["main", "alternative", "exception"]},
            "trigger": S, "branch_point": S, "steps": arr(obj({"step": {"type": "integer", "minimum": 1},
            "actor_action": S, "system_action": S, "input": S, "result": S}), 1),
            "termination": S, "expected_outcome": S, "data_state": S, "feedback": S, "recovery": S,
            "requirement_refs": refs("REQ", 1), "related_br_refs": refs("BR"), "confirmation_status": STATUS})
EC = obj({"ec_id": ident("EC"), "title": S, "scenario": S, "preconditions": arr(S),
          "expected_behavior": S, "open_question": S, "requirement_refs": refs("REQ", 1),
          "related_br_refs": refs("BR"), "related_ac_refs": refs("AC"), "confirmation_status": STATUS},
         ("expected_behavior", "open_question"))
EC["anyOf"] = [{"required": ["expected_behavior"]}, {"required": ["open_question"],
                  "properties": {"confirmation_status": {"const": "Open Question"}}}]
AC = obj({"ac_id": ident("AC"), "title": S, "given": S, "when": S, "then": S,
          "requirement_refs": refs("REQ", 1), "flow_refs": arr(S, 1), "edge_case_refs": refs("EC"),
          "confirmation_status": STATUS})
BUSINESS_HANDOVER = obj({"purpose": FACT, "customer_needs": arr(FACT, 1), "affected_areas": arr(FACT),
    "solution_sections": arr(obj({"title": S, "paragraphs": arr(FACT),
        "table": obj({"columns": arr(S, 2),
                      "rows": {"type": "array", "minItems": 1, "items": {"type": "array", "minItems": 2, "items": S}}}),
        "confirmation_status": STATUS, "source_refs": arr(S, 1)}, ("table",)), 1),
    "notes": arr(FACT), "quality_constraints": arr(FACT)}, ("quality_constraints",))
SPEC_HANDOVER = obj({
    "feature_branch": S, "created": {"type": "string", "pattern": r"^\d{4}-\d{2}-\d{2}$"},
    "platform": S, "figma_url": {"type": "string", "pattern": r"^https?://\S+$"},
    "stories": arr(obj({"title": S, "priority": {"enum": ["P1", "P2", "P3"]},
        "priority_reason": S, "independent_test": arr(S, 2), "ac_refs": refs("AC", 1)},
        ("priority", "priority_reason")), 1),
    "functional_requirements": arr(obj({"fr_id": ident("FR"), **FACT["properties"],
        "requirement_refs": refs("REQ", 1), "ac_refs": refs("AC", 1)}), 1),
    "nonfunctional_requirements": arr(obj({"nfr_id": ident("NFR"), **FACT["properties"]})),
    "success_criteria": arr(FACT, 1), "assumptions": arr(FACT), "dependencies": arr(FACT),
}, ("feature_branch", "created", "platform", "figma_url"))


def write(name, schema):
    schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": name, **schema}
    path = ROOT / "contracts" / f"{name}.schema.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    write("project-config", obj({"config_version": {"const": "1.0"}, "project_id": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
        "project_name": S, "repository_root": {**S, "default": ".", "description": "For .temp/ba-project.yaml, relative to the project above .temp; for legacy configs, relative to the config directory. Parent traversal is forbidden."},
        "output_root": {**S, "default": ".specify", "description": "Published Round/PBI pairs only; must be disjoint from .temp."},
        "planning_dir": {**S, "default": ".temp", "description": "Must resolve to project/.temp or a directory below it. Never inside output_root."},
        "round_prefix": {"type": "string", "pattern": "^[A-Za-z][A-Za-z0-9_-]*$"},
        "pbi_prefix": {"type": "string", "pattern": "^[A-Z][A-Z0-9]*$"}, "language": S,
        "skill_runtime": {"const": "codex"}, "approval_policy": {"const": "human_checkpoints"}}))
    types = ["brainstorm", "requirements", "product-backlog", "round-plan", "business", "spec", "review", "workflow-state"]
    meta = obj({"schema_version": {"const": "1.0"}, "document_type": {"enum": types}, "project_id": S,
        "status": DOC_STATUS, "source_documents": arr(SOURCE), "generated_by": {"enum": ["ba-" + t for t in types[:-1]] + ["ba-workflow"]},
        "pbi_id": PBI, "epic_id": ident("EPIC"), "feature_id": ident("FEAT"), "round_id": ROUND,
        "requirement_refs": refs("REQ", 1)}, ("pbi_id", "epic_id", "feature_id", "round_id", "requirement_refs"))
    meta["allOf"] = [{"if": {"properties": {"document_type": {"enum": ["business", "spec", "review"]}}},
                     "then": {"required": ["pbi_id", "epic_id", "feature_id", "requirement_refs"]}}]
    write("metadata", meta)
    write("brainstorm", obj({"product_overview": FACT, "vision": FACT, "target_users": arr(S, 1),
        "problems": arr(FACT, 1), "jobs_to_be_done": arr(FACT, 1),
        "capabilities": arr(obj({"capability_id": ident("CAP"), "name": S, "description": S,
        "target_users": arr(S, 1), "business_value": S, "source_refs": arr(S, 1), "confirmation_status": STATUS}), 1),
        "goals": arr(FACT, 1), "scope": arr(FACT, 1), "exclusions": arr(FACT), "constraints": arr(FACT),
        "assumptions": arr(FACT), "open_questions": arr(S), "metrics": arr(FACT), "change_history": HISTORY}))
    write("requirements", obj({"actors": arr(obj({"actor_id": ident("ACT"), "name": S, "role": S}), 1),
        "requirements": arr(obj({"requirement_id": ident("REQ"), "title": S, "description": S, "actor": ident("ACT"),
        "trigger": S, "preconditions": arr(S), "expected_outcome": S, "capability_refs": refs("CAP", 1),
        "source_refs": arr(S, 1), "confirmation_status": STATUS, "business_rule_refs": refs("BR")}), 1),
        "business_rules": arr(BR), "data": arr(FACT), "permissions": arr(FACT), "as_is": arr(FACT),
        "flows": arr(FLOW, 1), "edge_cases": arr(EC), "nonfunctional": arr(FACT), "open_questions": arr(S), "change_history": HISTORY}))
    write("product-backlog", obj({"epics": arr(obj({"epic_id": ident("EPIC"), "title": S, "business_value": S}), 1),
        "features": arr(obj({"feature_id": ident("FEAT"), "epic_id": ident("EPIC"), "title": S, "requirement_refs": refs("REQ", 1)}), 1),
        "pbis": arr(obj({"pbi_id": PBI, "epic_id": ident("EPIC"), "feature_id": ident("FEAT"), "title": S,
        "user_story": S, "business_value": S, "scope": arr(S, 1), "out_of_scope": arr(S), "requirement_refs": refs("REQ", 1),
        "dependencies": arr(PBI), "priority_proposal": S, "estimation_status": {"const": "Unestimated"},
        "confirmation_status": STATUS, "open_questions": arr(S),
        "invest": obj({k: S for k in ["independent", "negotiable", "valuable", "estimable", "small", "testable"]})}), 1),
        "unassigned_requirements": arr(obj({"requirement_id": ident("REQ"), "reason": S})), "change_history": HISTORY}))
    write("round-plan", obj({"rounds": arr(obj({"round_id": ROUND, "goal": S, "status": STATUS,
        "pbi_refs": arr(PBI), "dependencies": arr(ROUND), "risks": arr(S), "capacity_assumptions": arr(FACT),
        "capacity_gaps": arr(S), "allocation_rationale": S, "approval_status": {"enum": ["Pending", "Approved", "Proposed Allowed"]}}), 1),
        "unassigned_pbis": arr(PBI), "change_history": HISTORY}))
    identity = {"pbi_id": PBI, "epic_id": ident("EPIC"), "feature_id": ident("FEAT"), "round_id": ROUND,
                "requirement_refs": refs("REQ", 1), "title": S}
    write("business", obj({**identity, "business_story": FACT, "problems": arr(FACT, 1), "target_users": arr(S, 1),
        "goals": arr(FACT, 1), "business_value": FACT, "as_is": arr(FACT), "to_be": arr(FACT, 1),
        "solution": arr(obj({"entry_point": S, "ui_components": arr(S), "actions": arr(S, 1), "data_state": S,
        "feedback": S, "permission": S, "business_rule_refs": refs("BR"), "confirmation_status": STATUS, "source_refs": arr(S, 1)}), 1),
        "scope": arr(S, 1), "out_of_scope": arr(S), "business_rule_refs": refs("BR"), "dependencies": arr(PBI),
        "risks": arr(S), "open_questions": arr(S), "blockers": arr(S), "change_history": HISTORY,
        "handover": BUSINESS_HANDOVER}, ("round_id", "handover")))
    write("spec", obj({**identity, "user_stories": arr(obj({"as_a": S, "i_want": S, "so_that": S}), 1),
        "preconditions": arr(S), "postconditions": arr(S, 1), "flows": arr(FLOW, 1), "business_rules": arr(BR),
        "permissions": arr(FACT), "data_states": arr(FACT), "edge_cases": arr(EC), "acceptance_criteria": arr(AC, 1),
        "traceability": arr(obj({"requirement_id": ident("REQ"), "br_refs": refs("BR"), "flow_refs": arr(S, 1),
        "ec_refs": refs("EC"), "ac_refs": refs("AC", 1)}), 1), "scope": arr(S, 1), "out_of_scope": arr(S),
        "open_questions": arr(S), "blockers": arr(S), "change_history": HISTORY,
        "handover": SPEC_HANDOVER}, ("round_id", "handover")))
    write("review", obj({**identity, "result": {"enum": ["PASS", "CONDITIONAL", "FAIL"]},
        "readiness": {"enum": ["Ready", "Needs Refinement", "Blocked"]}, "blockers": arr(S),
        "findings": arr(obj({"finding_id": ident("FIND"), "severity": {"enum": ["Critical", "Major", "Minor"]},
        "file": S, "section": S, "evidence": S, "impact": S, "recommendation": S,
        "status": {"enum": ["Open", "Resolved"]}})), "coverage_notes": arr(S, 1), "change_history": HISTORY}, ("round_id",)))
    approval = obj({"checkpoint": {"enum": ["backlog", "round-plan", "publish"]}, "decision": {"enum": ["Approved", "Proposed Allowed", "Draft Publication"]},
        "actor": S, "evidence": S, "decided_at": S, "pbi_refs": arr(PBI), "documents": arr(SOURCE, 1), "resolved_decisions": arr(S)})
    write("approvals", obj({"schema_version": {"const": "1.0"}, "project_id": S, "approvals": arr(approval)}))
    write("workflow-state", obj({"mode": {"enum": ["INTERACTIVE", "DRAFT", "RESUME", "SINGLE-PBI", "SINGLE-ROUND"]},
        "current_phase": S, "completed": arr(S), "pending": arr(S), "blockers": arr(S), "artifacts": arr(SOURCE),
        "approvals": arr(approval), "last_updated": S, "selected_pbis": arr(PBI), "selected_round": S,
        "change_history": HISTORY}, ("selected_round",)))


if __name__ == "__main__":
    main()
