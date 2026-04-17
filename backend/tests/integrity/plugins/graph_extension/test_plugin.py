from __future__ import annotations

import json
from pathlib import Path

from backend.app.integrity.plugins.graph_extension.plugin import GraphExtensionPlugin
from backend.app.integrity.protocol import IntegrityPlugin, ScanContext
from backend.app.integrity.schema import GraphSnapshot


def _seed_graph(tmp_path: Path) -> GraphSnapshot:
    g = tmp_path / "graphify"
    g.mkdir()
    (g / "graph.json").write_text(json.dumps({"nodes": [], "links": []}))
    return GraphSnapshot.load(tmp_path)


def test_plugin_satisfies_protocol() -> None:
    plugin = GraphExtensionPlugin()
    assert isinstance(plugin, IntegrityPlugin)
    assert plugin.name == "graph_extension"
    assert plugin.version  # non-empty


def test_plugin_scan_writes_augmented_graph(tmp_path: Path) -> None:
    graph = _seed_graph(tmp_path)
    ctx = ScanContext(repo_root=tmp_path, graph=graph)

    result = GraphExtensionPlugin().scan(ctx)

    aug = tmp_path / "graphify" / "graph.augmented.json"
    assert aug.exists()
    assert result.plugin_name == "graph_extension"
    assert any(str(a).endswith("graph.augmented.json") for a in result.artifacts)
