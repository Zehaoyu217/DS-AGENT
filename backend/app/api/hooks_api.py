"""Read-only endpoint to inspect the current hook configuration (P23).

POST/PUT for editing hooks is out of scope — edit hooks.json directly.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import APIRouter

router = APIRouter(prefix="/api/hooks", tags=["hooks"])

_DEFAULT_CONFIG = Path(__file__).resolve().parents[3] / "config" / "hooks.json"


@router.get("")
def get_hooks() -> dict:
    """Return the current hook configuration."""
    path = Path(os.environ.get("CCAGENT_HOOKS_PATH", str(_DEFAULT_CONFIG)))
    if not path.exists():
        return {"hooks": {}, "config_path": str(path), "loaded": False}
    try:
        config = json.loads(path.read_text(encoding="utf-8"))
        return {"hooks": config, "config_path": str(path), "loaded": True}
    except Exception as exc:
        return {"hooks": {}, "config_path": str(path), "loaded": False, "error": str(exc)}
