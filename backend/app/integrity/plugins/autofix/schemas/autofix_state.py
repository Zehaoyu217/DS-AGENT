"""Shape validator for config/autofix_state.yaml."""
from __future__ import annotations

from typing import Any

VALID_ACTIONS = {"clean", "human_edited"}


def validate(payload: dict[str, Any]) -> None:
    """Raise ValueError on shape violations."""
    if not isinstance(payload, dict):
        raise ValueError("autofix_state must be a mapping")
    classes = payload.get("classes", {})
    if not isinstance(classes, dict):
        raise ValueError("autofix_state.classes must be a mapping")
    for cname, cstate in classes.items():
        if not isinstance(cstate, dict):
            raise ValueError(f"autofix_state.classes.{cname} must be a mapping")
        history = cstate.get("pr_history", [])
        if not isinstance(history, list):
            raise ValueError(f"autofix_state.classes.{cname}.pr_history must be a list")
        for i, entry in enumerate(history):
            if not isinstance(entry, dict):
                raise ValueError(
                    f"autofix_state.classes.{cname}.pr_history[{i}] must be a mapping"
                )
            action = entry.get("action")
            if action not in VALID_ACTIONS:
                raise ValueError(
                    f"autofix_state.classes.{cname}.pr_history[{i}].action "
                    f"must be one of {sorted(VALID_ACTIONS)} (got {action!r})"
                )
