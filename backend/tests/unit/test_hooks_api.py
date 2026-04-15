"""Smoke test for GET /api/hooks."""
from __future__ import annotations

from fastapi.testclient import TestClient
from app.main import create_app


def test_get_hooks_returns_200():
    client = TestClient(create_app())
    resp = client.get("/api/hooks")
    assert resp.status_code == 200
    data = resp.json()
    assert "hooks" in data
    assert "loaded" in data
