from __future__ import annotations

from app.harness.research.types import (
    CodeExample,
    CodeResult,
    PaperFinding,
    PapersResult,
    ResearchResult,
    RoutePlan,
    WebPage,
    WebResult,
)


def test_paper_finding_defaults():
    pf = PaperFinding(title="Test", key_finding="finding", source="arxiv")
    assert pf.arxiv_id is None
    assert pf.year is None
    assert pf.citation_count is None
    assert pf.section_excerpts == []


def test_research_result_budget_warning_default():
    rr = ResearchResult(
        summary="test",
        papers=[],
        code_examples=[],
        web_refs=[],
        follow_up_questions=[],
        modules_ran=["papers"],
        total_ms=100,
        budget_tokens_used=150_000,
    )
    assert rr.budget_warning is None


def test_route_plan_structure():
    plan = RoutePlan(
        modules=["papers", "code"],
        sub_queries={"papers": "q1", "code": "q2"},
        budgets={"papers": 90_000, "code": 60_000},
        parallel_ok=True,
        rationale="independent queries",
    )
    assert plan.budgets["papers"] == 90_000
    assert plan.parallel_ok is True


def test_budget_warning_set():
    rr = ResearchResult(
        summary="test",
        papers=[],
        code_examples=[],
        web_refs=[],
        follow_up_questions=[],
        modules_ran=["papers"],
        total_ms=100,
        budget_tokens_used=1_000_000,
        budget_warning="Hard cap applied.",
    )
    assert rr.budget_warning is not None
