"""``hooks.missing`` — WARN when a coverage rule has no matching hook."""
from __future__ import annotations

from datetime import date
from typing import Any

from ....issue import IntegrityIssue
from ....protocol import ScanContext
from ..coverage import CoverageDoc
from ..matching import matches
from ..settings_parser import HookRecord


def run(
    ctx: ScanContext,
    cfg: dict[str, Any],
    today: date,
) -> list[IntegrityIssue]:
    coverage: CoverageDoc = cfg["_coverage"]
    hooks: list[HookRecord] = cfg["_hooks"]

    issues: list[IntegrityIssue] = []
    for rule in coverage.rules:
        if any(matches(rule, h) for h in hooks):
            continue
        issues.append(IntegrityIssue(
            rule="hooks.missing",
            severity="WARN",
            node_id=rule.id,
            location=rule.id,
            message=(
                f"No hook matches coverage rule '{rule.id}': "
                f"need event={rule.requires_hook.event}, matcher overlapping "
                f"{rule.requires_hook.matcher!r}, command containing "
                f"{rule.requires_hook.command_substring!r}"
            ),
            evidence={
                "rule_paths": list(rule.when.paths),
                "required_event": rule.requires_hook.event,
                "required_matcher": rule.requires_hook.matcher,
                "required_substring": rule.requires_hook.command_substring,
            },
            fix_class=None,
        ))
    return issues
