"""``config.schema_drift`` — WARN when a config violates its schema validator."""
from __future__ import annotations

from dataclasses import asdict
from datetime import date
from typing import Any

from ....issue import IntegrityIssue
from ....protocol import ScanContext
from ..schemas import SCHEMA_REGISTRY


def run(
    ctx: ScanContext,
    cfg: dict[str, Any],
    today: date,
) -> list[IntegrityIssue]:
    drift_cfg = cfg.get("schema_drift", {})
    if not drift_cfg.get("enabled", True):
        return []
    strict_mode = bool(drift_cfg.get("strict_mode", False))

    current = cfg.get("_current_manifest") or {}
    issues: list[IntegrityIssue] = []

    for entry in current.get("configs", []):
        entry_id = str(entry.get("id"))
        type_name = str(entry.get("type", ""))
        path = ctx.repo_root / str(entry.get("path", ""))

        validator = SCHEMA_REGISTRY.get(type_name)
        if validator is None:
            if strict_mode:
                issues.append(IntegrityIssue(
                    rule="config.schema_drift",
                    severity="WARN",
                    node_id=entry_id,
                    location=f"configs:{entry_id}",
                    message=f"No schema for type '{type_name}' (strict mode)",
                    evidence={"type": type_name},
                ))
            continue

        if not path.exists():
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            issues.append(IntegrityIssue(
                rule="config.schema_drift",
                severity="WARN",
                node_id=entry_id,
                location=f"configs:{entry_id}",
                message=f"Cannot read file: {exc}",
                evidence={"error": str(exc)},
            ))
            continue

        failures = validator.validate(path, content)
        if failures:
            issues.append(IntegrityIssue(
                rule="config.schema_drift",
                severity="WARN",
                node_id=entry_id,
                location=f"configs:{entry_id}",
                message=(
                    f"{len(failures)} schema violation(s) in {entry_id} "
                    f"({type_name})"
                ),
                evidence={
                    "type": type_name,
                    "validation_failures": [asdict(f) for f in failures],
                },
            ))

    return issues
