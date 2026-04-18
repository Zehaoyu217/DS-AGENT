"""Tests for /api/sb/digest/* REST routes."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app import config as app_config


@pytest.fixture
def sb_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    home = tmp_path / "sb"
    (home / "digests").mkdir(parents=True)
    (home / "claims").mkdir()
    (home / "sources").mkdir()
    (home / ".sb").mkdir()
    monkeypatch.setenv("SECOND_BRAIN_HOME", str(home))
    monkeypatch.setattr(app_config, "SECOND_BRAIN_ENABLED", True, raising=False)
    return home


@pytest.fixture
def client() -> TestClient:
    from app.main import create_app

    return TestClient(create_app())


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


def test_digest_today_route_happy_path(sb_home: Path, client: TestClient) -> None:
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
    response = client.get("/api/sb/digest/today")
    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["date"] == today.isoformat()
    assert body["entry_count"] == 1
    assert body["unread"] == 1
    assert body["entries"][0]["id"] == "r01"


def test_digest_today_returns_404_when_disabled(
    monkeypatch: pytest.MonkeyPatch, client: TestClient
) -> None:
    monkeypatch.setattr(app_config, "SECOND_BRAIN_ENABLED", False, raising=False)
    response = client.get("/api/sb/digest/today")
    assert response.status_code == 404


def test_digest_apply_delegates_to_tool(
    sb_home: Path, client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict = {}

    def fake_apply(args: dict) -> dict:
        captured["args"] = args
        return {"ok": True, "applied": args.get("ids", []), "skipped": [], "failed": []}

    from app.api import sb_api

    monkeypatch.setattr(sb_api.sb_digest_tools, "sb_digest_apply", fake_apply)
    response = client.post("/api/sb/digest/apply", json={"ids": ["r01"]})
    assert response.status_code == 200
    assert captured["args"] == {"ids": ["r01"]}
    assert response.json()["applied"] == ["r01"]


def test_digest_apply_returns_404_when_disabled(
    monkeypatch: pytest.MonkeyPatch, client: TestClient
) -> None:
    monkeypatch.setattr(app_config, "SECOND_BRAIN_ENABLED", False, raising=False)
    response = client.post("/api/sb/digest/apply", json={"ids": ["r01"]})
    assert response.status_code == 404


def test_digest_skip_delegates_to_tool(
    sb_home: Path, client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    captured: dict = {}

    def fake_skip(args: dict) -> dict:
        captured["args"] = args
        return {"ok": True, "skipped": True, "signature": "sig_x", "expires_at": "2099-01-01"}

    from app.api import sb_api

    monkeypatch.setattr(sb_api.sb_digest_tools, "sb_digest_skip", fake_skip)
    response = client.post(
        "/api/sb/digest/skip", json={"id": "r01", "ttl_days": 14}
    )
    assert response.status_code == 200
    assert captured["args"] == {"id": "r01", "ttl_days": 14}
    assert response.json()["signature"] == "sig_x"


def test_digest_read_writes_marks(sb_home: Path, client: TestClient) -> None:
    today = date.today().isoformat()
    response = client.post("/api/sb/digest/read", json={"date": today})
    assert response.status_code == 200
    assert response.json() == {"ok": True, "date": today}
    marks_path = sb_home / "digests" / ".read_marks"
    assert marks_path.exists()
    assert today in marks_path.read_text()


def test_digest_read_is_idempotent(sb_home: Path, client: TestClient) -> None:
    today = date.today().isoformat()
    client.post("/api/sb/digest/read", json={"date": today})
    client.post("/api/sb/digest/read", json={"date": today})
    marks_path = sb_home / "digests" / ".read_marks"
    lines = [ln for ln in marks_path.read_text().splitlines() if ln.strip()]
    assert lines.count(today) == 1


def test_digest_read_returns_404_when_disabled(
    monkeypatch: pytest.MonkeyPatch, client: TestClient
) -> None:
    monkeypatch.setattr(app_config, "SECOND_BRAIN_ENABLED", False, raising=False)
    response = client.post("/api/sb/digest/read", json={"date": "2026-04-18"})
    assert response.status_code == 404
