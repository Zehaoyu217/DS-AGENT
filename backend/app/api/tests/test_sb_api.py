"""Tests for /api/sb REST routes."""
from __future__ import annotations

from fastapi.testclient import TestClient

from app import config as app_config
from app.api import sb_api


def _client() -> TestClient:
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(sb_api.router)
    return TestClient(app)


# ─────────────────────── gating ─────────────────────────────────────


def test_stats_returns_404_when_disabled(monkeypatch):
    monkeypatch.setattr(app_config, "SECOND_BRAIN_ENABLED", False, raising=False)
    resp = _client().get("/api/sb/stats")
    assert resp.status_code == 404


def test_stats_happy_path(monkeypatch):
    monkeypatch.setattr(app_config, "SECOND_BRAIN_ENABLED", True, raising=False)
    from app.tools import sb_digest_tools

    monkeypatch.setattr(
        sb_digest_tools,
        "sb_stats",
        lambda _args: {
            "ok": True,
            "stats": {"claims": 10},
            "health": {"score": 88, "grade": "B"},
        },
        raising=False,
    )
    resp = _client().get("/api/sb/stats")
    assert resp.status_code == 200
    body = resp.json()
    assert body["ok"] is True
    assert body["stats"] == {"claims": 10}
    assert body["health"]["score"] == 88


# ─────────────────────── pending / build ────────────────────────────


def test_digest_pending_returns_404_when_disabled(monkeypatch):
    monkeypatch.setattr(app_config, "SECOND_BRAIN_ENABLED", False, raising=False)
    resp = _client().get("/api/sb/digest/pending")
    assert resp.status_code == 404


def test_digest_pending_happy_path(monkeypatch):
    monkeypatch.setattr(app_config, "SECOND_BRAIN_ENABLED", True, raising=False)

    class _Entry:
        def __init__(self, id_, section, line, action):
            self.id = id_
            self.section = section
            self.line = line
            self.action = action

    monkeypatch.setattr(
        sb_api,
        "_read_pending",
        lambda _cfg: [
            _Entry(
                "pend_0001",
                "Reconciliation",
                "upgrade clm_foo",
                {"action": "upgrade_confidence", "claim_id": "clm_foo"},
            )
        ],
        raising=False,
    )
    monkeypatch.setattr(sb_api, "_sb_cfg", lambda: object(), raising=False)

    resp = _client().get("/api/sb/digest/pending")
    assert resp.status_code == 200
    body = resp.json()
    assert body["ok"] is True
    assert body["count"] == 1
    assert body["proposals"][0]["id"] == "pend_0001"
    assert body["proposals"][0]["section"] == "Reconciliation"
    assert body["proposals"][0]["line"] == "upgrade clm_foo"
    assert body["proposals"][0]["action"]["action"] == "upgrade_confidence"


def test_digest_build_returns_404_when_disabled(monkeypatch):
    monkeypatch.setattr(app_config, "SECOND_BRAIN_ENABLED", False, raising=False)
    resp = _client().post("/api/sb/digest/build")
    assert resp.status_code == 404


def test_digest_build_emits(monkeypatch):
    monkeypatch.setattr(app_config, "SECOND_BRAIN_ENABLED", True, raising=False)

    class _Result:
        def __init__(self, n):
            self.entries = [object()] * n

    monkeypatch.setattr(sb_api, "_sb_cfg", lambda: object(), raising=False)
    monkeypatch.setattr(sb_api, "_load_habits", lambda _cfg: object(), raising=False)
    monkeypatch.setattr(
        sb_api,
        "_run_build",
        lambda _cfg, _habits: _Result(3),
        raising=False,
    )
    resp = _client().post("/api/sb/digest/build")
    assert resp.status_code == 200
    body = resp.json()
    assert body["ok"] is True
    assert body["emitted"] is True
    assert body["entries"] == 3


def test_digest_build_empty(monkeypatch):
    monkeypatch.setattr(app_config, "SECOND_BRAIN_ENABLED", True, raising=False)

    class _Result:
        entries: list = []

    monkeypatch.setattr(sb_api, "_sb_cfg", lambda: object(), raising=False)
    monkeypatch.setattr(sb_api, "_load_habits", lambda _cfg: object(), raising=False)
    monkeypatch.setattr(
        sb_api,
        "_run_build",
        lambda _cfg, _habits: _Result(),
        raising=False,
    )
    resp = _client().post("/api/sb/digest/build")
    assert resp.status_code == 200
    body = resp.json()
    assert body["ok"] is True
    assert body["emitted"] is False
    assert body["entries"] == 0
