"""Per-bucket autonomy config and graduation readiness check."""
from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict

from app.sop.log import list_entries

MIN_SESSIONS = 5
MIN_SUCCESS_RATE = 0.80
MIN_DISTINCT_RUNGS = 3


class AutonomyConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    autonomous_buckets: list[str] = []


def load_autonomy_config(path: Path) -> AutonomyConfig:
    if not path.exists():
        return AutonomyConfig()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return AutonomyConfig.model_validate(data)


def _save(config: AutonomyConfig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(config.model_dump(), sort_keys=False))


def mark_autonomous(bucket: str, path: Path) -> None:
    cfg = load_autonomy_config(path)
    if bucket in cfg.autonomous_buckets:
        return
    _save(AutonomyConfig(autonomous_buckets=[*cfg.autonomous_buckets, bucket]), path)


def revert_to_proposed(bucket: str, path: Path) -> None:
    cfg = load_autonomy_config(path)
    remaining = [b for b in cfg.autonomous_buckets if b != bucket]
    _save(AutonomyConfig(autonomous_buckets=remaining), path)


def evaluate_graduation_readiness(bucket: str, log_dir: Path) -> bool:
    """True iff bucket meets all graduation criteria."""
    entries = [
        e for e in list_entries(log_dir)
        if e.triage is not None and e.triage.bucket == bucket
    ]
    if len(entries) < MIN_SESSIONS:
        return False
    success_rate = sum(1 for e in entries if e.outcome.get("success")) / len(entries)
    if success_rate < MIN_SUCCESS_RATE:
        return False
    distinct_rungs = {e.fix.ladder_id for e in entries if e.fix is not None}
    return len(distinct_rungs) >= MIN_DISTINCT_RUNGS
