from __future__ import annotations
from pathlib import Path

import pytest

from backend.app.integrity.plugins.graph_extension.extractors import intra_file_calls
from backend.app.integrity.schema import GraphSnapshot

FIXTURES = Path(__file__).parent / "fixtures" / "intra_file"


@pytest.fixture
def empty_graph() -> GraphSnapshot:
    return GraphSnapshot(nodes=[], links=[])


def _scan(tmp_path: Path, fixture: str, empty_graph: GraphSnapshot):
    py = tmp_path / "backend" / "app" / "module.py"
    py.parent.mkdir(parents=True)
    py.write_text((FIXTURES / fixture).read_text())
    return intra_file_calls.extract(tmp_path, empty_graph)


def test_module_level_call_emits_calls_edge(tmp_path, empty_graph: GraphSnapshot) -> None:
    result = _scan(tmp_path, "two_funcs.py", empty_graph)
    edges = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("module_public", "module_helper", "calls") in edges


def test_isolated_function_emits_no_outgoing_calls(tmp_path, empty_graph: GraphSnapshot) -> None:
    result = _scan(tmp_path, "two_funcs.py", empty_graph)
    sources = {e.source for e in result.edges}
    assert "module_isolated" not in sources


def test_self_method_call_emits_class_method_edge(tmp_path, empty_graph: GraphSnapshot) -> None:
    result = _scan(tmp_path, "self_method.py", empty_graph)
    edges = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("module_double", "module_add", "calls") in edges


def test_decorated_helper_call_resolves_to_def(tmp_path, empty_graph: GraphSnapshot) -> None:
    result = _scan(tmp_path, "decorated_helpers.py", empty_graph)
    edges = {(e.source, e.target, e.relation) for e in result.edges}
    assert ("module_caller", "module_cached_value", "calls") in edges
