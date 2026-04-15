"""Tests for the in-session todo store (P19)."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.harness.todo_store import TodoItem, TodoStore, get_todo_store
from app.main import create_app


def _items(*entries: tuple[str, str, str]) -> list[dict]:
    return [{"id": i, "content": c, "status": s} for i, c, s in entries]


def test_store_empty_by_default() -> None:
    store = TodoStore()
    assert store.list("s1") == ()


def test_store_replace_stores_all() -> None:
    store = TodoStore()
    out = store.replace(
        "s1",
        _items(("t1", "Do the thing", "pending"), ("t2", "Then do next", "pending")),
    )
    assert len(out) == 2
    assert out[0] == TodoItem(id="t1", content="Do the thing", status="pending")
    assert out[1].status == "pending"
    assert store.list("s1") == out


def test_store_replace_overwrites_previous() -> None:
    store = TodoStore()
    store.replace("s1", _items(("a", "first", "pending")))
    store.replace("s1", _items(("b", "second", "in_progress")))
    listed = store.list("s1")
    assert len(listed) == 1
    assert listed[0].id == "b"
    assert listed[0].status == "in_progress"


def test_store_scoped_per_session() -> None:
    store = TodoStore()
    store.replace("s1", _items(("a", "x", "pending")))
    store.replace("s2", _items(("b", "y", "pending")))
    assert store.list("s1")[0].id == "a"
    assert store.list("s2")[0].id == "b"


def test_store_validates_status() -> None:
    store = TodoStore()
    with pytest.raises(ValueError, match="invalid status"):
        store.replace("s1", _items(("t1", "do", "not-a-status")))


def test_store_rejects_blank_id_or_content() -> None:
    store = TodoStore()
    with pytest.raises(ValueError, match="non-empty 'id'"):
        store.replace("s1", _items(("", "x", "pending")))
    with pytest.raises(ValueError, match="non-empty 'content'"):
        store.replace("s1", _items(("t1", "", "pending")))


def test_store_clear_removes_session() -> None:
    store = TodoStore()
    store.replace("s1", _items(("a", "x", "pending")))
    store.clear("s1")
    assert store.list("s1") == ()


def test_singleton_is_stable() -> None:
    a = get_todo_store()
    b = get_todo_store()
    assert a is b


def test_todo_read_endpoint_returns_empty_initially() -> None:
    get_todo_store().reset_for_tests()
    with TestClient(create_app()) as client:
        r = client.get("/api/todos/nonexistent")
        assert r.status_code == 200
        data = r.json()
        assert data["session_id"] == "nonexistent"
        assert data["count"] == 0
        assert data["todos"] == []


def test_todo_read_endpoint_returns_stored_items() -> None:
    store = get_todo_store()
    store.reset_for_tests()
    store.replace(
        "sess-xyz",
        _items(
            ("1", "Load dataset", "completed"),
            ("2", "Run correlation", "in_progress"),
            ("3", "Validate finding", "pending"),
        ),
    )
    with TestClient(create_app()) as client:
        r = client.get("/api/todos/sess-xyz")
        assert r.status_code == 200
        data = r.json()
        assert data["count"] == 3
        ids = [t["id"] for t in data["todos"]]
        assert ids == ["1", "2", "3"]
        assert data["todos"][1]["status"] == "in_progress"
