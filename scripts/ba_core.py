"""Shared parsing, safe paths, contracts and reference validation for BA Skills Kit."""
from __future__ import annotations

import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath

import yaml
from jsonschema import Draft202012Validator

KIT = Path(__file__).resolve().parents[1]
# CLI pipes on Windows may otherwise use cp1252 and crash on Vietnamese diagnostics.
for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")
START, END = "<!-- BA-DATA:START -->", "<!-- BA-DATA:END -->"
HEADINGS = {
    "brainstorm": ["Product Overview", "Vision", "Target Users", "Problems", "Capabilities", "Goals", "Scope", "Assumptions", "Open Questions", "Metrics"],
    "requirements": ["Actors", "Functional Requirements", "Business Rules", "Data", "Permissions", "As-Is / To-Be", "Flows", "Edge Cases", "Nonfunctional Considerations", "Coverage", "Open Questions"],
    "product-backlog": ["Product Backlog Overview", "Epics", "Features", "PBIs", "INVEST", "Requirement Coverage", "Dependencies", "Open Questions"],
    "round-plan": ["Round Goals", "Allocations", "Dependencies", "Capacity Gaps", "Approval State", "Change History"],
    "business": ["Thông tin PBI", "Câu chuyện nghiệp vụ", "Vấn đề", "Đối tượng", "Mục tiêu", "Giá trị", "As-Is/To-Be", "Giải pháp phần mềm chi tiết", "Scope", "Rules", "Dependencies", "Risks", "Open Questions", "Sources"],
    "spec": ["PBI Information", "User Stories", "Preconditions", "Postconditions", "Main Flow", "Alternative Flows", "Exception Flows", "Business Rules", "Permissions", "Data and States", "Edge Cases", "Acceptance Criteria", "Traceability", "Scope", "Open Questions"],
    "review": ["Review Result", "Findings", "Coverage", "Readiness", "Blockers", "Sources"],
    "workflow-state": ["Current Phase", "Completed", "Pending", "Blockers", "Artifacts", "Approvals", "Recovery"],
}
REQUIRED_SOURCES = {
    "brainstorm": set(), "requirements": {"brainstorm"},
    "product-backlog": {"brainstorm", "requirements"}, "round-plan": {"product-backlog", "requirements"},
    "business": {"brainstorm", "requirements", "product-backlog"},
    "spec": {"business", "requirements", "product-backlog"},
    "review": {"business", "spec", "requirements", "product-backlog"}, "workflow-state": set(),
}
COLLECTION_IDS = {"capabilities": "capability_id", "actors": "actor_id", "requirements": "requirement_id",
    "epics": "epic_id", "features": "feature_id", "pbis": "pbi_id", "rounds": "round_id",
    "business_rules": "br_id", "flows": "flow_id", "edge_cases": "ec_id",
    "acceptance_criteria": "ac_id", "findings": "finding_id"}
REF_KEYS = {"capability_refs": "CAP", "requirement_refs": "REQ", "business_rule_refs": "BR",
    "related_br_refs": "BR", "br_refs": "BR", "flow_refs": "FLOW", "related_ac_refs": "AC",
    "ac_refs": "AC", "edge_case_refs": "EC", "ec_refs": "EC", "pbi_refs": "PBI"}


class BAError(Exception):
    def __init__(self, code, message, file="", location="/", fix="Sửa input rồi chạy lại validator."):
        super().__init__(message)
        self.diagnostic = {"severity": "ERROR", "code": code, "file": str(file), "location": location,
                           "message": message, "suggested_fix": fix}


class StrictLoader(yaml.SafeLoader):
    pass


def mapping(loader, node, deep=False):
    result = {}
    for k, v in node.value:
        key = loader.construct_object(k, deep=deep)
        if not isinstance(key, str) or key in result:
            raise ValueError(f"Duplicate or non-string YAML key: {key!r}")
        result[key] = loader.construct_object(v, deep=deep)
    return result


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def yaml_load(text, file=""):
    try:
        if any(isinstance(t, yaml.tokens.AliasToken) for t in yaml.scan(text)):
            raise ValueError("YAML aliases are not supported in interchange documents")
        return yaml.load(text, Loader=StrictLoader)
    except (yaml.YAMLError, ValueError, TypeError) as exc:
        raise BAError("INVALID_YAML", str(exc), file) from exc


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def schema(name):
    return json.loads((KIT / "contracts" / f"{name}.schema.json").read_text(encoding="utf-8"))


