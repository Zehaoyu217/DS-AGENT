from __future__ import annotations
from pathlib import Path

import pytest

from backend.app.integrity.plugins.graph_extension.extractors import fastapi_routes
from backend.app.integrity.schema import GraphSnapshot

FIXTURES = Path(__file__).parent / "fixtures" / "fastapi_app"


@pytest.fixture
def empty_graph() -> GraphSnapshot:
    return GraphSnapshot(nodes=[], links=[])


def _build_repo(tmp_path: Path, fixture: str) -> Path:
    """Mirror `backend/app/api/<fixture>` under tmp_path."""
    api = tmp_path / "backend" / "app" / "api"
    api.mkdir(parents=True)
    (api / fixture).write_text((FIXTURES / fixture).read_text())
    return tmp_path


def test_basic_router_emits_three_routes(tmp_path: Path, empty_graph: GraphSnapshot) -> None:
    repo = _build_repo(tmp_path, "basic_router.py")
    result = fastapi_routes.extract(repo, empty_graph)

    route_ids = sorted(n.id for n in result.nodes)
    assert route_ids == [
        "route::DELETE::/items/{item_id}",
        "route::GET::/items/list",
        "route::POST::/items/create",
    ]
    relations = {(e.source, e.relation) for e in result.edges}
    assert ("route::GET::/items/list", "routes_to") in relations


def test_basic_router_edges_target_handler_function_names(
    tmp_path: Path, empty_graph: GraphSnapshot
) -> None:
    repo = _build_repo(tmp_path, "basic_router.py")
    result = fastapi_routes.extract(repo, empty_graph)

    targets = {e.target for e in result.edges}
    assert "basic_router_list_items" in targets
    assert "basic_router_create_item" in targets
    assert "basic_router_delete_item" in targets
