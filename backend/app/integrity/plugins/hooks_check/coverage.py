"""Coverage doc parser — `config/hooks_coverage.yaml`.

Top-level shape::

    rules:
      - id: <unique slug>
        description: <human-readable>
        when:
          paths: [<glob>, ...]
        requires_hook:
          event: <PreToolUse | PostToolUse | Stop | UserPromptSubmit | ...>
          matcher: <Claude Code matcher string, pipe-joined>
          command_substring: <substring required to be in the hook command>
    tolerated:
      - <command substring excluded from hooks.unused>

All fields are required. Validation errors raise ``ValueError`` with the
offending rule id (or ``<root>``) prefixed.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class RequiredHook:
    event: str
    matcher: str
    command_substring: str


@dataclass(frozen=True)
class CoverageWhen:
    paths: tuple[str, ...]


@dataclass(frozen=True)
class CoverageRule:
    id: str
    description: str
    when: CoverageWhen
    requires_hook: RequiredHook


@dataclass(frozen=True)
class CoverageDoc:
    rules: tuple[CoverageRule, ...]
    tolerated: tuple[str, ...]


def load_coverage(path: Path) -> CoverageDoc:
    """Load + validate ``config/hooks_coverage.yaml``.

    Raises:
        FileNotFoundError: if ``path`` does not exist.
        ValueError: on shape violations (path-prefixed message).
    """
    if not path.exists():
        raise FileNotFoundError(path)
    raw = yaml.safe_load(path.read_text()) or {}
    if not isinstance(raw, dict):
        raise ValueError("<root>: top-level must be a mapping")

    raw_rules = raw.get("rules")
    if not isinstance(raw_rules, list) or not raw_rules:
        raise ValueError("<root>: must define at least one rule under 'rules:'")

    seen_ids: set[str] = set()
    rules: list[CoverageRule] = []
    for idx, raw_rule in enumerate(raw_rules):
        rule = _parse_rule(raw_rule, idx)
        if rule.id in seen_ids:
            raise ValueError(f"<root>: duplicate rule id {rule.id!r}")
        seen_ids.add(rule.id)
        rules.append(rule)

    raw_tolerated = raw.get("tolerated", []) or []
    if not isinstance(raw_tolerated, list):
        raise ValueError("<root>.tolerated: must be a list")
    tolerated = tuple(str(t) for t in raw_tolerated)

    return CoverageDoc(rules=tuple(rules), tolerated=tolerated)


def _parse_rule(raw: object, idx: int) -> CoverageRule:
    if not isinstance(raw, dict):
        raise ValueError(f"rules[{idx}]: must be a mapping")

    rid = raw.get("id")
    if not isinstance(rid, str) or not rid:
        raise ValueError(f"rules[{idx}].id: required string")

    description = raw.get("description")
    if not isinstance(description, str):
        raise ValueError(f"rules[{rid}].description: required string")

    when_raw = raw.get("when")
    if not isinstance(when_raw, dict):
        raise ValueError(f"rules[{rid}].when: required mapping")
    paths_raw = when_raw.get("paths")
    if not isinstance(paths_raw, list) or not paths_raw:
        raise ValueError(f"rules[{rid}].when.paths: non-empty list required")
    paths = tuple(str(p) for p in paths_raw)

    rh_raw = raw.get("requires_hook")
    if not isinstance(rh_raw, dict):
        raise ValueError(f"rules[{rid}].requires_hook: required mapping")
    for field in ("event", "matcher", "command_substring"):
        if field not in rh_raw:
            raise ValueError(
                f"rules[{rid}].requires_hook.{field}: required field"
            )
    requires_hook = RequiredHook(
        event=str(rh_raw["event"]),
        matcher=str(rh_raw["matcher"]),
        command_substring=str(rh_raw["command_substring"]),
    )

    return CoverageRule(
        id=rid,
        description=description,
        when=CoverageWhen(paths=paths),
        requires_hook=requires_hook,
    )
