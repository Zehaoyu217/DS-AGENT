from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ...protocol import ScanContext, ScanResult


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

    def scan(self, ctx: ScanContext) -> ScanResult:
        return ScanResult(plugin_name=self.name, plugin_version=self.version)
