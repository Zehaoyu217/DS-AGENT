"""Tests for second-brain digest tool handlers."""
from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import pytest

from app import config as app_config


@pytest.fixture
def sb_home(tmp_path, monkeypatch):
    home = tmp_path / "sb"
    (home / "digests").mkdir(parents=True)
    (home / "claims").mkdir()
    (home / "sources").mkdir()
    (home / ".sb").mkdir()
    monkeypatch.setenv("SECOND_BRAIN_HOME", str(home))
    monkeypatch.setattr(app_config, "SECOND_BRAIN_ENABLED", True, raising=False)
    return home


def _write_digest(home: Path, today: date, entries: list[dict]) -> None:
    digest_dir = home / "digests"
    md = f"# Digest {today.isoformat()}\n\n"
    for e in entries:
        md += f"## {e['section']}\n- [{e['id']}] {e['line']}\n"
    (digest_dir / f"{today.isoformat()}.md").write_text(md)
    sidecar = digest_dir / f"{today.isoformat()}.actions.jsonl"
    with sidecar.open("w") as f:
        for e in entries:
            f.write(
                json.dumps({"id": e["id"], "section": e["section"], "action": e["action"]})
                + "\n"
            )


# ─────────────────────── sb_digest_today ──────────────────────────


def test_sb_digest_today_happy_path(sb_home):
    from app.tools.sb_digest_tools import sb_digest_today

    today = date.today()
    _write_digest(
        sb_home,
        today,
        [
            {
                "id": "r01",
                "section": "Reconciliation",
                "line": "upgrade clm_foo",
                "action": {
                    "action": "upgrade_confidence",
                    "claim_id": "clm_foo",
                    "from": "low",
                    "to": "medium",
                    "rationale": "x",
                },
            },
        ],
    )
    result = sb_digest_today({})
    assert result["ok"] is True
    assert result["date"] == today.isoformat()
    assert result["entry_count"] == 1
    assert result["unread"] == 1
    assert result["entries"][0]["id"] == "r01"


def test_sb_digest_today_disabled(monkeypatch):
    monkeypatch.setattr(app_config, "SECOND_BRAIN_ENABLED", False, raising=False)
    from app.tools.sb_digest_tools import sb_digest_today

    result = sb_digest_today({})
    assert result == {"ok": False, "error": "second_brain_disabled"}


def test_sb_digest_today_missing(sb_home):
    from app.tools.sb_digest_tools import sb_digest_today

    result = sb_digest_today({})
    assert result["ok"] is True
    assert result["entry_count"] == 0
    assert result["entries"] == []


# ─────────────────────── sb_digest_list / show ─────────────────────


def test_sb_digest_list(sb_home):
    from app.tools.sb_digest_tools import sb_digest_list

    today = date.today()
    yday = today - timedelta(days=1)
    _write_digest(
        sb_home,
        today,
        [{"id": "r01", "section": "Reconciliation", "line": "a", "action": {"action": "keep"}}],
    )
    _write_digest(
        sb_home,
        yday,
        [{"id": "r01", "section": "Taxonomy", "line": "b", "action": {"action": "keep"}}],
    )
    result = sb_digest_list({"limit": 5})
    assert result["ok"] is True
    dates = [d["date"] for d in result["digests"]]
    assert dates == [today.isoformat(), yday.isoformat()]
    assert result["digests"][0]["entry_count"] == 1


def test_sb_digest_show(sb_home):
    from app.tools.sb_digest_tools import sb_digest_show

    today = date.today()
    _write_digest(
        sb_home,
        today,
        [{"id": "r01", "section": "Reconciliation", "line": "x", "action": {"action": "keep"}}],
    )
    result = sb_digest_show({"date": today.isoformat()})
    assert result["ok"] is True
    assert result["date"] == today.isoformat()
    assert "Digest" in result["markdown"]
    assert result["entries"][0]["id"] == "r01"


def test_sb_digest_show_missing(sb_home):
    from app.tools.sb_digest_tools import sb_digest_show

    result = sb_digest_show({"date": "2099-01-01"})
    assert result == {"ok": False, "error": "digest_not_found", "date": "2099-01-01"}
