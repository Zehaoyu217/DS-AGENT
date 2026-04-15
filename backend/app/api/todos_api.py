"""Todo list read endpoint (P19).

The agent writes todos via the ``todo_write`` tool; the frontend reads them
via this endpoint to show a live task panel in the DevTools middle tab.
"""
from __future__ import annotations

from fastapi import APIRouter

from app.harness.todo_store import get_todo_store

router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.get("/{session_id}")
def read_session_todos(session_id: str) -> dict:
    store = get_todo_store()
    items = store.list(session_id)
    return {
        "session_id": session_id,
        "count": len(items),
        "todos": [t.to_dict() for t in items],
    }
