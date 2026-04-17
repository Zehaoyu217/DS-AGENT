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


def _build_repo_multi(tmp_path: Path, fixtures: list[str]) -> Path:
    api = tmp_path / "backend" / "app" / "api"
    api.mkdir(parents=True)
    (api / "__init__.py").write_text("")
    for f in fixtures:
        (api / f).write_text((FIXTURES / f).read_text())
    return tmp_path


def test_api_route_fans_out_methods(tmp_path: Path, empty_graph: GraphSnapshot) -> None:
    repo = _build_repo_multi(tmp_path, ["api_route_methods.py"])
    result = fastapi_routes.extract(repo, empty_graph)

    ids = {n.id for n in result.nodes}
    assert "route::GET::/multi/both" in ids
    assert "route::POST::/multi/both" in ids


def test_add_api_route_emits_route(tmp_path: Path, empty_graph: GraphSnapshot) -> None:
    repo = _build_repo_multi(tmp_path, ["api_route_methods.py"])
    result = fastapi_routes.extract(repo, empty_graph)

    ids = {n.id for n in result.nodes}
    assert "route::PUT::/programmatic" in ids


def test_include_router_composes_prefix(tmp_path: Path, empty_graph: GraphSnapshot) -> None:
    repo = tmp_path
    (repo / "backend" / "app" / "api").mkdir(parents=True)
    (repo / "backend" / "app" / "api" / "__init__.py").write_text("")
    (repo / "backend" / "app" / "api" / "composed_router.py").write_text(
        (FIXTURES / "composed_router.py").read_text()
    )
    (repo / "backend" / "app" / "main.py").write_text(
        (FIXTURES / "main_with_include.py").read_text()
    )

    result = fastapi_routes.extract(repo, empty_graph)
    ids = {n.id for n in result.nodes}
    assert "route::GET::/v1/inner/leaf" in ids