def errors_for(name, value, file):
    return [{"severity": "ERROR", "code": "SCHEMA_INVALID", "file": str(file),
             "location": "/" + "/".join(map(str, e.absolute_path)), "message": e.message,
             "suggested_fix": f"Đối chiếu contracts/{name}.schema.json; không tự duyệt quyết định nghiệp vụ."}
            for e in Draft202012Validator(schema(name)).iter_errors(value)]


def safe_path(root, value):
    """Reject lexical traversal, foreign drive paths and symlink/junction escapes."""
    root = Path(root).resolve()
    value = str(value)
    win = PureWindowsPath(value)
    if ".." in win.parts or "\x00" in value:
        raise BAError("UNSAFE_PATH", "Path traversal is not allowed", value)
    if Path(value).is_absolute():
        path = Path(value)
    elif win.drive or value.startswith(("/", "\\")):
        raise BAError("UNSAFE_PATH", "Foreign or drive-relative path", value)
    else:
        # Avoid NTFS alternate streams and Windows reserved names on every OS.
        if ":" in value:
            raise BAError("UNSAFE_PATH", "Alternate data stream is not allowed", value)
        path = root / value.replace("\\", "/")
    for part in path.parts[len(path.anchor and Path(path.anchor).parts or ()):]:
        if any(c in part for c in ':*?<>|"') or part.endswith((".", " ")) or re.match(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\.|$)", part, re.I):
            raise BAError("UNSAFE_PATH", "Unsafe platform filename", value)
    resolved = path.resolve()
    if not resolved.is_relative_to(root):
        raise BAError("UNSAFE_PATH", "Path escapes repository root", value)
    return resolved


@dataclass
class Project:
    config_path: Path
    root: Path
    config: dict

    @staticmethod
    def find_config(start=None):
        """Look only in the working project, preferring its .temp config over legacy root config."""
        directory = Path(start or Path.cwd()).absolute()
        preferred = directory / ".temp" / "ba-project.yaml"
        legacy = directory / "ba-project.yaml"
        for candidate in (preferred, legacy):
            if candidate.exists() or candidate.is_symlink():
                return candidate
        return preferred

    @classmethod
    def load(cls, config_path=None):
        requested = Path(config_path if config_path is not None else cls.find_config()).absolute()
        # Recognize only the canonical .temp/ba-project.yaml layout. Anchor before resolving
        # the file so a .temp symlink cannot silently change the chosen project boundary.
        # Path.match follows the platform's case rules (Windows accepts .TEMP/BA-PROJECT.YAML).
        in_temp = requested.match(".temp/ba-project.yaml")
        anchor = requested.parent.parent.resolve() if in_temp else requested.resolve().parent
        path = safe_path(anchor, requested) if in_temp else requested.resolve()
        if not path.is_file():
            raise BAError("MISSING_CONFIG", "Project config not found", path,
                          fix="Tạo .temp/ba-project.yaml từ template tại project đang mở và xác nhận các giá trị thiết yếu với người dùng.")
        cfg = yaml_load(path.read_text(encoding="utf-8-sig"), path)
        issues = errors_for("project-config", cfg, path)
        if issues:
            raise BAError("INVALID_CONFIG", issues[0]["message"], path)
        # Canonical config: repository_root is relative to the project above .temp.
        # Legacy config: preserve its original directory-based resolution.
        root = safe_path(anchor, cfg["repository_root"])
        if not root.is_dir():
            raise BAError("INVALID_CONFIG", "repository_root must be an existing directory", root)
        output = safe_path(root, cfg["output_root"])
        planning = safe_path(root, cfg["planning_dir"])
        temp = safe_path(root, ".temp")
        if not planning.is_relative_to(temp):
            raise BAError("PLANNING_LAYOUT", "planning_dir must be .temp or a subdirectory of .temp", path, "/planning_dir",
                          "Đổi planning_dir thành .temp. Với dữ liệu cũ, chuyển hồ sơ khỏi .specify rồi cập nhật refs/hash và review theo conventions/BA-CONVENTIONS.md; không xóa dữ liệu.")
        if output.is_relative_to(temp) or temp.is_relative_to(output):
            raise BAError("INVALID_CONFIG", "output_root and .temp must not overlap or contain one another", path)
        project = cls(path, root, cfg)
        check_output_layout(project)
        return project

    def path(self, value):
        return safe_path(self.root, value)

    def relative(self, path):
        return self.path(path).relative_to(self.root).as_posix()

    @property
    def planning(self):
        return self.path(self.config["planning_dir"])

    @property
    def temp(self):
        return self.path(".temp")

    @property
    def output(self):
        return self.path(self.config["output_root"])

    def temporary_path(self, value):
        path = self.path(value)
        if not path.is_relative_to(self.temp):
            raise BAError("TEMP_LAYOUT", "Intermediate BA artifacts must be written under project/.temp", path,
                          fix="Ghi exploration/backlog/drafts/reviews/state/logs vào planning_dir dưới .temp; .specify chỉ dành cho cặp đã publish.")
        return path


