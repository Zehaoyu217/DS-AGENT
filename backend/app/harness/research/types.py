from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class PaperFinding:
    title: str
    key_finding: str          # one sentence: result + recipe
    source: str               # "hf_papers" | "semantic_scholar" | "arxiv"
    arxiv_id: str | None = None
    year: int | None = None
    citation_count: int | None = None
    section_excerpts: list[str] = field(default_factory=list)


@dataclass
class PapersResult:
    papers: list[PaperFinding] = field(default_factory=list)
    crawl_depth: int = 0


@dataclass
class CodeExample:
    url: str
    repo: str
    file_path: str
    snippet: str              # ≤500 chars
    relevance: str            # one sentence
    stars: int | None = None


@dataclass
class CodeResult:
    examples: list[CodeExample] = field(default_factory=list)


@dataclass
class WebPage:
    url: str
    title: str
    summary: str              # ≤300 chars


@dataclass
class WebResult:
    pages: list[WebPage] = field(default_factory=list)


@dataclass
class RoutePlan:
    modules: list[str]
    sub_queries: dict[str, str]
    budgets: dict[str, int]
    parallel_ok: bool
    rationale: str


@dataclass
class ResearchResult:
    summary: str
    papers: list[PaperFinding]
    code_examples: list[CodeExample]
    web_refs: list[WebPage]
    follow_up_questions: list[str]
    modules_ran: list[str]
    total_ms: int
    budget_tokens_used: int
    budget_warning: str | None = None
