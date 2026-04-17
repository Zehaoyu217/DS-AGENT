from __future__ import annotations

from collections import deque
from datetime import date
from typing import Any

from ....issue import IntegrityIssue
from ....protocol import ScanContext
from ..index import MarkdownIndex


def run(ctx: ScanContext, cfg: dict[str, Any], today: date) -> list[IntegrityIssue]:
    idx = MarkdownIndex.build(ctx.repo_root, cfg)
    seeds: list[str] = list(cfg.get("seed_docs", ["CLAUDE.md"]))
    visited: set[str] = set()
    queue: deque[str] = deque()
    for seed in seeds:
        if seed in idx.docs:
            visited.add(seed)
            queue.append(seed)

    while queue:
        cur = queue.popleft()
        for nxt in idx.link_graph.get(cur, set()):
            if nxt in visited:
                continue
            if nxt in idx.docs:
                visited.add(nxt)
                queue.append(nxt)

    issues: list[IntegrityIssue] = []
    for rel in sorted(idx.docs):
        if rel in visited:
            continue
        if rel in idx.ignored:
            continue
        if rel in seeds:
            continue
        issues.append(
            IntegrityIssue(
                rule="doc.unindexed",
                severity="WARN",
                node_id=rel,
                location=rel,
                message=f"Not reachable from {seeds}",
                evidence={"seed_docs": seeds},
                fix_class="claude_md_link",
            )
        )
    return issues
