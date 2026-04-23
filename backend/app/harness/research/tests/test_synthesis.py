from __future__ import annotations

import json
from unittest.mock import MagicMock

from app.harness.research.synthesis import SynthesisAgent
from app.harness.research.types import (
    CodeExample,
    CodeResult,
    PaperFinding,
    PapersResult,
    WebResult,
)


def _mock_http(summary_text: str) -> MagicMock:
    """Mimic an httpx module with .post returning openrouter-shaped JSON."""
    mock_http = MagicMock()
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": json.dumps({
                        "summary": summary_text,
                        "follow_up_questions": ["What dataset should I use?"],
                    }),
                },
            },
        ],
    }
    mock_resp.raise_for_status = MagicMock()
    mock_http.post.return_value = mock_resp
    return mock_http


def test_synthesise_basic():
    papers = PapersResult(papers=(
        PaperFinding(title="Guo 2017", key_finding="temperature scaling works",
                     source="semantic_scholar", arxiv_id="1706.04599"),
    ), crawl_depth=1)
    code = CodeResult(examples=(
        CodeExample(url="https://github.com/org/repo/blob/main/cal.py",
                    repo="org/repo", file_path="cal.py",
                    snippet="from sklearn.calibration import CalibratedClassifierCV",
                    relevance="sklearn calibration example"),
    ))
    web = WebResult()

    agent = SynthesisAgent(http=_mock_http("Temperature scaling is the best approach."))
    result = agent.synthesise(
        query="calibration methods",
        context="",
        papers=papers,
        code=code,
        web=web,
        modules_ran=["papers", "code"],
        total_ms=1200,
        budget_tokens_used=150_000,
    )
    assert result.summary == "Temperature scaling is the best approach."
    assert len(result.papers) == 1
    assert len(result.code_examples) == 1
    assert result.modules_ran == ("papers", "code")
    assert result.total_ms == 1200
    assert result.budget_warning is None


def test_synthesise_sets_budget_warning():
    agent = SynthesisAgent(http=_mock_http("summary"))
    result = agent.synthesise(
        query="q", context="", papers=PapersResult(), code=CodeResult(), web=WebResult(),
        modules_ran=[],
        total_ms=0, budget_tokens_used=1_000_000,
        budget_warning="Hard cap applied.",
    )
    assert result.budget_warning == "Hard cap applied."


def test_synthesise_falls_back_on_api_error():
    mock_http = MagicMock()
    mock_http.post.side_effect = Exception("API down")
    agent = SynthesisAgent(http=mock_http)
    result = agent.synthesise(
        query="test", context="", papers=PapersResult(), code=CodeResult(), web=WebResult(),
        modules_ran=["papers"],
        total_ms=500, budget_tokens_used=50_000,
    )
    assert "papers" in result.modules_ran
    assert isinstance(result.summary, str)


def test_synthesise_strips_markdown_json_fence():
    """Reasoning models sometimes wrap JSON in ```json fences — we must strip them."""
    mock_http = MagicMock()
    mock_resp = MagicMock()
    wrapped = (
        "```json\n"
        + json.dumps({
            "summary": "wrapped", "follow_up_questions": [],
        })
        + "\n```"
    )
    mock_resp.json.return_value = {
        "choices": [{"message": {"content": wrapped}}],
    }
    mock_resp.raise_for_status = MagicMock()
    mock_http.post.return_value = mock_resp

    agent = SynthesisAgent(http=mock_http)
    result = agent.synthesise(
        query="q", context="", papers=PapersResult(), code=CodeResult(), web=WebResult(),
        modules_ran=["papers"],
        total_ms=0, budget_tokens_used=50_000,
    )
    assert result.summary == "wrapped"


def test_result_fields_are_tuples():
    agent = SynthesisAgent(http=_mock_http("done"))
    result = agent.synthesise(
        query="q", context="",
        papers=PapersResult(papers=(
            PaperFinding(title="T", key_finding="f", source="arxiv"),
        )),
        code=CodeResult(),
        web=WebResult(),
        modules_ran=["papers"],
        total_ms=100, budget_tokens_used=50_000,
    )
    assert isinstance(result.papers, tuple)
    assert isinstance(result.code_examples, tuple)
    assert isinstance(result.web_refs, tuple)
    assert isinstance(result.follow_up_questions, tuple)
    assert isinstance(result.modules_ran, tuple)
