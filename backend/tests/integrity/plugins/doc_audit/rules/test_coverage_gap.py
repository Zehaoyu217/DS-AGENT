from datetime import date
from pathlib import Path

from backend.app.integrity.plugins.doc_audit.rules.coverage_gap import run
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


def _ctx(tmp_path: Path) -> ScanContext:
    g = tmp_path / "graphify"
    g.mkdir(parents=True, exist_ok=True)
    (g / "graph.json").write_text('{"nodes":[],"links":[]}', encoding="utf-8")
    return ScanContext(repo_root=tmp_path, graph=GraphSnapshot.load(tmp_path))


def test_no_issues_when_all_required_present(tmp_path: Path):
    docs = tmp_path / "docs"
    docs.mkdir()
    for name in ("dev-setup.md", "testing.md", "gotchas.md", "skill-creation.md", "log.md"):
        (docs / name).write_text("# x\n")

    cfg = {
        "coverage_required": [
            "dev-setup.md",
            "testing.md",
            "gotchas.md",
            "skill-creation.md",
            "log.md",
        ],
    }
    issues = run(_ctx(tmp_path), cfg, date(2026, 4, 17))
    assert issues == []


def test_missing_files_emit_one_issue_each(tmp_path: Path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "dev-setup.md").write_text("# x\n")
    # testing.md and log.md missing

    cfg = {"coverage_required": ["dev-setup.md", "testing.md", "log.md"]}
    issues = run(_ctx(tmp_path), cfg, date(2026, 4, 17))
    assert len(issues) == 2
    rules = {i.rule for i in issues}
    assert rules == {"doc.coverage_gap"}
    locations = {i.location for i in issues}
    assert locations == {"docs/testing.md", "docs/log.md"}
    for i in issues:
        assert i.severity == "WARN"
        assert i.evidence["expected_path"].startswith("docs/")


def test_handles_missing_docs_directory(tmp_path: Path):
    cfg = {"coverage_required": ["dev-setup.md"]}
    issues = run(_ctx(tmp_path), cfg, date(2026, 4, 17))
    assert len(issues) == 1
    assert issues[0].location == "docs/dev-setup.md"
