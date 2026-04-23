from __future__ import annotations

import json
from unittest.mock import MagicMock

from app.harness.research.router import RoutingAgent
from app.harness.research.types import RoutePlan


def _mock_http(content_text: str) -> MagicMock:
    """Mimic httpx module with .post returning an openrouter-shaped response."""
    mock_http = MagicMock()
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "choices": [{"message": {"content": content_text}}],
    }
    mock_resp.raise_for_status = MagicMock()
    mock_http.post.return_value = mock_resp
    return mock_http


def _mock_http_json(json_content: dict) -> MagicMock:
    return _mock_http(json.dumps(json_content))


def test_route_parallel_query():
    plan_json = {
        "modules": ["papers", "code"],
        "sub_queries": {"papers": "calibration methods", "code": "calibration sklearn"},
        "budgets": {"papers": 90_000, "code": 60_000},
        "parallel_ok": True,
        "rationale": "independent queries",
    }
    router = RoutingAgent(http=_mock_http_json(plan_json))
    plan = router.route(
        query="isotonic calibration LightGBM",
        context="",
        sources=["papers", "code", "web"],
        budget_tokens=150_000,
    )
    assert isinstance(plan, RoutePlan)
    assert plan.parallel_ok is True
    assert "papers" in plan.modules
    assert plan.budgets["papers"] == 90_000


def test_route_strips_markdown_json_fence():
    """Reasoning models (GPT-OSS, Llama) often wrap JSON in ```json fences."""
    plan_json = {
        "modules": ["papers"],
        "sub_queries": {"papers": "q"},
        "budgets": {"papers": 100_000},
        "parallel_ok": True,
        "rationale": "test",
    }
    wrapped = "```json\n" + json.dumps(plan_json) + "\n```"
    router = RoutingAgent(http=_mock_http(wrapped))
    plan = router.route("q", "", ["papers"], 100_000)
    assert plan.modules == ("papers",)


def test_route_falls_back_on_invalid_json():
    router = RoutingAgent(http=_mock_http("not valid json at all"))
    plan = router.route(
        query="test", context="", sources=["papers", "code"], budget_tokens=100_000,
    )
    assert set(plan.modules) == {"papers", "code"}
    assert isinstance(plan.modules, tuple)
    assert plan.parallel_ok is True


def test_route_falls_back_on_api_error():
    mock_http = MagicMock()
    mock_http.post.side_effect = Exception("API error")

    router = RoutingAgent(http=mock_http)
    plan = router.route(
        query="test", context="", sources=["papers"], budget_tokens=50_000,
    )
    assert "papers" in plan.modules
    assert plan.budgets["papers"] == 50_000


def test_budget_not_allocated_to_unselected_modules():
    plan_json = {
        "modules": ["papers"],
        "sub_queries": {"papers": "distribution shift finance"},
        "budgets": {"papers": 150_000},
        "parallel_ok": True,
        "rationale": "papers only",
    }
    router = RoutingAgent(http=_mock_http_json(plan_json))
    plan = router.route("finance", "", ["papers", "code", "web"], 150_000)
    assert "code" not in plan.modules
    assert "web" not in plan.modules


def test_route_plan_modules_is_tuple():
    plan_json = {
        "modules": ["papers", "code"],
        "sub_queries": {"papers": "q1", "code": "q2"},
        "budgets": {"papers": 75_000, "code": 75_000},
        "parallel_ok": True,
        "rationale": "test",
    }
    router = RoutingAgent(http=_mock_http_json(plan_json))
    plan = router.route("q", "", ["papers", "code"], 150_000)
    assert isinstance(plan.modules, tuple)
