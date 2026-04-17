from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from backend.app.integrity.plugins.graph_extension.extractors import jsx_usage
from backend.app.integrity.schema import GraphSnapshot

FIXTURES = Path(__file__).parent / "fixtures" / "jsx_app"


@pytest.fixture
def empty_graph() -> GraphSnapshot:
    return GraphSnapshot(nodes=[], links=[])


def _build_repo(tmp_path: Path, names: list[str]) -> Path:
    src = tmp_path / "frontend" / "src"
    src.mkdir(parents=True)
    for name in names:
        shutil.copy(FIXTURES / name, src / name)
    return tmp_path


def test_direct_component_usage(tmp_path: Path, empty_graph: GraphSnapshot) -> None:
    repo = _build_repo(tmp_path, ["Direct.tsx"])
    result = jsx_usage.extract(repo, empty_graph)
    relations = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("direct_direct", "inner_inner", "uses") in relations


def test_hoc_unwrap(tmp_path: Path, empty_graph: GraphSnapshot) -> None:
    repo = _build_repo(tmp_path, ["HOC.tsx"])
    result = jsx_usage.extract(repo, empty_graph)
    targets = {e.target for e in result.edges}
    assert "mycomp_mycomp" in targets


def test_lazy_import(tmp_path: Path, empty_graph: GraphSnapshot) -> None:
    repo = _build_repo(tmp_path, ["LazyImport.tsx"])
    result = jsx_usage.extract(repo, empty_graph)
    targets = {e.target for e in result.edges}
    assert "heavy_heavy" in targets


def test_render_prop_callback(tmp_path: Path, empty_graph: GraphSnapshot) -> None:
    repo = _build_repo(tmp_path, ["RenderProp.tsx"])
    result = jsx_usage.extract(repo, empty_graph)
    targets = {e.target for e in result.edges}
    assert "inner_inner" in targets
    assert "outer_outer" in targets


def test_resolves_to_existing_graph_node(tmp_path: Path) -> None:
    repo = _build_repo(tmp_path, ["Direct.tsx"])
    graph = GraphSnapshot(
        nodes=[
            {"id": "direct_direct", "label": "Direct()"},
            {"id": "components_inner", "label": "Inner()"},
        ],
        links=[],
    )
    result = jsx_usage.extract(repo, graph)
    relations = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("direct_direct", "components_inner", "uses") in relations


def test_no_frontend_dir_returns_empty(tmp_path: Path, empty_graph: GraphSnapshot) -> None:
    result = jsx_usage.extract(tmp_path, empty_graph)
    assert result.edges == []
