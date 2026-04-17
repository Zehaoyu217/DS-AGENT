from datetime import date
from pathlib import Path
from unittest.mock import patch

from backend.app.integrity.plugins.doc_audit.rules.stale_candidate import run
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


def _write(repo: Path, rel: str, content: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _ctx(repo: Path) -> ScanContext:
    g = repo / "graphify"
    g.mkdir(parents=True, exist_ok=True)
    (g / "graph.json").write_text('{"nodes":[],"links":[]}', encoding="utf-8")
    return ScanContext(repo_root=repo, graph=GraphSnapshot.load(repo))


_CFG = {
    "doc_roots": ["*.md", "docs/**/*.md"],
    "excluded_paths": [],
    "seed_docs": ["CLAUDE.md"],
    "claude_ignore_file": ".claude-ignore",
    "thresholds": {"stale_days": 90},
}


def _patched_git_log(*, doc_iso: str | None, src_iso: str | None):
    """Return a context manager that patches GitLog.last_commit_iso."""
    def fake_last_commit_iso(self, rel_path: str) -> str | None:
        if rel_path.endswith(".md"):
            return doc_iso
        return src_iso

    return patch(
        "backend.app.integrity.plugins.doc_audit.rules.stale_candidate.GitLog.last_commit_iso",
        fake_last_commit_iso,
    )


def test_stale_doc_with_changed_ref_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/old.md", "See `backend/app/foo.py`.\n")
    _write(tmp_path, "backend/app/foo.py", "# changed\n")

    with _patched_git_log(doc_iso="2025-01-01T00:00:00+00:00", src_iso="2026-04-17T00:00:00+00:00"):
        issues = run(_ctx(tmp_path), _CFG, date(2026, 4, 17))

    matching = [i for i in issues if "old.md" in i.location]
    assert len(matching) == 1
    issue = matching[0]
    assert issue.rule == "doc.stale_candidate"
    assert issue.severity == "INFO"
    assert "backend/app/foo.py" in issue.evidence["changed_refs"]


def test_recent_doc_not_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/fresh.md", "See `backend/app/foo.py`.\n")
    _write(tmp_path, "backend/app/foo.py", "# changed\n")

    with _patched_git_log(doc_iso="2026-04-15T00:00:00+00:00", src_iso="2026-04-17T00:00:00+00:00"):
        issues = run(_ctx(tmp_path), _CFG, date(2026, 4, 17))

    assert all("fresh.md" not in i.location for i in issues)


def test_old_doc_with_no_changed_ref_not_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/old-stable.md", "See `backend/app/foo.py`.\n")
    _write(tmp_path, "backend/app/foo.py", "# unchanged\n")

    # src_iso older than doc_iso → ref didn't change after doc
    with _patched_git_log(doc_iso="2025-12-01T00:00:00+00:00", src_iso="2025-01-01T00:00:00+00:00"):
        issues = run(_ctx(tmp_path), _CFG, date(2026, 4, 17))

    assert all("old-stable.md" not in i.location for i in issues)


def test_uncommitted_doc_skipped(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/new.md", "See `backend/app/foo.py`.\n")
    _write(tmp_path, "backend/app/foo.py", "# anything\n")

    with _patched_git_log(doc_iso=None, src_iso="2026-04-17T00:00:00+00:00"):
        issues = run(_ctx(tmp_path), _CFG, date(2026, 4, 17))

    assert all("new.md" not in i.location for i in issues)
