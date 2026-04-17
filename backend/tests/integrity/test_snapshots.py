import json
from datetime import date, timedelta
from pathlib import Path

import pytest
from backend.app.integrity.snapshots import (
    load_snapshot_by_age,
    prune_older_than,
    snapshot_path,
    write_snapshot,
)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    return tmp_path


def test_write_creates_dated_file(repo: Path):
    payload = {"nodes": [{"id": "a"}], "links": []}
    out = write_snapshot(repo, payload, today=date(2026, 4, 17))
    assert out == repo / "integrity-out" / "snapshots" / "2026-04-17.json"
    assert json.loads(out.read_text()) == payload


def test_write_is_atomic(repo: Path, monkeypatch):
    payload = {"nodes": [], "links": []}
    p = write_snapshot(repo, payload, today=date(2026, 4, 17))
    # No partial / temp files should remain alongside the final file
    siblings = list(p.parent.iterdir())
    assert siblings == [p]


def test_load_by_age_returns_correct_snapshot(repo: Path):
    write_snapshot(repo, {"nodes": [{"id": "yesterday"}], "links": []}, today=date(2026, 4, 16))
    write_snapshot(repo, {"nodes": [{"id": "weekago"}], "links": []}, today=date(2026, 4, 10))
    today = date(2026, 4, 17)
    yest = load_snapshot_by_age(repo, days=1, today=today)
    week = load_snapshot_by_age(repo, days=7, today=today)
    assert yest is not None and yest["nodes"][0]["id"] == "yesterday"
    assert week is not None and week["nodes"][0]["id"] == "weekago"


def test_load_by_age_returns_none_when_missing(repo: Path):
    today = date(2026, 4, 17)
    assert load_snapshot_by_age(repo, days=1, today=today) is None


def test_prune_removes_older_than_n_days(repo: Path):
    today = date(2026, 4, 17)
    for i in range(0, 35, 5):
        write_snapshot(repo, {"nodes": [], "links": []}, today=today - timedelta(days=i))
    removed = prune_older_than(repo, days=30, today=today)
    assert removed == 1  # only the 35-day-old one
    remaining = sorted(p.name for p in (repo / "integrity-out" / "snapshots").iterdir())
    assert "2026-03-13.json" not in remaining


def test_snapshot_path_uses_iso_date(repo: Path):
    p = snapshot_path(repo, date(2026, 4, 17))
    assert p.name == "2026-04-17.json"
