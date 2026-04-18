"""Second-Brain digest tool handlers.

Each function returns a JSON-serializable dict. When the KB is disabled,
each handler returns ``{"ok": False, "error": "second_brain_disabled"}``.
"""
from __future__ import annotations

import json
from datetime import date as date_t
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app import config


def _disabled(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {"ok": False, "error": "second_brain_disabled"}
    if extra:
        out.update(extra)
    return out


def _cfg():  # noqa: ANN202
    from second_brain.config import Config

    return Config.load()


def _parse_date(raw: str | None) -> date_t:
    if not raw:
        return date_t.today()
    return datetime.strptime(raw, "%Y-%m-%d").date()


def _entries_for(cfg, day: date_t) -> list[dict[str, Any]]:
    sidecar = cfg.digests_dir / f"{day.isoformat()}.actions.jsonl"
    if not sidecar.exists():
        return []
    out: list[dict[str, Any]] = []
    for ln in sidecar.read_text().splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError:
            continue
    return out


def _applied_ids(cfg, day: date_t) -> set[str]:
    path = cfg.digests_dir / f"{day.isoformat()}.applied.jsonl"
    if not path.exists():
        return set()
    ids: set[str] = set()
    for ln in path.read_text().splitlines():
        try:
            ids.add(json.loads(ln).get("id", ""))
        except json.JSONDecodeError:
            continue
    ids.discard("")
    return ids


def _shape_entries(entries: list[dict[str, Any]], applied: set[str]) -> list[dict[str, Any]]:
    return [
        {
            "id": e.get("id", ""),
            "section": e.get("section", ""),
            "line": e.get("action", {}).get("rationale")
            or e.get("action", {}).get("action", ""),
            "action": e.get("action", {}).get("action", ""),
            "applied": e.get("id") in applied,
        }
        for e in entries
    ]


def sb_digest_today(_args: dict[str, Any]) -> dict[str, Any]:
    if not config.SECOND_BRAIN_ENABLED:
        return _disabled()
    cfg = _cfg()
    today = date_t.today()
    entries = _entries_for(cfg, today)
    applied = _applied_ids(cfg, today)
    shaped = _shape_entries(entries, applied)
    unread = sum(1 for s in shaped if not s["applied"])
    return {
        "ok": True,
        "date": today.isoformat(),
        "entry_count": len(shaped),
        "unread": unread,
        "entries": shaped,
    }
