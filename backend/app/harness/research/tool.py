from __future__ import annotations

import dataclasses
import logging
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from app.harness.clients.base import ToolSchema
from app.harness.research.jobs import JobRegistry
from app.harness.research.modules.code import CodeModule
from app.harness.research.modules.papers import PapersModule
from app.harness.research.modules.web import WebModule
from app.harness.research.router import RoutingAgent
from app.harness.research.synthesis import SynthesisAgent
from app.harness.research.types import (
    CodeResult,
    PapersResult,
    ResearchResult,
    RoutePlan,
    WebResult,
)

logger = logging.getLogger(__name__)

_BUDGET_HARDCAP = 1_000_000
_BUDGET_WARNING = (
    "Requested budget exceeded 1,000,000 tokens (the hard cap). "
    "Research ran at 1,000,000 tokens. To raise the cap, ask a developer."
)
_MODULE_ESTIMATE_S = {"papers": 30, "code": 15, "web": 10}


def _build_anthropic_client() -> Any:
    import anthropic
    return anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


RESEARCH_SCHEMAS: tuple[ToolSchema, ...] = (
    ToolSchema(
        name="research",
        description=(
            "Run a synchronous research query across papers, code, and/or web sources. "
            "Returns structured findings. Use when the result is needed before your next step. "
            "For long queries (>60s), prefer research_start.\n\n"
            "budget_tokens controls total token spend across all modules. Default 150,000. "
            "The routing agent allocates the budget across modules based on your query. "
            "Hard cap: 1,000,000 tokens. Requests above the cap run at 1M and return "
            "a budget_warning field — contact a developer to raise the cap."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "What to research. Be specific — include domain, method name, metric, "
                        "or constraint. Bad: 'calibration'. Good: 'isotonic regression "
                        "calibration for imbalanced binary classification, LightGBM, post-hoc'."
                    ),
                },
                "context": {
                    "type": "string",
                    "description": "Optional. Context from prior work that narrows the search.",
                },
                "sources": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["papers", "code", "web"]},
                    "description": "Which source modules to run. Omit for all three.",
                },
                "budget_tokens": {
                    "type": "integer",
                    "description": "Total token budget. Default 150,000. Hard cap 1,000,000.",
                },
            },
            "required": ["query"],
        },
    ),
    ToolSchema(
        name="research_start",
        description=(
            "Start a research query in the background and return a job_id immediately. "
            "Use when you have other analysis or tool calls to do while research runs. "
            "Retrieve results with research_get.\n\n"
            "Same budget_tokens semantics as research — default 150,000, hard cap 1,000,000."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "context": {"type": "string"},
                "sources": {
                    "type": "array",
                    "items": {"type": "string", "enum": ["papers", "code", "web"]},
                },
                "budget_tokens": {"type": "integer"},
            },
            "required": ["query"],
        },
    ),
    ToolSchema(
        name="research_get",
        description=(
            "Fetch the result of a research_start job. Non-blocking — returns immediately "
            "with whatever has completed. "
            "status: 'running'=partial only, 'done'=full result available, "
            "'failed'=retry with research synchronously, 'not_found'=job expired."
        ),
        input_schema={
            "type": "object",
            "properties": {"job_id": {"type": "string"}},
            "required": ["job_id"],
        },
    ),
)