def check_output_layout(project):
    """Read-only structural audit: output contains only Round/PBI/{business.md,spec.md}."""
    output = project.output
    if not output.exists():
        return
    if not output.is_dir():
        raise BAError("OUTPUT_LAYOUT", "output_root must be a directory", output)
    seen = {}
    round_pattern = re.escape(project.config["round_prefix"]) + r"[1-9][0-9]*"
    pbi_pattern = r"(" + re.escape(project.config["pbi_prefix"]) + r"-[0-9]{3,})-[a-z0-9]+(?:-[a-z0-9]+)*"
    for rnd in sorted(output.iterdir()):
        project.path(rnd)
        if rnd.is_symlink() or not rnd.is_dir() or not re.fullmatch(round_pattern, rnd.name):
            raise BAError("OUTPUT_LAYOUT", "Only Round directories are allowed in output_root", rnd,
                          fix="Chuyển hồ sơ trung gian sang .temp bằng migration có kiểm soát; không tự xóa file cũ.")
        if rnd.resolve().parent != output:
            raise BAError("UNSAFE_PATH", "Round directory resolves outside output_root", rnd)
        for folder in sorted(rnd.iterdir()):
            project.path(folder)
            match = re.fullmatch(pbi_pattern, folder.name)
            if folder.is_symlink() or not folder.is_dir() or not match:
                raise BAError("OUTPUT_LAYOUT", "Round may contain only PBI-ID-slug directories", folder)
            if folder.resolve().parent != rnd.resolve():
                raise BAError("UNSAFE_PATH", "PBI directory resolves outside its Round", folder)
            identifier = match.group(1)
            if identifier in seen:
                raise BAError("DUPLICATE_PUBLISHED_PBI", f"{identifier} already exists at {seen[identifier]}", folder)
            seen[identifier] = folder
            if {p.name for p in folder.iterdir()} != {"business.md", "spec.md"}:
                raise BAError("PUBLISH_CONFLICT", "Published PBI must contain exactly business.md and spec.md", folder)
            for name in ("business.md", "spec.md"):
                file = folder / name
                project.path(file)
                if file.is_symlink() or not file.is_file() or file.resolve().parent != folder.resolve():
                    raise BAError("UNSAFE_PATH", "Published pair must be regular files inside the PBI directory", file)


def check_document_location(project, doc):
    """Canonical intermediates stay in .temp; only correctly addressed PBI pairs may be published."""
    kind = doc.metadata["document_type"]
    if doc.path.is_relative_to(project.temp):
        return
    if kind in ("business", "spec") and doc.path.is_relative_to(project.output):
        data = doc.data
        if "round_id" not in data:
            raise BAError("DOCUMENT_LOCATION", "Published PBI must have a round_id", doc.path)
        expected = project.path(project.output / data["round_id"] / f"{data['pbi_id']}-{slugify(data['title'])}" / f"{kind}.md")
        if doc.path == expected:
            return
    raise BAError("DOCUMENT_LOCATION", "BA intermediates belong in .temp; published files must match Round/PBI paths", doc.path)


@dataclass
class Document:
    path: Path
    metadata: dict
    data: dict
    prose: str


