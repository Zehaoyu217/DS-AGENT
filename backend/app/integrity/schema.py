from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class GraphSnapshot:
    """Read-only view of the merged graphify + augmented graph at scan time."""

    nodes: list[dict[str, Any]]
    links: list[dict[str, Any]]

    @classmethod
    def load(cls, repo_root: Path) -> GraphSnapshot:
        graph_path = repo_root / "graphify" / "graph.json"
        base = json.loads(graph_path.read_text())
        nodes_by_id: dict[str, dict[str, Any]] = {n["id"]: n for n in base["nodes"]}
        link_keys: set[tuple[str, str, str]] = set()
        links: list[dict[str, Any]] = []
        for link in base["links"]:
            key = (link["source"], link["target"], link.get("relation", ""))
            if key in link_keys:
                continue
            link_keys.add(key)
            links.append(link)

        aug_path = repo_root / "graphify" / "graph.augmented.json"
        if aug_path.exists():
            aug = json.loads(aug_path.read_text())
            for node in aug.get("nodes", []):
                nodes_by_id[node["id"]] = node  # augmented wins
            for link in aug.get("links", []):
                key = (link["source"], link["target"], link.get("relation", ""))
                if key in link_keys:
                    continue
                link_keys.add(key)
                links.append(link)

        return cls(nodes=list(nodes_by_id.values()), links=links)