class ResearchTool:
    """Orchestrates RoutingAgent → module execution → SynthesisAgent."""

    def __init__(self) -> None:
        api = _build_anthropic_client()
        self._routing_agent = RoutingAgent(api_client=api)
        self._synthesis_agent = SynthesisAgent(api_client=api)
        self._papers_module = PapersModule()
        self._code_module = CodeModule()
        self._web_module = WebModule()
        self._jobs = JobRegistry()

    # ── Public execute / start / get ─────────────────────────────────────────

    def execute(
        self,
        query: str,
        context: str,
        sources: list[str],
        budget_tokens: int,
    ) -> ResearchResult:
        budget_warning: str | None = None
        if budget_tokens > _BUDGET_HARDCAP:
            budget_warning = _BUDGET_WARNING
            budget_tokens = _BUDGET_HARDCAP

        sources = sources or ["papers", "code", "web"]
        t0 = time.monotonic()

        plan = self._routing_agent.route(
            query=query, context=context,
            sources=sources, budget_tokens=budget_tokens,
        )
        papers, code, web = self._run_modules(plan, query)
        total_ms = int((time.monotonic() - t0) * 1000)

        result = self._synthesis_agent.synthesise(
            query=query, context=context,
            papers=papers, code=code, web=web,
            modules_ran=list(plan.modules),
            total_ms=total_ms,
            budget_tokens_used=budget_tokens,
            budget_warning=budget_warning,
        )
        # If the synthesis agent dropped the warning (e.g. mocked or error path),
        # stamp it back so callers always see the cap notification.
        if budget_warning and not result.budget_warning:
            result = dataclasses.replace(result, budget_warning=budget_warning)
        return result

    def start(
        self,
        query: str,
        context: str,
        sources: list[str],
        budget_tokens: int,
    ) -> dict[str, Any]:
        sources = sources or ["papers", "code", "web"]
        est = sum(_MODULE_ESTIMATE_S.get(s, 20) for s in sources)
        job_id = self._jobs.create(query=query, sources=sources, estimated_seconds=est)

        def _run() -> None:
            try:
                result = self.execute(query, context, sources, budget_tokens)
                self._jobs.complete(job_id, result)
            except Exception as exc:
                logger.error("Research job %s failed: %s", job_id, exc)
                self._jobs.fail(job_id, str(exc))

        threading.Thread(target=_run, daemon=True).start()
        return {"job_id": job_id, "estimated_seconds": est}

    def get(self, job_id: str) -> dict[str, Any]:
        return self._jobs.get(job_id)

    # ── Tool handlers (called by ToolDispatcher) ──────────────────────────────

    def handle_research(self, args: dict[str, Any]) -> dict[str, Any]:
        result = self.execute(
            query=args["query"],
            context=args.get("context", ""),
            sources=args.get("sources", ["papers", "code", "web"]),
            budget_tokens=int(args.get("budget_tokens", 150_000)),
        )
        return dataclasses.asdict(result)

    def handle_research_start(self, args: dict[str, Any]) -> dict[str, Any]:
        return self.start(
            query=args["query"],
            context=args.get("context", ""),
            sources=args.get("sources", ["papers", "code", "web"]),
            budget_tokens=int(args.get("budget_tokens", 150_000)),
        )

    def handle_research_get(self, args: dict[str, Any]) -> dict[str, Any]:
        return self.get(args["job_id"])

    # ── Internal module dispatch ──────────────────────────────────────────────

    def _run_modules(
        self, plan: RoutePlan, original_query: str,
    ) -> tuple[PapersResult, CodeResult, WebResult]:
        papers: PapersResult = PapersResult()
        code: CodeResult = CodeResult()
        web: WebResult = WebResult()

        # Build per-module callables with default-arg capture to avoid late-binding
        module_fns: dict[str, Any] = {}
        if "papers" in plan.modules:
            q = plan.sub_queries.get("papers", original_query)
            b = plan.budgets.get("papers", 50_000)
            module_fns["papers"] = lambda q=q, b=b: self._papers_module.run(q, b)
        if "code" in plan.modules:
            q = plan.sub_queries.get("code", original_query)
            b = plan.budgets.get("code", 30_000)
            module_fns["code"] = lambda q=q, b=b: self._code_module.run(q, b)
        if "web" in plan.modules:
            b = plan.budgets.get("web", 20_000)
            urls_raw = plan.sub_queries.get("web", "")
            urls = [urls_raw] if urls_raw else []
            module_fns["web"] = lambda urls=urls, b=b: (
                self._web_module.run(urls, b) if urls else WebResult()
            )

        active = [m for m in plan.modules if m in module_fns]

        if plan.parallel_ok and len(active) > 1:
            with ThreadPoolExecutor(max_workers=3) as ex:
                futures = {ex.submit(module_fns[m]): m for m in active}
                for fut in as_completed(futures):
                    mod = futures[fut]
                    try:
                        r = fut.result()
                        if mod == "papers":
                            papers = r
                        elif mod == "code":
                            code = r
                        elif mod == "web":
                            web = r
                    except Exception as exc:
                        logger.warning("Module %s failed: %s", mod, exc)
        else:
            for mod in active:
                try:
                    r = module_fns[mod]()
                    if mod == "papers":
                        papers = r
                    elif mod == "code":
                        code = r
                    elif mod == "web":
                        web = r
                except Exception as exc:
                    logger.warning("Module %s failed: %s", mod, exc)

        return papers, code, web


# ── Process-wide singleton ────────────────────────────────────────────────────

_research_tool: ResearchTool | None = None
_tool_lock = threading.Lock()


def get_research_tool() -> ResearchTool:
    global _research_tool
    if _research_tool is not None:
        return _research_tool
    with _tool_lock:
        if _research_tool is None:
            _research_tool = ResearchTool()
    return _research_tool


def register_research_tools(dispatcher: Any) -> None:
    """Register research, research_start, research_get with the dispatcher."""
    tool = get_research_tool()
    dispatcher.register("research", tool.handle_research)
    dispatcher.register("research_start", tool.handle_research_start)
    dispatcher.register("research_get", tool.handle_research_get)
