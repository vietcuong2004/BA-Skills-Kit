import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from fixture_pipeline import build, approve_fixture
from ba_core import BAError, HEADINGS, Project, Validator, parse, render, sha
from publish_ba import prepare, publish
from workflow_state import resume


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_temp = tempfile.TemporaryDirectory()
        cls.base = build(Path(cls.base_temp.name) / "base")

    @classmethod
    def tearDownClass(cls):
        cls.base_temp.cleanup()

    def setUp(self):
        import shutil
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name) / "project"
        shutil.copytree(self.base.root, root)
        self.project = Project.load(root / "ba-project.yaml")
        self.plan = self.project.planning

    def path(self, kind):
        if kind in ("business", "spec"):
            return self.plan / "drafts" / "PBI-001" / f"{kind}.md"
        if kind == "review":
            return self.plan / "reviews" / "PBI-001-review.md"
        return self.plan / f"{kind}.md"

    def mutate(self, kind, change):
        path = self.path(kind)
        doc = parse(path)
        change(doc)
        # Rebuild the machine projection, as an editor would. Hashes in downstream remain stale.
        sections = {h: "Nội dung fixture đã sửa có kiểm soát." for h in HEADINGS[kind]}
        path.write_text(render(doc.metadata, doc.data, sections), encoding="utf-8")
        return path

    def codes(self, kind, pbi_id=None):
        validator = Validator(self.project)
        validator.validate(self.path(kind), pbi_id=pbi_id)
        return {d["code"] for d in validator.diagnostics if d["severity"] == "ERROR"}

    def assert_block(self, code):
        with self.assertRaises(BAError) as cm:
            prepare(self.project, "PBI-001")
        self.assertEqual(cm.exception.diagnostic["code"], code)

    def test_real_file_pipeline_and_publish(self):
        for kind in HEADINGS:
            self.assertEqual(self.codes(kind), set(), kind)
        manifest = prepare(self.project, "PBI-001")
        self.assertEqual(manifest["blocked"], [])
        result = publish(self.project, manifest)
        self.assertEqual(len(result["created"]), 2)
        target = self.project.path(manifest["target"])
        self.assertEqual({p.name for p in target.iterdir()}, {"business.md", "spec.md"})
        for name in ("business", "spec"):
            self.assertEqual(sha(target / f"{name}.md"), sha(self.path(name)))

    def test_idempotent(self):
        publish(self.project, prepare(self.project, "PBI-001"))
        manifest = prepare(self.project, "PBI-001")
        before = {e["destination"]: self.project.path(e["destination"]).stat().st_mtime_ns for e in manifest["entries"]}
        result = publish(self.project, manifest)
        self.assertEqual(len(result["skipped"]), 2)
        self.assertEqual(before, {p: self.project.path(p).stat().st_mtime_ns for p in before})

    def test_missing_field(self):
        self.mutate("spec", lambda d: d.data.pop("user_stories"))
        self.assertIn("SCHEMA_INVALID", self.codes("spec"))

    def test_wrong_type_and_version(self):
        for field, value in [("document_type", "unknown"), ("schema_version", "2.0")]:
            with self.subTest(field=field):
                self.mutate("business", lambda d: d.metadata.update({field: value}))
                self.assertIn("SCHEMA_INVALID", self.codes("business"))

    def test_wrong_known_type(self):
        validator = Validator(self.project)
        validator.validate(self.path("requirements"), expected_type="brainstorm")
        self.assertIn("WRONG_DOCUMENT_TYPE", {d["code"] for d in validator.diagnostics})

    def test_missing_file(self):
        self.path("business").unlink()
        self.assertIn("MISSING_INPUT", self.codes("spec"))

    def test_duplicate_ids(self):
        def change(doc):
            duplicate = copy.deepcopy(doc.data["pbis"][0])
            duplicate["title"] = "Different title, same ID"
            doc.data["pbis"].append(duplicate)
        self.mutate("product-backlog", change)
        self.assertIn("DUPLICATE_ID", self.codes("product-backlog"))

    def test_broken_reference(self):
        self.mutate("requirements", lambda d: d.data["requirements"][0].update(capability_refs=["CAP-999"]))
        self.assertIn("BROKEN_REF", self.codes("requirements"))

    def test_wrong_pbi(self):
        self.assertIn("PBI_MISMATCH", self.codes("business", "PBI-002"))

    def test_wrong_business_pbi_in_spec_sources(self):
        self.mutate("business", lambda d: (d.metadata.update(pbi_id="PBI-002"), d.data.update(pbi_id="PBI-002")))
        self.assertIn("PBI_MISMATCH", self.codes("spec"))

    def test_missing_gwt(self):
        self.mutate("spec", lambda d: d.data["acceptance_criteria"][0].pop("given"))
        self.assertIn("SCHEMA_INVALID", self.codes("spec"))

    def test_missing_edge_outcome(self):
        self.mutate("spec", lambda d: d.data["edge_cases"][0].pop("expected_behavior"))
        self.assertIn("SCHEMA_INVALID", self.codes("spec"))

    def test_open_edge_question_is_warning(self):
        def change(d):
            ec = d.data["edge_cases"][0]
            ec.pop("expected_behavior")
            ec.update(open_question="Cần chọn cách khôi phục", confirmation_status="Open Question")
        self.mutate("spec", change)
        validator = Validator(self.project)
        validator.validate(self.path("spec"))
        self.assertTrue(validator.ok, validator.diagnostics)
        self.assertIn("OPEN_EDGE_CASE", {d["code"] for d in validator.diagnostics})

    def test_stale_transitive(self):
        self.mutate("requirements", lambda d: d.data["requirements"][0].update(title="Thay đổi yêu cầu"))
        self.assertIn("STALE_INPUT", self.codes("review"))

    def test_resume_invalidates_downstream(self):
        self.assertFalse(resume(self.project)["invalidated"])
        self.mutate("requirements", lambda d: d.data["requirements"][0].update(title="Yêu cầu mới"))
        result = resume(self.project)
        invalid = {Path(a["path"]).name for a in result["invalidated"]}
        self.assertTrue({"requirements.md", "product-backlog.md", "round-plan.md", "business.md", "spec.md", "PBI-001-review.md"}.issubset(invalid))
        self.assertIn(self.project.relative(self.path("brainstorm")), result["current"])

    def test_state_human_approval_actor_not_business_actor_ref(self):
        approvals = json.loads((self.plan / "approvals.json").read_text(encoding="utf-8"))["approvals"]
        self.mutate("workflow-state", lambda d: d.data.update(approvals=approvals))
        self.assertEqual(self.codes("workflow-state"), set())
        self.assertFalse(resume(self.project)["invalidated"])

    def test_review_fail_blocks(self):
        self.mutate("review", lambda d: d.data.update(result="FAIL", readiness="Blocked", blockers=["Quyền chưa chốt"]))
        self.assert_block("PUBLISH_BLOCKED")

    def test_missing_approval(self):
        (self.plan / "approvals.json").unlink()
        manifest = prepare(self.project, "PBI-001")
        self.assertEqual(manifest["blocked"][0]["code"], "MISSING_APPROVAL")
        with self.assertRaises(BAError):
            publish(self.project, manifest)
        self.assertFalse(self.project.path(manifest["target"]).exists())

    def test_stale_review_blocks(self):
        self.mutate("spec", lambda d: d.data["acceptance_criteria"][0].update(then="Kết quả đã đổi"))
        self.assert_block("STALE_INPUT")

    def test_path_traversal(self):
        for path in ("../escape.md", "..\\escape.md", "C:escape.md", "a:stream", "NUL.md", str(self.project.root / "file:stream")):
            with self.subTest(path=path), self.assertRaises(BAError):
                self.project.path(path)

    def test_rule_redefinition(self):
        self.mutate("spec", lambda d: d.data["business_rules"][0].update(rule="Mọi người xem mọi tài liệu"))
        self.assertIn("RULE_MISMATCH", self.codes("spec"))

    def test_no_capacity_cannot_be_confirmed(self):
        self.mutate("round-plan", lambda d: d.data["rounds"][0].update(status="Confirmed"))
        self.assertIn("CAPACITY_UNCONFIRMED", self.codes("round-plan"))

    def test_review_major_cannot_pass(self):
        self.mutate("review", lambda d: d.data["findings"].append({"finding_id": "FIND-001", "severity": "Major", "file": "spec.md",
            "section": "Acceptance Criteria", "evidence": "Thiếu nghiệm thu", "impact": "Không kiểm thử được", "recommendation": "Bổ sung AC", "status": "Open"}))
        self.assertIn("REVIEW_INCONSISTENT", self.codes("review"))

    def test_approval_hash_must_be_current(self):
        self.mutate("review", lambda d: d.data["coverage_notes"].append("Review refinement"))
        self.assertEqual(prepare(self.project, "PBI-001")["blocked"][0]["code"], "MISSING_APPROVAL")

    def test_source_cycle(self):
        self.mutate("brainstorm", lambda d: d.metadata["source_documents"].append({"path": self.project.relative(self.path("requirements")), "sha256": sha(self.path("requirements"))}))
        self.assertIn("SOURCE_CYCLE", self.codes("brainstorm"))

    def test_raw_markdown_evidence_is_hashed_but_not_ba_contract(self):
        path = self.project.root / "research.md"
        path.write_text("# Existing product research\nUser-supplied context.", encoding="utf-8")
        self.mutate("brainstorm", lambda d: d.metadata["source_documents"].append({"path": "research.md", "sha256": sha(path), "kind": "raw"}))
        self.assertEqual(self.codes("brainstorm"), set())
        path.write_text("changed research", encoding="utf-8")
        self.assertIn("STALE_INPUT", self.codes("brainstorm"))

    def test_raw_source_cannot_replace_required_ba_source(self):
        self.mutate("requirements", lambda d: d.metadata["source_documents"][0].update(kind="raw"))
        self.assertIn("MISSING_SOURCE_TYPE", self.codes("requirements"))

    def test_wrong_project(self):
        self.mutate("business", lambda d: d.metadata.update(project_id="other-project"))
        self.assertIn("PROJECT_MISMATCH", self.codes("business"))

    def test_uncovered_requirement(self):
        self.mutate("product-backlog", lambda d: d.data["pbis"].pop())
        self.assertIn("REQUIREMENT_COVERAGE", self.codes("product-backlog"))

    def test_publish_conflict_preserves_bytes(self):
        manifest = prepare(self.project, "PBI-001")
        publish(self.project, manifest)
        path = self.project.path(manifest["target"]) / "spec.md"
        path.write_text("user edit", encoding="utf-8")
        manifest = prepare(self.project, "PBI-001")
        self.assertTrue(manifest["blocked"])
        with self.assertRaises(BAError):
            publish(self.project, manifest)
        self.assertEqual(path.read_text(), "user edit")

    def test_duplicate_round_allocation(self):
        def change(d):
            rnd = copy.deepcopy(d.data["rounds"][0])
            rnd["round_id"] = "R2"
            d.data["rounds"].append(rnd)
        self.mutate("round-plan", change)
        self.assertIn("DUPLICATE_ALLOCATION", self.codes("round-plan"))

    def test_dependency_cycle(self):
        self.mutate("product-backlog", lambda d: d.data["pbis"][0].update(dependencies=["PBI-002"]))
        self.assertIn("DEPENDENCY_CYCLE", self.codes("product-backlog"))

    def test_trace_mismatch(self):
        self.mutate("spec", lambda d: d.data["traceability"][0].update(requirement_id="REQ-002"))
        self.assertIn("TRACE_MISMATCH", self.codes("spec"))

    def test_machine_prose_projection(self):
        path = self.path("business")
        text = path.read_text(encoding="utf-8")
        text = text.replace("| PBI-001 |", "| PBI-002 |")
        path.write_text(text, encoding="utf-8")
        self.assertIn("PROSE_DATA_MISMATCH", self.codes("business"))

    def test_renderer_shared_values_does_not_emit_aliases(self):
        doc = parse(self.path("business"))
        doc.data["solution"][0]["business_rule_refs"] = doc.data["business_rule_refs"]
        self.path("business").write_text(render(doc.metadata, doc.data, {h: "Fixture content" for h in HEADINGS["business"]}), encoding="utf-8")
        self.assertEqual(self.codes("business"), set())

    def test_duplicate_yaml_key(self):
        path = self.path("brainstorm")
        text = path.read_text(encoding="utf-8").replace("document_type: brainstorm", "document_type: brainstorm\ndocument_type: spec")
        path.write_text(text, encoding="utf-8")
        self.assertIn("INVALID_YAML", self.codes("brainstorm"))

    def test_duplicate_data_block(self):
        path = self.path("brainstorm")
        path.write_text(path.read_text(encoding="utf-8") + "\n<!-- BA-DATA:START -->", encoding="utf-8")
        self.assertIn("INVALID_DATA_BLOCK", self.codes("brainstorm"))

    def test_freshness_between_dryrun_and_apply(self):
        manifest = prepare(self.project, "PBI-001")
        self.path("spec").write_text(self.path("spec").read_text(encoding="utf-8") + "\n", encoding="utf-8")
        with self.assertRaises(BAError) as cm:
            publish(self.project, manifest)
        self.assertEqual(cm.exception.diagnostic["code"], "STALE_INPUT")

    def test_conditional_requires_explicit_draft_publication(self):
        self.mutate("review", lambda d: d.data.update(result="CONDITIONAL", readiness="Needs Refinement"))
        approve_fixture(self.project, "PBI-001")
        self.assertFalse(prepare(self.project, "PBI-001")["blocked"])
        path = self.plan / "approvals.json"
        approvals = json.loads(path.read_text(encoding="utf-8"))
        approvals["approvals"][-1]["decision"] = "Approved"
        path.write_text(json.dumps(approvals), encoding="utf-8")
        self.assertTrue(prepare(self.project, "PBI-001")["blocked"])

    def test_custom_prefixes_and_multi_project(self):
        project = build(Path(self.temp.name) / "other", pbi_prefix="ITEM", round_prefix="Cycle", publish_pair=True)
        manifest = prepare(project, "ITEM-001")
        self.assertIn("/Cycle1/ITEM-001-", manifest["entries"][0]["destination"])

    def test_cli_json_and_exit_codes(self):
        script = Path(__file__).resolve().parents[1] / "scripts" / "validate_ba_document.py"
        cmd = [sys.executable, str(script), "--project-config", str(self.project.config_path), "--file", str(self.path("spec")), "--check-refs", "--format", "json"]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["result"], "PASS")
        self.path("spec").write_text("bad", encoding="utf-8")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["result"], "FAIL")


if __name__ == "__main__":
    unittest.main()
