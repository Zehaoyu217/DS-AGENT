"""``hooks.broken`` — WARN when a configured hook exits non-zero in dry-run."""
from __future__ import annotations

from datetime import date
from typing import Any

from ....issue import IntegrityIssue
from ....protocol import ScanContext
from ..coverage import CoverageDoc
from ..dry_run import run_for
from ..matching import matches
from ..settings_parser import HookRecord


def run(
    ctx: ScanContext,
    cfg: dict[str, Any],
    today: date,
) -> list[IntegrityIssue]:
    coverage: CoverageDoc = cfg["_coverage"]
    hooks: list[HookRecord] = cfg["_hooks"]
    timeout: int = int(cfg.get("_dry_run_timeout", 10))
    fixtures_dir = cfg["_fixtures_dir"]

    issues: list[IntegrityIssue] = []
    for rule in coverage.rules:
        matched = [h for h in hooks if matches(rule, h)]
        if not matched:
            continue
        hook = matched[0]
        result = run_for(rule, hook, ctx.repo_root, timeout, fixtures_dir)
        if result.timed_out:
            message = (
                f"Hook for rule '{rule.id}' timed out after {timeout}s: "
                f"{hook.command[:80]!r}"
            )
        elif result.exit_code == 0:
            continue
        else:
            message = (
                f"Hook for rule '{rule.id}' exited {result.exit_code}: "
                f"{hook.command[:80]!r}"
            )
        issues.append(IntegrityIssue(
            rule="hooks.broken",
            severity="WARN",
            node_id=rule.id,
            location=(
                f"{rule.id}@.claude/settings.json#"
                f"{':'.join(str(i) for i in hook.source_index)}"
            ),
            message=message,
            evidence={
                "command": hook.command,
                "exit_code": result.exit_code,
                "stderr_tail": result.stderr[-1024:],
                "duration_ms": result.duration_ms,
                "timed_out": result.timed_out,
            },
            fix_class=None,
        ))
    return issues
