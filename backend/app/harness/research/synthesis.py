from __future__ import annotations

import json
import logging
from typing import Any

from app.harness.research.llm import openrouter_chat, strip_json_fence
from app.harness.research.types import (
    CodeResult,
    PapersResult,
    ResearchResult,
    WebResult,
)

logger = logging.getLogger(__name__)

_MAX_TOKENS = 1024

_SYSTEM_PROMPT = """\
You are a synthesis agent. You receive research findings from multiple source modules
(papers, code examples, web pages) and produce a structured summary for a data scientist
or ML engineer.

Your output MUST be valid JSON with this exact shape:
{
  "summary": "2-4 sentences directly answering the query, citing specific findings",
  "follow_up_questions": ["question if more research needed", ...]
}

Rules:
- summary must cite specific papers, methods, or code found — not generic statements
- follow_up_questions: 0-3 questions the agent should research next; empty list if none needed
- Respond ONLY with the JSON object. No prose before or after."""


class SynthesisAgent:
    """Merges module outputs into a ResearchResult via OpenRouter chat-completions."""

    def __init__(self, http: Any) -> None:
        self._http = http

    def synthesise(
        self,
        query: str,
        context: str,
        papers: PapersResult,
        code: CodeResult,
        web: WebResult,
        modules_ran: list[str],
        total_ms: int,
        budget_tokens_used: int,
        budget_warning: str | None = None,
    ) -> ResearchResult:
        user_msg = self._build_user_message(query, context, papers, code, web)
        summary = ""
        follow_ups: tuple[str, ...] = ()

        try:
            text = openrouter_chat(
                self._http,
                system=_SYSTEM_PROMPT,
                user=user_msg,
                max_tokens=_MAX_TOKENS,
            )
            data = json.loads(strip_json_fence(text))
            summary = data.get("summary", "")
            follow_ups = tuple(data.get("follow_up_questions", []))
        except Exception as exc:
            logger.warning("SynthesisAgent failed (%s) — using raw results", exc)
            ran = ", ".join(modules_ran)
            summary = f"Research completed across {ran}. See papers and code below."

        return ResearchResult(
            summary=summary,
            papers=papers.papers,
            code_examples=code.examples,
            web_refs=web.pages,
            follow_up_questions=follow_ups,
            modules_ran=tuple(modules_ran),
            total_ms=total_ms,
            budget_tokens_used=budget_tokens_used,
            budget_warning=budget_warning,
        )

    def _build_user_message(
        self,
        query: str,
        context: str,
        papers: PapersResult,
        code: CodeResult,
        web: WebResult,
    ) -> str:
        parts = [f"Query: {query}"]
        if context:
            parts.append(f"Context: {context}")

        if papers.papers:
            parts.append(f"\n## Papers found ({len(papers.papers)})")
            for p in papers.papers[:10]:
                parts.append(f"- [{p.source}] {p.title} ({p.year}): {p.key_finding}")

        if code.examples:
            parts.append(f"\n## Code examples found ({len(code.examples)})")
            for ex in code.examples[:5]:
                parts.append(f"- {ex.repo}: {ex.relevance}\n  {ex.snippet[:200]}")

        if web.pages:
            parts.append(f"\n## Web pages found ({len(web.pages)})")
            for pg in web.pages[:3]:
                parts.append(f"- {pg.title}: {pg.summary}")

        parts.append("\nSynthesize these findings.")
        return "\n".join(parts)
