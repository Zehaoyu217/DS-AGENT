"""REST endpoints for DevTools SOP views."""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from app.api.trace_api import (
    get_judge_variance as _get_judge_variance,
)
from app.api.trace_api import (
    get_prompt_assembly as _get_prompt_assembly,
)
from app.api.trace_api import (
    get_timeline as _get_timeline,
)
from app.sop.ladder_loader import load_all_ladders
from app.sop.log import list_entries, read_entry

router = APIRouter(prefix="/api/sop", tags=["sop"])

_SESSION_ID_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def _log_dir() -> Path:
    return Path(os.environ.get("SOP_LOG_DIR", "docs/superpowers/sop-log"))


@router.get("/sessions")
def list_sessions() -> dict[str, Any]:
    try:
        return {"sessions": [e.model_dump() for e in list_entries(_log_dir())]}
    except (ValueError, ValidationError) as exc:
        raise HTTPException(status_code=500, detail="Failed to load sessions") from exc


@router.get("/sessions/{session_id}")
def get_session(session_id: str) -> dict[str, Any]:
    if not _SESSION_ID_RE.match(session_id):
        raise HTTPException(status_code=400, detail="invalid session_id")
    try:
        entry = read_entry(session_id, _log_dir())
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return entry.model_dump()


@router.get("/ladders")
def list_ladders() -> dict[str, Any]:
    try:
        return {"ladders": [ld.model_dump() for ld in load_all_ladders()]}
    except (ValueError, ValidationError) as exc:
        raise HTTPException(status_code=500, detail="Failed to load ladders") from exc


@router.get("/judge-variance/{trace_id}")
def judge_variance(trace_id: str, n: int = 5) -> dict[str, object]:
    return _get_judge_variance(trace_id=trace_id, refresh=0, n=n)


@router.get("/prompt-assembly/{trace_id}/{step_id}")
def prompt_assembly(trace_id: str, step_id: str) -> dict[str, object]:
    try:
        return _get_prompt_assembly(trace_id=trace_id, step_id=step_id)
    except HTTPException as exc:
        if exc.status_code == 404:
            return {"sections": [], "conflicts": []}
        raise


@router.get("/timeline/{trace_id}")
def timeline(trace_id: str) -> dict[str, object]:
    return _get_timeline(trace_id=trace_id)
