"""Fixer: append unindexed-doc entries to CLAUDE.md.

Reads `doc.unindexed` issues from doc_audit.json. Bundles all unindexed docs
into one Diff for CLAUDE.md, alphabetically inserted into the configured
target section, dedup-checked.

Pure: no side effects beyond reading repo_root files.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..diff import Diff, IssueRef
from ..loader import SiblingArtifacts

DEFAULT_SECTION = "## Deeper Context"


def _title_for(doc_path: Path, repo_root: Path) -> str:
    full = repo_root / doc_path
    if full.exists():
        for line in full.read_text().splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
    stem = doc_path.stem.replace("_", " ").replace("-", " ")
    return " ".join(w.capitalize() for w in stem.split())


def _already_indexed(claude_md_text: str, doc_path: Path) -> bool:
    return f"]({doc_path.as_posix()})" in claude_md_text


def _insert_in_section(text: str, section_header: str, new_lines: list[str]) -> str:
    lines = text.splitlines(keepends=True)
    in_section = False
    insert_idx: int | None = None
    for idx, line in enumerate(lines):
        if line.rstrip() == section_header:
            in_section = True
            continue
        if in_section and line.startswith("## "):
            insert_idx = idx
            break
    if not in_section:
        suffix = "" if text.endswith("\n") else "\n"
        body = "\n".join(new_lines)
        return f"{text}{suffix}\n{section_header}\n\n{body}\n"
    if insert_idx is None:
        insert_idx = len(lines)
    insert_at = insert_idx
    while insert_at > 0 and lines[insert_at - 1].strip() == "":
        insert_at -= 1
    addition = "".join(line + "\n" for line in new_lines) + "\n"
    return "".join(lines[:insert_at]) + addition + "".join(lines[insert_at:])


def propose(
    artifacts: SiblingArtifacts,
    repo_root: Path,
    config: dict[str, Any],
) -> list[Diff]:
    if not artifacts.doc_audit:
        return []
    issues = [i for i in artifacts.doc_audit.get("issues", [])
              if i.get("rule") == "doc.unindexed"]
    if not issues:
        return []

    claude_md_path = repo_root / "CLAUDE.md"
    if not claude_md_path.exists():
        return []
    original = claude_md_path.read_text()

    section = str(config.get("target_section", DEFAULT_SECTION))

    refs: list[IssueRef] = []
    new_entries: list[tuple[str, str]] = []
    for issue in issues:
        ev = issue.get("evidence", {})
        rel = ev.get("path")
        if not rel:
            continue
        doc = Path(rel)
        if _already_indexed(original, doc):
            continue
        title = _title_for(doc, repo_root)
        new_entries.append((title, doc.as_posix()))
        refs.append(IssueRef(
            plugin="doc_audit",
            rule="doc.unindexed",
            message=str(issue.get("message", "")),
            evidence=dict(ev),
        ))

    if not new_entries:
        return []

    new_entries.sort(key=lambda e: e[0].lower())
    new_lines = [f"- [{t}]({p})" for t, p in new_entries]
    new_content = _insert_in_section(original, section, new_lines)

    if new_content == original:
        return []

    rationale = f"Index {len(new_entries)} unindexed doc(s) under {section}"
    return [Diff(
        path=Path("CLAUDE.md"),
        original_content=original,
        new_content=new_content,
        rationale=rationale,
        source_issues=tuple(refs),
    )]
