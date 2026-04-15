"""REST endpoints for user settings.

Storage layout: a single `data/settings.json` file (base overridable via
`DATA_DIR`). PUT replaces the whole document. Single-process assumption.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from app.storage.json_store import JsonStoreError, read_json, write_json_atomic

router = APIRouter(prefix="/api/settings", tags=["settings"])


class UserSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    theme: Literal["light", "dark", "system"] = "system"
    model: str = "claude-sonnet-4-6"
    send_on_enter: bool = True
    # Keep the schema small. The frontend can extend later.


def _data_dir() -> Path:
    return Path(os.environ.get("DATA_DIR", "data"))


def _settings_path() -> Path:
    return _data_dir() / "settings.json"


@router.get("")
def get_settings() -> UserSettings:
    path = _settings_path()
    try:
        return read_json(path, UserSettings, default=UserSettings())
    except JsonStoreError as exc:
        raise HTTPException(status_code=500, detail="failed to load settings") from exc


@router.put("")
def put_settings(payload: UserSettings) -> UserSettings:
    write_json_atomic(_settings_path(), payload)
    return payload
