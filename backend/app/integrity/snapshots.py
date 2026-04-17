from __future__ import annotations

import json
import os
import tempfile
from datetime import date, timedelta
from pathlib import Path
from typing import Any


def _snapshots_dir(repo_root: Path) -> Path:
    d = repo_root / "integrity-out" / "snapshots"
    d.mkdir(parents=True, exist_ok=True)
    return d


def snapshot_path(repo_root: Path, day: date) -> Path:
    return _snapshots_dir(repo_root) / f"{day.isoformat()}.json"


def write_snapshot(
    repo_root: Path, payload: dict[str, Any], today: date
) -> Path:
    final = snapshot_path(repo_root, today)
    fd, tmp_path_str = tempfile.mkstemp(
        prefix=".snapshot-", suffix=".json", dir=str(final.parent)
    )
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(payload, f)
        os.replace(tmp_path_str, final)
    except Exception:
        Path(tmp_path_str).unlink(missing_ok=True)
        raise
    return final


def load_snapshot_by_age(
    repo_root: Path, days: int, today: date
) -> dict[str, Any] | None:
    target = today - timedelta(days=days)
    p = snapshot_path(repo_root, target)
    if not p.exists():
        return None
    return json.loads(p.read_text())


def prune_older_than(repo_root: Path, days: int, today: date) -> int:
    cutoff = today - timedelta(days=days)
    removed = 0
    for snap in _snapshots_dir(repo_root).glob("*.json"):
        try:
            day = date.fromisoformat(snap.stem)
        except ValueError:
            continue
        if day <= cutoff:
            snap.unlink()
            removed += 1
    return removed
