"""Fixer: remove dead linter-suppression directives.

Only strips directives whose rule code is in the configured `known_codes`
allowlist. MVP supports two strategies:
  - Python ruff: `# noqa: <code>` (in-line trailing comment)
  - TypeScript ESLint: `// eslint-disable-next-line <rule>` (own line above)

Block-form `eslint-disable` permanently out of scope (too risky to strip without
parsing scope).
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from ..diff import Diff, IssueRef
from ..loader import SiblingArtifacts

DEFAULT_KNOWN_CODES = (
    "F401", "F811", "E501", "E731",  # ruff/flake8
    "react/no-unused-vars", "@typescript-eslint/no-unused-vars",
)

NOQA_TRAILING_RE = re.compile(r"\s*#\s*noqa(?::\s*[A-Z0-9, ]+)?\s*$")
ESLINT_DISABLE_LINE_RE = re.compile(r"^\s*//\s*eslint-disable-next-line\b.*$")


def _strip_python_noqa(line: str) -> str:
    return NOQA_TRAILING_RE.sub("", line)


def _is_eslint_disable_line(line: str) -> bool:
    return bool(ESLINT_DISABLE_LINE_RE.match(line))


def propose(
    artifacts: SiblingArtifacts,
    repo_root: Path,
    config: dict[str, Any],
) -> list[Diff]:
    if not artifacts.graph_lint:
        return []
    known = set(config.get("known_codes", DEFAULT_KNOWN_CODES))

    by_file: dict[str, list[dict[str, Any]]] = defaultdict(list)
    refs_by_file: dict[str, list[IssueRef]] = defaultdict(list)

    for issue in artifacts.graph_lint.get("issues", []):
        ev = issue.get("evidence", {})
        if "directive_kind" not in ev or "rule_code" not in ev:
            continue
        if ev["rule_code"] not in known:
            continue
        path = ev.get("path")
        if not path:
            continue
        by_file[path].append(ev)
        refs_by_file[path].append(IssueRef(
            plugin="graph_lint",
            rule=str(issue.get("rule", "")),
            message=str(issue.get("message", "")),
            evidence=dict(ev),
        ))

    diffs: list[Diff] = []
    for rel_path, evs in sorted(by_file.items()):
        target = repo_root / rel_path
        if not target.exists():
            continue
        original = target.read_text()
        lines = original.splitlines(keepends=True)

        lines_to_drop: set[int] = set()
        line_rewrites: dict[int, str] = {}

        for ev in evs:
            kind = ev.get("directive_kind")
            line_no = int(ev.get("line", 0)) - 1
            if line_no < 0 or line_no >= len(lines):
                continue
            line = lines[line_no]
            if kind == "noqa":
                rewritten = _strip_python_noqa(line.rstrip("\n"))
                if line.endswith("\n"):
                    rewritten += "\n"
                if rewritten.strip() == "" and line.strip() != "":
                    lines_to_drop.add(line_no)
                else:
                    line_rewrites[line_no] = rewritten
            elif kind == "eslint-disable-next-line":
                if _is_eslint_disable_line(line):
                    lines_to_drop.add(line_no)

        if not lines_to_drop and not line_rewrites:
            continue

        new_lines: list[str] = []
        for idx, line in enumerate(lines):
            if idx in lines_to_drop:
                continue
            new_lines.append(line_rewrites.get(idx, line))
        new_content = "".join(new_lines)
        if new_content == original:
            continue
        diffs.append(Diff(
            path=Path(rel_path),
            original_content=original,
            new_content=new_content,
            rationale=f"Strip {len(evs)} dead lint directive(s) from {rel_path}",
            source_issues=tuple(refs_by_file[rel_path]),
        ))

    return diffs
