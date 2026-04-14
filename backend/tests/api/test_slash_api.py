from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def test_list_slash_commands(client: TestClient) -> None:
    r = client.get("/api/slash")
    assert r.status_code == 200
    body = r.json()
    ids = [cmd["id"] for cmd in body]
    assert ids == ["help", "clear", "new", "settings"]
    for cmd in body:
        assert set(cmd.keys()) == {"id", "label", "description"}
        assert cmd["label"].startswith("/")
        assert cmd["description"]


def test_execute_known_command(client: TestClient) -> None:
    r = client.post("/api/slash/execute", json={"command_id": "help", "args": {}})
    assert r.status_code == 200
    assert r.json() == {"ok": True, "message": "Executed help"}


def test_execute_accepts_optional_fields(client: TestClient) -> None:
    r = client.post(
        "/api/slash/execute",
        json={"command_id": "clear", "conversation_id": "abc-123", "args": {"quiet": True}},
    )
    assert r.status_code == 200
    assert r.json()["ok"] is True


def test_execute_unknown_returns_404(client: TestClient) -> None:
    r = client.post("/api/slash/execute", json={"command_id": "launch-nukes"})
    assert r.status_code == 404


def test_execute_missing_command_id_returns_422(client: TestClient) -> None:
    r = client.post("/api/slash/execute", json={})
    assert r.status_code == 422
