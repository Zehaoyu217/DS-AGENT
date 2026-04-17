"""Circuit breaker for Plugin F autofix.

State stored in `config/autofix_state.yaml` (committed). Counters track per-class
clean-merge / human-edited PR outcomes over a rolling window. When `human_edited`
exceeds `max_human_edits` in the window, the class is disabled.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml

from .schemas.autofix_state import validate as validate_state


@dataclass(frozen=True)
class PRRecord:
    pr: int
    merged_at: str  # ISO date
    action: str  # "clean" | "human_edited"


@dataclass(frozen=True)
class ClassState:
    merged_clean: int = 0
    human_edited: int = 0
    pr_history: tuple[PRRecord, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class AutofixState:
    generated_at: str = ""
    generator_version: str = "1.0.0"
    window_days: int = 30
    classes: dict[str, ClassState] = field(default_factory=dict)


def load_state(path: Path) -> AutofixState:
    """Load state from disk. Returns default state if file missing."""
    if not path.exists():
        return AutofixState()
    raw = yaml.safe_load(path.read_text()) or {}
    validate_state(raw)
    classes: dict[str, ClassState] = {}
    for cname, cstate in (raw.get("classes") or {}).items():
        history = tuple(
            PRRecord(pr=int(e["pr"]), merged_at=str(e["merged_at"]), action=str(e["action"]))
            for e in (cstate.get("pr_history") or [])
        )
        classes[cname] = ClassState(
            merged_clean=int(cstate.get("merged_clean", 0)),
            human_edited=int(cstate.get("human_edited", 0)),
            pr_history=history,
        )
    return AutofixState(
        generated_at=str(raw.get("generated_at", "")),
        generator_version=str(raw.get("generator_version", "1.0.0")),
        window_days=int(raw.get("window_days", 30)),
        classes=classes,
    )


def save_state(path: Path, state: AutofixState) -> None:
    payload = {
        "generated_at": state.generated_at,
        "generator_version": state.generator_version,
        "window_days": state.window_days,
        "classes": {
            cname: {
                "merged_clean": cstate.merged_clean,
                "human_edited": cstate.human_edited,
                "pr_history": [
                    {"pr": r.pr, "merged_at": r.merged_at, "action": r.action}
                    for r in cstate.pr_history
                ],
            }
            for cname, cstate in state.classes.items()
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(payload, sort_keys=True))


def disabled_classes(state: AutofixState, max_human_edits: int) -> set[str]:
    return {
        cname for cname, cstate in state.classes.items()
        if cstate.human_edited > max_human_edits
    }


def record_pr_outcome(
    state: AutofixState,
    *,
    fix_class: str,
    pr: int,
    merged_at: str,
    action: str,
    today: date | None = None,
) -> AutofixState:
    """Append a PR outcome and prune entries older than window_days."""
    if action not in {"clean", "human_edited"}:
        raise ValueError(f"action must be clean|human_edited, got {action!r}")
    today = today or date.today()
    cutoff = today - timedelta(days=state.window_days)
    existing = state.classes.get(fix_class, ClassState())
    new_history = list(existing.pr_history) + [
        PRRecord(pr=pr, merged_at=merged_at, action=action)
    ]
    pruned = tuple(
        r for r in new_history
        if datetime.strptime(r.merged_at, "%Y-%m-%d").date() >= cutoff
    )
    merged_clean = sum(1 for r in pruned if r.action == "clean")
    human_edited = sum(1 for r in pruned if r.action == "human_edited")
    new_classes = dict(state.classes)
    new_classes[fix_class] = ClassState(
        merged_clean=merged_clean,
        human_edited=human_edited,
        pr_history=pruned,
    )
    return AutofixState(
        generated_at=state.generated_at,
        generator_version=state.generator_version,
        window_days=state.window_days,
        classes=new_classes,
    )
