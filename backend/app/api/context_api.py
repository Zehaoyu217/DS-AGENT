from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.context.manager import ContextManager, session_registry

router = APIRouter()


# ── Legacy global endpoint (kept for backward compat) ─────────────────────────

_global_ctx = ContextManager()


def get_context_manager() -> ContextManager:
    return _global_ctx


@router.get("/api/context")
async def get_context() -> dict[str, object]:
    return get_context_manager().snapshot()


# ── Per-session endpoints ─────────────────────────────────────────────────────

@router.get("/api/context/sessions")
async def list_sessions() -> dict[str, object]:
    """List all session IDs that have context data."""
    return {"sessions": session_registry.list_sessions()}


@router.get("/api/context/{session_id}")
async def get_session_context(session_id: str) -> dict[str, object]:
    """Current context snapshot for a specific session."""
    mgr = session_registry.get(session_id)
    if mgr is None:
        # Return a zero-state snapshot rather than a 404 so the UI loads cleanly.
        return {
            "session_id": session_id,
            "total_tokens": 0,
            "max_tokens": 200_000,
            "utilization": 0.0,
            "compaction_needed": False,
            "layers": [],
            "compaction_history": [],
        }
    snap = mgr.snapshot()
    return {"session_id": session_id, **snap}


@router.get("/api/context/{session_id}/history")
async def get_session_history(session_id: str) -> dict[str, object]:
    """Compaction history for a specific session."""
    mgr = session_registry.get(session_id)
    if mgr is None:
        return {"session_id": session_id, "history": []}
    return {"session_id": session_id, "history": mgr.compaction_history}


@router.get("/api/context/{session_id}/compaction/{compaction_id}")
async def get_compaction_diff(session_id: str, compaction_id: int) -> dict[str, object]:
    """Detailed diff for a single compaction event."""
    mgr = session_registry.get(session_id)
    if mgr is None:
        raise HTTPException(status_code=404, detail="Session not found")
    history = mgr.compaction_history
    entry = next((e for e in history if e.get("id") == compaction_id), None)
    if entry is None:
        raise HTTPException(status_code=404, detail="Compaction event not found")

    tokens_before: int = entry.get("tokens_before", 0)
    tokens_after: int = entry.get("tokens_after", 0)
    tokens_freed: int = entry.get("tokens_freed", 0)
    loss_pct = (tokens_freed / tokens_before * 100) if tokens_before > 0 else 0.0

    if loss_pct >= 40:
        loss_severity = "HIGH"
    elif loss_pct >= 20:
        loss_severity = "MEDIUM"
    else:
        loss_severity = "LOW"

    return {
        "session_id": session_id,
        "compaction_id": compaction_id,
        "timestamp": entry.get("timestamp"),
        "tokens_before": tokens_before,
        "tokens_after": tokens_after,
        "tokens_freed": tokens_freed,
        "trigger_utilization": entry.get("trigger_utilization", 0.0),
        "information_loss_pct": round(loss_pct, 1),
        "loss_severity": loss_severity,
        "removed": entry.get("removed", []),
        "survived": entry.get("survived", []),
    }
