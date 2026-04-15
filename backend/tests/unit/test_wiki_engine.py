from __future__ import annotations

from pathlib import Path

import pytest

from app.wiki.engine import WikiEngine
from app.wiki.schema import Finding


@pytest.fixture
def wiki(tmp_path: Path) -> WikiEngine:
    for sub in ("findings", "hypotheses", "entities", "meta"):
        (tmp_path / sub).mkdir()
    (tmp_path / "working.md").write_text("# Working\n\n## Current Focus\n\ninitial\n")
    (tmp_path / "index.md").write_text("# Wiki Index\n\n")
    (tmp_path / "log.md").write_text("# Log\n\n")
    return WikiEngine(tmp_path)


def test_read_working_returns_file_contents(wiki: WikiEngine) -> None:
    text = wiki.read_working()
    assert "initial" in text


def test_write_working_replaces_contents(wiki: WikiEngine) -> None:
    wiki.write_working("# Working\n\n## Current Focus\n\nanalyzing customers\n")
    assert "analyzing customers" in wiki.read_working()


def test_write_working_rejects_over_200_lines(wiki: WikiEngine) -> None:
    too_long = "\n".join(f"line {i}" for i in range(250))
    with pytest.raises(ValueError, match="200"):
        wiki.write_working(too_long)


def test_append_log_adds_timestamped_line(wiki: WikiEngine) -> None:
    wiki.append_log("turn 1: profiled customers_v1")
    text = (wiki.root / "log.md").read_text()
    assert "turn 1: profiled customers_v1" in text


def test_promote_finding_writes_markdown(wiki: WikiEngine) -> None:
    finding = Finding(
        id="F-20260412-001",
        title="Revenue grew 12% QoQ",
        body="Analysis shows ...",
        evidence=["art_ab12cd"],
        stat_validate_pass=True,
    )
    path = wiki.promote_finding(finding)
    assert path.exists()
    assert path.name == "F-20260412-001.md"
    assert "Revenue grew 12% QoQ" in path.read_text()


def test_promote_finding_refuses_without_evidence(wiki: WikiEngine) -> None:
    bad = Finding(id="F-X", title="t", body="b", evidence=[], stat_validate_pass=True)
    with pytest.raises(ValueError, match="evidence"):
        wiki.promote_finding(bad)


def test_promote_finding_refuses_without_stat_validate_pass(wiki: WikiEngine) -> None:
    bad = Finding(id="F-X", title="t", body="b", evidence=["art1"], stat_validate_pass=False)
    with pytest.raises(ValueError, match="stat_validate"):
        wiki.promote_finding(bad)


def test_rebuild_index_lists_all_pages(wiki: WikiEngine) -> None:
    wiki.promote_finding(
        Finding(id="F-X", title="First", body="b", evidence=["a"], stat_validate_pass=True)
    )
    (wiki.root / "entities" / "customers.md").write_text("# customers\n\nentity notes\n")

    wiki.rebuild_index()
    text = (wiki.root / "index.md").read_text()
    assert "F-X" in text
    assert "First" in text
    assert "customers" in text
