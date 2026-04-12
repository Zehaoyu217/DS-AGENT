from __future__ import annotations

import time
from pathlib import Path

from app.wiki.schema import Finding

MAX_WORKING_LINES = 200


class WikiEngine:
    def __init__(self, root: Path) -> None:
        self.root = root

    # ── working.md ──────────────────────────────────────────────────────────

    def read_working(self) -> str:
        return (self.root / "working.md").read_text()

    def write_working(self, content: str) -> None:
        lines = content.splitlines()
        if len(lines) > MAX_WORKING_LINES:
            raise ValueError(
                f"working.md exceeds {MAX_WORKING_LINES} lines ({len(lines)}); compact first"
            )
        (self.root / "working.md").write_text(content)

    # ── log.md ──────────────────────────────────────────────────────────────

    def append_log(self, line: str) -> None:
        stamp = time.strftime("%Y-%m-%dT%H:%M:%S")
        path = self.root / "log.md"
        existing = path.read_text() if path.exists() else "# Log\n\n"
        path.write_text(existing + f"- {stamp} — {line}\n")

    # ── findings ────────────────────────────────────────────────────────────

    def promote_finding(self, finding: Finding) -> Path:
        if not finding.evidence:
            raise ValueError("cannot promote finding without evidence (need artifact IDs)")
        if not finding.stat_validate_pass:
            raise ValueError("cannot promote finding without stat_validate PASS")
        body = (
            f"# {finding.title}\n\n"
            f"**Finding ID:** `{finding.id}`\n\n"
            f"## Summary\n\n{finding.body}\n\n"
            f"## Evidence\n\n"
            + "\n".join(f"- `{a}`" for a in finding.evidence)
            + "\n"
        )
        path = self.root / "findings" / f"{finding.id}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body)
        return path

    # ── index ───────────────────────────────────────────────────────────────

    def _list_titles(self, subdir: str) -> list[tuple[str, str]]:
        folder = self.root / subdir
        if not folder.exists():
            return []
        out: list[tuple[str, str]] = []
        for md in sorted(folder.glob("*.md")):
            first_heading = next(
                (ln.lstrip("# ").strip() for ln in md.read_text().splitlines() if ln.startswith("# ")),
                md.stem,
            )
            out.append((md.stem, first_heading))
        return out

    def rebuild_index(self) -> None:
        sections = [
            ("Findings", self._list_titles("findings")),
            ("Hypotheses", self._list_titles("hypotheses")),
            ("Entities", self._list_titles("entities")),
            ("Meta", self._list_titles("meta")),
        ]
        lines = ["# Wiki Index", ""]
        for heading, items in sections:
            lines.append(f"## {heading}")
            lines.append("")
            if not items:
                lines.append("_(no pages yet)_")
            else:
                for stem, title in items:
                    lines.append(f"- [{stem}]({stem}.md) — {title}")
            lines.append("")
        (self.root / "index.md").write_text("\n".join(lines))
