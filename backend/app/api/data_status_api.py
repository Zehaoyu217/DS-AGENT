"""Data status endpoint — returns active database name and table list."""
from __future__ import annotations

import contextlib
import logging
from pathlib import Path
from typing import Any

import duckdb
from fastapi import APIRouter

from app.config import get_config

router = APIRouter(prefix="/api/data", tags=["data"])
logger = logging.getLogger(__name__)


@router.get("/info")
def data_info() -> dict[str, Any]:
    """Return active database name and table list for the UI status indicator."""
    config = get_config()
    db_path = Path(config.duckdb_path)
    db_name = db_path.name
    tables: list[str] = []

    if db_path.exists():
        with contextlib.suppress(Exception):
            conn = duckdb.connect(str(db_path), read_only=True)
            tables = [t[0] for t in conn.execute("SHOW TABLES").fetchall()]
            conn.close()

    return {"db_name": db_name, "tables": tables}
