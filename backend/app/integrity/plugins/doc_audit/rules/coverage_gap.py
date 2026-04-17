from __future__ import annotations

from datetime import date
from typing import Any

from ....issue import IntegrityIssue
from ....protocol import ScanContext


def run(ctx: ScanContext, cfg: dict[str, Any], today: date) -> list[IntegrityIssue]:
    required: list[str] = list(cfg.get("coverage_required", []))
    issues: list[IntegrityIssue] = []
    for name in required:
        rel = f"docs/{name}"
        if not (ctx.repo_root / rel).is_file():
            issues.append(
                IntegrityIssue(
                    rule="doc.coverage_gap",
                    severity="WARN",
                    node_id=rel,
                    location=rel,
                    message=f"Required doc missing: {rel}",
                    evidence={"expected_path": rel},
                )
            )
    return issues