def parse(path):
    path = Path(path)
    if not path.is_file():
        raise BAError("MISSING_INPUT", "Input document not found", path,
                      fix="Chạy skill tạo tài liệu này trước; skill đơn lẻ không tự tái tạo nguồn.")
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeError as exc:
        raise BAError("INVALID_ENCODING", "Expected UTF-8 Markdown", path) from exc
    fm = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    if not fm:
        raise BAError("MISSING_METADATA", "Expected YAML front matter at start", path)
    body = text[fm.end():]
    if body.count(START) != 1 or body.count(END) != 1:
        raise BAError("INVALID_DATA_BLOCK", "Expected exactly one BA-DATA marker pair", path)
    block = re.search(re.escape(START) + r"\s*```yaml\n(.*?)\n```\s*" + re.escape(END), body, re.S)
    if not block:
        raise BAError("INVALID_DATA_BLOCK", "Expected fenced yaml inside BA-DATA markers", path)
    return Document(path, yaml_load(fm.group(1), path), yaml_load(block.group(1), path),
                    body[:block.start()] + body[block.end():])


def entities(data):
    for collection, idkey in COLLECTION_IDS.items():
        for item in data.get(collection, []):
            yield idkey, item[idkey], item


def summary(data):
    rows = []
    if "pbi_id" in data:
        rows.append((data["pbi_id"], data["title"], data.get("result", "—")))
    for _, identifier, item in entities(data):
        rows.append((identifier, item.get("title", item.get("name", item.get("goal", item.get("evidence", "—")))),
                     item.get("confirmation_status", item.get("approval_status", item.get("status", "—")))))
    escape = lambda value: str(value).replace("|", "&#124;").replace("\n", " ")
    return "| ID | Title | State |\n| --- | --- | --- |\n" + "\n".join("| " + " | ".join(map(escape, row)) + " |" for row in rows)


def render(metadata, data, sections):
    """Render actual author-supplied prose plus a deterministic ID/title/status projection."""
    class InterchangeDumper(yaml.SafeDumper):
        def ignore_aliases(self, value):
            return True

    def dump(value):
        return yaml.dump(value, Dumper=InterchangeDumper, allow_unicode=True, sort_keys=False, width=110).rstrip()
    return ("---\n" + dump(metadata) + "\n---\n# " + metadata["document_type"] + "\n\n" + START +
            "\n```yaml\n" + dump(data) + "\n```\n" + END + "\n\n" +
            "\n\n".join(f"## {heading}\n\n{content}" for heading, content in sections.items()) +
            "\n\n## Contract Summary\n\n" + summary(data) + "\n")


def walk(value, location=""):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key, item, location + "/" + key
            yield from walk(item, location + "/" + key)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk(item, location + "/" + str(index))


