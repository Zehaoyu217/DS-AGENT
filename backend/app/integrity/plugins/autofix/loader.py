"""Sibling artifact loader for Plugin F.

Reads `integrity-out/{date}/{plugin}.json` files emitted by Plugins B/C/E and
the aggregate `report.json`. Missing files → recorded in `failures` (Plugin F
will mark dependent fix classes as skipped). Parse errors → recorded in
`failures` with prefix `parse_error: ...` (Plugin F emits ERROR severity).

Never raises on missing artifacts. Plugin F survives partial sibling failures.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

ARTIFACT_NAMES = {
    "doc_audit": "doc_audit.json",
    "config_registry": "config_registry.json",
    "graph_lint": "graph_lint.json",
    "aggregate": "report.json",
}


@dataclass(frozen=True)
class SiblingArtifacts:
    doc_audit: dict[str, Any] | None
    config_registry: dict[str, Any] | None
    graph_lint: dict[str, Any] | None
    aggregate: dict[str, Any] | None
    failures: dict[str, str]


def read_today(integrity_out: Path, today: date) -> SiblingArtifacts:
    """Load today's sibling artifacts.

    integrity_out: the `integrity-out/` root (containing date subdirectories).
    today: which date subdirectory to read.
    """
    run_dir = integrity_out / today.isoformat()
    loaded: dict[str, dict[str, Any] | None] = {}
    failures: dict[str, str] = {}

    for key, fname in ARTIFACT_NAMES.items():
        path = run_dir / fname
        if not path.exists():
            loaded[key] = None
            failures[key] = "missing"
            continue
        try:
            loaded[key] = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError) as exc:
            loaded[key] = None
            failures[key] = f"parse_error: {type(exc).__name__}: {exc}"

    return SiblingArtifacts(
        doc_audit=loaded["doc_audit"],
        config_registry=loaded["config_registry"],
        graph_lint=loaded["graph_lint"],
        aggregate=loaded["aggregate"],
        failures=failures,
    )
