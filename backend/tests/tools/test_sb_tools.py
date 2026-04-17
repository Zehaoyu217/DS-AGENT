"""Tests for Second Brain tool handlers with graceful-degradation contract."""
from __future__ import annotations

import importlib
import sqlite3
from pathlib import Path


def _point_at_home(monkeypatch, home: Path, enabled: bool) -> None:
    if enabled:
        (home / ".sb").mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("SECOND_BRAIN_HOME", str(home))
    from app import config
    importlib.reload(config)


def test_sb_search_no_op_when_disabled(monkeypatch, tmp_path):
    _point_at_home(monkeypatch, tmp_path / "sb", enabled=False)
    from app.tools import sb_tools
    importlib.reload(sb_tools)
    res = sb_tools.sb_search({"query": "x"})
    assert res == {"ok": False, "error": "second_brain_disabled", "hits": []}


def test_sb_search_returns_hits_when_enabled(monkeypatch, tmp_path):
    home = tmp_path / "sb"
    (home / ".sb").mkdir(parents=True)
    # Minimal FTS5 index so BM25Retriever can respond.
    db = sqlite3.connect(home / ".sb" / "kb.sqlite")
    db.executescript(
        """
        CREATE VIRTUAL TABLE claim_fts USING fts5(
            claim_id UNINDEXED, statement, abstract, body, taxonomy,
            tokenize='unicode61 remove_diacritics 2'
        );
        CREATE VIRTUAL TABLE source_fts USING fts5(
            source_id UNINDEXED, title, abstract, processed_body, taxonomy,
            tokenize='unicode61 remove_diacritics 2'
        );
        INSERT INTO claim_fts(claim_id, statement, abstract, body, taxonomy)
        VALUES ('clm_x', 'attention alone suffices', 'attention', 'body', 'papers/ml');
        """
    )
    db.commit()
    db.close()
    _point_at_home(monkeypatch, home, enabled=True)

    from app.tools import sb_tools
    importlib.reload(sb_tools)
    res = sb_tools.sb_search({"query": "attention", "k": 3, "scope": "claims"})
    assert res["ok"] is True
    assert any(h["id"] == "clm_x" for h in res["hits"])


def test_sb_load_unknown_id_returns_error(monkeypatch, tmp_path):
    home = tmp_path / "sb"
    (home / ".sb").mkdir(parents=True)
    _point_at_home(monkeypatch, home, enabled=True)
    from app.tools import sb_tools
    importlib.reload(sb_tools)
    res = sb_tools.sb_load({"node_id": "clm_doesnt_exist"})
    assert res["ok"] is False


def test_sb_ingest_rejects_path_when_disabled(monkeypatch, tmp_path):
    _point_at_home(monkeypatch, tmp_path / "sb", enabled=False)
    from app.tools import sb_tools
    importlib.reload(sb_tools)
    res = sb_tools.sb_ingest({"path": str(tmp_path / "doc.md")})
    assert res == {"ok": False, "error": "second_brain_disabled"}
