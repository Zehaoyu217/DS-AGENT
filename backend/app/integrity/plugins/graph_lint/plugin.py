from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date
from typing import Any

from ...issue import IntegrityIssue
from ...protocol import ScanContext, ScanResult

# Rule signature: ctx, plugin_config, today -> list[IntegrityIssue]
Rule = Callable[[ScanContext, dict[str, Any], date], list[IntegrityIssue]]


def _default_rules() -> dict[str, Rule]:
    # Imported lazily so subagents can build the plugin shell before all rules exist.
    from .rules import dead_code, density_drop, drift, handler_unbound, orphan_growth

    return {
        "graph.dead_code": dead_code.run,
        "graph.drift_added": drift.run_added,
        "graph.drift_removed": drift.run_removed,
        "graph.density_drop": density_drop.run,
        "graph.orphan_growth": orphan_growth.run,
        "graph.handler_unbound": handler_unbound.run,
    }


@dataclass
class GraphLintPlugin:
    name: str = "graph_lint"
    version: str = "1.0.0"
    depends_on: tuple[str, ...] = ("graph_extension",)
    paths: tuple[str, ...] = (
        "backend/app/**/*.py",
        "frontend/src/**/*.{ts,tsx,js,jsx}",
        "graphify/graph.json",
        "graphify/graph.augmented.json",
    )
    config: dict[str, Any] = field(default_factory=dict)
    today: date = field(default_factory=date.today)
    rules: dict[str, Rule] | None = None

    def scan(self, ctx: ScanContext) -> ScanResult:
        rules = self.rules if self.rules is not None else _default_rules()
        disabled = set(self.config.get("disabled_rules", []))

        all_issues: list[IntegrityIssue] = []
        rules_run: list[str] = []
        failures: list[str] = []

        for rule_id, fn in rules.items():
            if rule_id in disabled:
                continue
            try:
                issues = fn(ctx, self.config, self.today)
                all_issues.extend(issues)
                rules_run.append(rule_id)
            except Exception as exc:
                failures.append(f"{rule_id}: {type(exc).__name__}: {exc}")
                all_issues.append(
                    IntegrityIssue(
                        rule=rule_id,
                        severity="ERROR",
                        node_id="<rule-failure>",
                        location=f"graph_lint/{rule_id}",
                        message=f"{type(exc).__name__}: {exc}",
                    )
                )

        run_dir = ctx.repo_root / "integrity-out" / self.today.isoformat()
        run_dir.mkdir(parents=True, exist_ok=True)
        artifact = run_dir / "graph_lint.json"
        artifact.write_text(
            json.dumps(
                {
                    "date": self.today.isoformat(),
                    "rules_run": rules_run,
                    "failures": failures,
                    "issues": [i.to_dict() for i in all_issues],
                },
                indent=2,
                sort_keys=True,
            )
        )

        return ScanResult(
            plugin_name=self.name,
            plugin_version=self.version,
            issues=all_issues,
            artifacts=[artifact],
            failures=failures,
        )