class Validator:
    def __init__(self, project, check_refs=True):
        self.project, self.check_refs = project, check_refs
        self.diagnostics, self.documents, self.visiting = [], {}, set()
        self.fingerprints = {}

    def issue(self, code, doc, message, location="/", severity="ERROR", fix="Sửa tài liệu nguồn bằng skill tương ứng rồi tái kiểm tra downstream."):
        self.diagnostics.append({"severity": severity, "code": code, "file": str(doc.path),
                                 "location": location, "message": message, "suggested_fix": fix})

    def validate(self, file, expected_type=None, pbi_id=None):
        try:
            path = self.project.path(file)
            if path in self.visiting:
                raise BAError("SOURCE_CYCLE", "Cyclic source document chain", path)
            if path in self.documents:
                doc = self.documents[path]
            else:
                self.visiting.add(path)
                try:
                    doc = self._validate(path)
                    self.documents[path] = doc
                finally:
                    self.visiting.discard(path)
            if doc and expected_type and doc.metadata["document_type"] != expected_type:
                self.issue("WRONG_DOCUMENT_TYPE", doc, f"Expected {expected_type}")
            if doc and pbi_id and doc.metadata.get("pbi_id") != pbi_id:
                self.issue("PBI_MISMATCH", doc, f"Expected {pbi_id}")
            return doc
        except (BAError, OSError) as exc:
            if isinstance(exc, BAError):
                self.diagnostics.append(exc.diagnostic)
            else:
                self.diagnostics.append(BAError("IO_ERROR", str(exc), file).diagnostic)
            return None

    def _validate(self, path):
        initial_hash = sha(path) if path.is_file() else None
        if path.is_relative_to(self.project.output):
            return self._validate_public(path, initial_hash)
        doc = parse(path)
        issues = errors_for("metadata", doc.metadata, path)
        self.diagnostics.extend(issues)
        if issues:
            return None
        meta, data = doc.metadata, doc.data
        kind = meta["document_type"]
        issues = errors_for(kind, data, path)
        self.diagnostics.extend(issues)
        if issues:
            return None
        if meta["project_id"] != self.project.config["project_id"]:
            self.issue("PROJECT_MISMATCH", doc, "project_id differs from config")
        check_document_location(self.project, doc)
        expected_generator = "ba-workflow" if kind == "workflow-state" else "ba-" + kind
        if meta["generated_by"] != expected_generator:
            self.issue("GENERATOR_MISMATCH", doc, f"Expected {expected_generator}")
        actual_headings = re.findall(r"^## (.+)$", doc.prose, re.M)
        for heading in HEADINGS[kind] + ["Contract Summary"]:
            if actual_headings.count(heading) != 1:
                self.issue("MISSING_HEADING", doc, f"Expected one heading: {heading}")
        projection = re.search(r"^## Contract Summary\s*\n(.*?)(?=^## |\Z)", doc.prose, re.M | re.S)
        if not projection or projection.group(1).strip() != summary(data).strip():
            self.issue("PROSE_DATA_MISMATCH", doc, "Contract Summary ID/title/state table differs from BA-DATA")
        for h in HEADINGS[kind]:
            section = re.search(r"^## " + re.escape(h) + r"\n(.*?)(?=^## |\Z)", doc.prose, re.M | re.S)
            if section and not section.group(1).strip():
                self.issue("EMPTY_SECTION", doc, f"Empty section: {h}")
        known = set()
        for _, identifier, _ in entities(data):
            if identifier in known:
                self.issue("DUPLICATE_ID", doc, identifier)
            known.add(identifier)
        for key in ("pbi_id", "epic_id", "feature_id", "round_id", "requirement_refs"):
            if key in data and data[key] != meta.get(key):
                self.issue("METADATA_MISMATCH", doc, f"{key} differs between metadata and BA-DATA")
        for key, value, loc in walk(data):
            if key in ("pbi_id",) or key in ("pbi_refs", "unassigned_pbis"):
                for identifier in value if isinstance(value, list) else [value]:
                    if not re.fullmatch(re.escape(self.project.config["pbi_prefix"]) + r"-[0-9]{3,}", identifier):
                        self.issue("ID_PREFIX", doc, f"Unexpected PBI prefix: {identifier}", loc)
            if key == "round_id" and not re.fullmatch(re.escape(self.project.config["round_prefix"]) + r"[1-9][0-9]*", value):
                self.issue("ID_PREFIX", doc, f"Unexpected Round prefix: {value}", loc)
        for flow in data.get("flows", []):
            prefix = {"main": "MF", "alternative": "AF", "exception": "EF"}[flow["kind"]]
            if not flow["flow_id"].startswith(prefix + "-") or [s["step"] for s in flow["steps"]] != list(range(1, len(flow["steps"]) + 1)):
                self.issue("INVALID_FLOW", doc, f"Invalid flow kind or step sequence: {flow['flow_id']}")
        if kind in ("requirements", "spec") and not any(f["kind"] == "main" for f in data["flows"]):
            self.issue("MISSING_MAIN_FLOW", doc, "At least one main flow is required")
        if kind == "spec":
            if set(data["requirement_refs"]) != {x["requirement_id"] for x in data["traceability"]}:
                self.issue("TRACE_COVERAGE", doc, "Traceability must cover exactly the selected requirements")
            for ec in data["edge_cases"]:
                if "open_question" in ec:
                    self.issue("OPEN_EDGE_CASE", doc, ec["open_question"], severity="WARNING")
        if kind == "review":
            severe = any(f["status"] == "Open" and f["severity"] in ("Critical", "Major") for f in data["findings"])
            if (severe or data["blockers"]) and data["result"] != "FAIL":
                self.issue("REVIEW_INCONSISTENT", doc, "Open Critical/Major findings or blockers require FAIL")
            expected = {"PASS": "Ready", "CONDITIONAL": "Needs Refinement", "FAIL": "Blocked"}[data["result"]]
            if data["readiness"] != expected:
                self.issue("REVIEW_INCONSISTENT", doc, "readiness does not match result")
            if any(f["status"] == "Open" for f in data["findings"]) and data["result"] == "PASS":
                self.issue("REVIEW_INCONSISTENT", doc, "Open minor refinements require CONDITIONAL")
        sources = []
        seen_paths = set()
        for source in meta["source_documents"]:
            source_path = self.project.path(source["path"])
            if source_path in seen_paths:
                self.issue("DUPLICATE_SOURCE", doc, source["path"])
            seen_paths.add(source_path)
            if not source_path.is_file():
                self.issue("MISSING_INPUT", doc, source["path"], fix="Chạy skill upstream tạo file còn thiếu, không đoán dữ liệu thay thế.")
                continue
            source_hash = sha(source_path)
            self.fingerprints[source_path] = source_hash
            if source_hash != source["sha256"]:
                self.issue("STALE_INPUT", doc, f"Source bytes changed: {source['path']}")
            if self.check_refs and source.get("kind", "ba" if source_path.suffix.lower() == ".md" else "raw") == "ba":
                source_doc = self.validate(source_path)
                if source_doc:
                    sources.append(source_doc)
        if self.check_refs:
            for required in REQUIRED_SOURCES[kind] - {s.metadata["document_type"] for s in sources}:
                self.issue("MISSING_SOURCE_TYPE", doc, f"Missing validated {required} input",
                           fix=f"Chạy ba-{required} rồi thêm path và SHA-256 đúng vào source_documents.")
            self._references(doc, sources)
        else:
            self.issue("REFS_NOT_CHECKED", doc, "Cross-document references were not checked", severity="WARNING")
        if sha(path) != initial_hash:
            self.issue("STALE_INPUT", doc, "Document changed during validation; retry from a stable snapshot")
        self.fingerprints[path] = initial_hash
        return doc

    def _validate_public(self, path, initial_hash):
        from ba_public import check_public_text, public_bytes

        parts = path.relative_to(self.project.output).parts
        match = re.fullmatch(r"(" + re.escape(self.project.config["pbi_prefix"]) + r"-[0-9]{3,})-.+", parts[1]) if len(parts) == 3 else None
        if not match or parts[2] not in ("business.md", "spec.md"):
            raise BAError("DOCUMENT_LOCATION", "Expected a published Round/PBI business/spec file", path)
        kind, pbi_id = path.stem, match.group(1)
        draft = self.project.planning / "drafts" / pbi_id / path.name
        canonical = self.require_valid(draft, kind, pbi_id)
        if not path.is_file():
            raise BAError("MISSING_INPUT", "Published document not found", path)
        content = path.read_bytes()
        try:
            text = content.decode("utf-8")
        except UnicodeError as exc:
            raise BAError("INVALID_ENCODING", "Expected UTF-8 Markdown", path) from exc
        check_public_text(text, path)
        doc = Document(path, canonical.metadata, canonical.data, text)
        check_document_location(self.project, doc)
        if content != public_bytes(self.project, canonical, self):
            self.issue("PUBLIC_CONTENT_MISMATCH", doc, "Published prose differs from the current validated draft",
                       fix="So sánh bản bàn giao với draft trong .temp; review/publish lại theo quy trình, không tự ghi đè.")
        if sha(path) != initial_hash:
            self.issue("STALE_INPUT", doc, "Document changed during validation")
        self.fingerprints[path] = initial_hash
        return doc

    def _references(self, doc, sources):
        data, kind = doc.data, doc.metadata["document_type"]
        if kind == "workflow-state":
            # State approval actors are humans, not ACT IDs; approval PBI lists are historical scope.
            for artifact in data["artifacts"]:
                self.project.path(artifact["path"])
            for approval in data["approvals"]:
                for source in approval["documents"]:
                    self.project.path(source["path"])
            return
        pools = {k: set() for k in ("CAP", "REQ", "BR", "FLOW", "AC", "EC", "PBI", "EPIC", "FEAT", "ACT", "ROUND")}
        idtypes = {"capability_id": "CAP", "requirement_id": "REQ", "br_id": "BR", "flow_id": "FLOW", "ac_id": "AC",
                   "ec_id": "EC", "pbi_id": "PBI", "epic_id": "EPIC", "feature_id": "FEAT", "actor_id": "ACT", "round_id": "ROUND"}
        for source in sources + [doc]:
            for idkey, identifier, _ in entities(source.data):
                if idkey not in idtypes:
                    continue
                group = idtypes[idkey]
                # AC/EC/Flow IDs are scoped to their document/PBI. Never borrow from another document.
                if group in ("AC", "EC", "FLOW") and source is not doc:
                    continue
                pools[group].add(identifier)
        for key, value, loc in walk(data):
            if key in REF_KEYS:
                group = REF_KEYS[key]
                for identifier in value:
                    if identifier not in pools[group]:
                        self.issue("BROKEN_REF", doc, f"{key}: {identifier} does not exist in validated scope", loc)
            if kind == "requirements" and key == "actor" and value not in pools["ACT"]:
                self.issue("BROKEN_REF", doc, f"Unknown actor {value}", loc)
        bytype = {}
        for source in sources:
            t = source.metadata["document_type"]
            if t in bytype:
                self.issue("AMBIGUOUS_SOURCE", doc, f"Multiple sources of type {t}")
            bytype[t] = source
        backlog = doc if kind == "product-backlog" else bytype.get("product-backlog")
        if backlog:
            features = {x["feature_id"]: x for x in backlog.data["features"]}
            epics = {x["epic_id"] for x in backlog.data["epics"]}
            pbis = {x["pbi_id"]: x for x in backlog.data["pbis"]}
            if kind == "product-backlog":
                for feature in features.values():
                    if feature["epic_id"] not in epics:
                        self.issue("BROKEN_REF", doc, f"Feature parent missing: {feature['feature_id']}")
                for pbi in pbis.values():
                    feature = features.get(pbi["feature_id"])
                    if not feature or pbi["epic_id"] != feature["epic_id"]:
                        self.issue("PARENT_MISMATCH", doc, pbi["pbi_id"])
                    elif not set(pbi["requirement_refs"]).issubset(feature["requirement_refs"]):
                        self.issue("SCOPE_MISMATCH", doc, "PBI requirements exceed feature scope")
                    if set(pbi["dependencies"]) - pbis.keys():
                        self.issue("BROKEN_REF", doc, f"Missing PBI dependency: {pbi['pbi_id']}")
                self._cycles(doc, {p: v["dependencies"] for p, v in pbis.items()})
                covered = {r for p in pbis.values() for r in p["requirement_refs"]}
                unassigned = {r["requirement_id"] for r in data["unassigned_requirements"]}
                if covered & unassigned or covered | unassigned != pools["REQ"]:
                    self.issue("REQUIREMENT_COVERAGE", doc, "Each REQ must be covered or explicitly unassigned with reason")
            if kind in ("business", "spec", "review"):
                pbi = pbis.get(data["pbi_id"])
                if not pbi:
                    self.issue("PBI_MISMATCH", doc, "PBI does not exist in backlog")
                else:
                    for field in ("epic_id", "feature_id", "requirement_refs", "title"):
                        if data[field] != pbi[field]:
                            self.issue("PBI_MISMATCH", doc, f"{field} differs from selected backlog PBI")
                    if kind in ("business", "spec") and (data["scope"] != pbi["scope"] or data["out_of_scope"] != pbi["out_of_scope"]):
                        self.issue("SCOPE_MISMATCH", doc, "Scope differs from selected backlog PBI")
                    if kind == "business" and data["dependencies"] != pbi["dependencies"]:
                        self.issue("SCOPE_MISMATCH", doc, "Business dependencies differ from backlog")
                    for key, value, loc in walk(data):
                        if key == "requirement_refs" and not set(value).issubset(pbi["requirement_refs"]):
                            self.issue("SCOPE_MISMATCH", doc, "Requirements outside selected PBI", loc)
                for source in sources:
                    if source.metadata["document_type"] in ("business", "spec") and source.metadata["pbi_id"] != data["pbi_id"]:
                        self.issue("PBI_MISMATCH", doc, "Source business/spec belongs to another PBI")
                plan = bytype.get("round-plan")
                if plan and "round_id" in data:
                    assignments = [r["round_id"] for r in plan.data["rounds"] if data["pbi_id"] in r["pbi_refs"]]
                    if assignments != [data["round_id"]]:
                        self.issue("ROUND_MISMATCH", doc, "Round differs from active allocation")
            if kind == "round-plan":
                allocations = {}
                rounds = {r["round_id"]: i for i, r in enumerate(data["rounds"])}
                for index, rnd in enumerate(data["rounds"]):
                    for dependency in rnd["dependencies"]:
                        if dependency not in rounds or rounds[dependency] >= index:
                            self.issue("DEPENDENCY_ORDER", doc, f"Round dependency must be earlier: {dependency}")
                    for identifier in rnd["pbi_refs"]:
                        if identifier in allocations:
                            self.issue("DUPLICATE_ALLOCATION", doc, identifier)
                        allocations[identifier] = index
                    if not rnd["capacity_assumptions"]:
                        self.issue("CAPACITY_UNKNOWN", doc, rnd["round_id"], severity="WARNING")
                        if rnd["status"] != "Proposed":
                            self.issue("CAPACITY_UNCONFIRMED", doc, "Without capacity evidence, allocation must remain Proposed")
                if set(allocations) & set(data["unassigned_pbis"]) or set(allocations) | set(data["unassigned_pbis"]) != set(pbis):
                    self.issue("PBI_COVERAGE", doc, "Every PBI must be allocated once or unassigned")
                for identifier, index in allocations.items():
                    for dependency in pbis.get(identifier, {}).get("dependencies", []):
                        if dependency not in allocations or allocations[dependency] > index:
                            self.issue("DEPENDENCY_ORDER", doc, f"{identifier} requires {dependency} in same/earlier Round")
        if kind == "spec":
            reqdoc = bytype.get("requirements")
            source_rules = {r["br_id"]: r for r in reqdoc.data["business_rules"]} if reqdoc else {}
            for rule in data["business_rules"]:
                original = source_rules.get(rule["br_id"])
                if original and any(rule[field] != original[field] for field in ("title", "rule", "confirmation_status")):
                    self.issue("RULE_MISMATCH", doc, f"Source rule redefined under the same ID: {rule['br_id']}")
            records = {idkey: {identifier: item for k, identifier, item in entities(data) if k == idkey}
                       for idkey in ("br_id", "flow_id", "ec_id", "ac_id")}
            for row in data["traceability"]:
                for field, idkey in (("br_refs", "br_id"), ("flow_refs", "flow_id"), ("ec_refs", "ec_id"), ("ac_refs", "ac_id")):
                    for identifier in row[field]:
                        item = records[idkey].get(identifier)
                        if not item or row["requirement_id"] not in item["requirement_refs"]:
                            self.issue("TRACE_MISMATCH", doc, f"{row['requirement_id']} not supported by {identifier}")
            covered_ac = {a for row in data["traceability"] for a in row["ac_refs"]}
            if covered_ac != set(records["ac_id"]):
                self.issue("TRACE_COVERAGE", doc, "Every AC must appear in traceability")

    def _cycles(self, doc, graph):
        visited, active = set(), set()
        def visit(node):
            if node in active:
                self.issue("DEPENDENCY_CYCLE", doc, node)
                return
            if node in visited:
                return
            active.add(node)
            for dependency in graph.get(node, []):
                visit(dependency)
            active.remove(node)
            visited.add(node)
        for node in graph:
            visit(node)

    @property
    def ok(self):
        return not any(d["severity"] == "ERROR" for d in self.diagnostics)

    def require_valid(self, file, expected_type=None, pbi_id=None):
        doc = self.validate(file, expected_type, pbi_id)
        if not self.ok or doc is None:
            first = next(d for d in self.diagnostics if d["severity"] == "ERROR")
            raise BAError(first["code"], first["message"], first["file"], first["location"], first["suggested_fix"])
        return doc


def slugify(text):
    text = text.lower().replace("đ", "d")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return slug or "item"
