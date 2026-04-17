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
    assert ("Direct", "Inner", "uses") in relations


def test_hoc_unwrap(tmp_path: Path, empty_graph: GraphSnapshot) -> None:
    repo = _build_repo(tmp_path, ["HOC.tsx"])
    result = jsx_usage.extract(repo, empty_graph)
    targets = {e.target for e in result.edges}
    assert "MyComp" in targets


def test_lazy_import(tmp_path: Path, empty_graph: GraphSnapshot) -> None:
    repo = _build_repo(tmp_path, ["LazyImport.tsx"])
    result = jsx_usage.extract(repo, empty_graph)
    targets = {e.target for e in result.edges}
    assert "Heavy" in targets


def test_render_prop_callback(tmp_path: Path, empty_graph: GraphSnapshot) -> None:
    repo = _build_repo(tmp_path, ["RenderProp.tsx"])
    result = jsx_usage.extract(repo, empty_graph)
    targets = {e.target for e in result.edges}
    assert "Inner" in targets
    assert "Outer" in targets


def test_no_frontend_dir_returns_empty(tmp_path: Path, empty_graph: GraphSnapshot) -> None:
    result = jsx_usage.extract(tmp_path, empty_graph)
    assert result.edges == []
