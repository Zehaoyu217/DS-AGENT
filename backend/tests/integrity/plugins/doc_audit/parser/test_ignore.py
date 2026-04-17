from pathlib import Path

from backend.app.integrity.plugins.doc_audit.parser.ignore import IgnoreMatcher


def test_empty_when_file_missing(tmp_path: Path):
    matcher = IgnoreMatcher.load(tmp_path / "missing", repo_root=tmp_path)
    assert not matcher.matches("docs/anything.md")
    assert matcher.patterns == ()


def test_matches_glob_patterns(tmp_path: Path):
    ignore = tmp_path / ".claude-ignore"
    ignore.write_text(
        "# top comment\n"
        "docs/draft/**\n"
        "knowledge/wiki/scratch/*.md\n"
        "\n"  # blank line
        "*.tmp.md\n",
        encoding="utf-8",
    )
    matcher = IgnoreMatcher.load(ignore, repo_root=tmp_path)
    assert matcher.matches("docs/draft/notes.md")
    assert matcher.matches("docs/draft/sub/deep.md")
    assert matcher.matches("knowledge/wiki/scratch/idea.md")
    assert matcher.matches("anything.tmp.md")
    assert not matcher.matches("docs/dev-setup.md")
    assert not matcher.matches("knowledge/wiki/working.md")


def test_normalizes_windows_separators(tmp_path: Path):
    ignore = tmp_path / ".claude-ignore"
    ignore.write_text("docs/draft/**\n", encoding="utf-8")
    matcher = IgnoreMatcher.load(ignore, repo_root=tmp_path)
    assert matcher.matches("docs\\draft\\notes.md")
