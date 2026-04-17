from __future__ import annotations

from dataclasses import dataclass, field

from ...protocol import ScanContext, ScanResult
from .augmenter import augment
from .extractors import fastapi_routes, intra_file_calls, jsx_usage


@dataclass
class GraphExtensionPlugin:
    name: str = "graph_extension"
    version: str = "1.0.0"
    depends_on: tuple[str, ...] = ()
    paths: tuple[str, ...] = field(
        default=(
            "backend/app/api/**/*.py",
            "backend/app/main.py",
            "backend/app/**/*.py",
            "frontend/src/**/*.tsx",
            "frontend/src/**/*.jsx",
        )
    )

    def scan(self, ctx: ScanContext) -> ScanResult:
        manifest = augment(
            ctx.repo_root,
            extractors=[
                ("fastapi_routes", fastapi_routes.extract),
                ("intra_file_calls", intra_file_calls.extract),
                ("jsx_usage", jsx_usage.extract),
            ],
        )
        artifacts = [
            ctx.repo_root / "graphify" / "graph.augmented.json",
            ctx.repo_root / "graphify" / "graph.augmented.manifest.json",
        ]
        return ScanResult(
            plugin_name=self.name,
            plugin_version=self.version,
            artifacts=artifacts,
            failures=manifest.get("failures", []),
        )
