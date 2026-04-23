# Research Tool — Design Spec

**Date:** 2026-04-22  
**Status:** Approved for implementation  
**Scope:** `backend/app/harness/research/`

---

## Problem

The main agent has no way to ground its analysis in current literature, working code examples, or recent ML developments. When a user asks for the "best approach" to calibration, forecasting, or any methodology question, the agent works from training knowledge only — it cannot crawl papers, traverse citation graphs, or find validated implementations.

---

## Solution

A modular **research tool** that the main agent calls as a black box. Internally it runs a coordinator–specialist architecture: a cheap routing LLM decides which source modules to run and with what sub-queries, the modules execute (in parallel when possible), and a cheap synthesis LLM merges the outputs into a structured result.

The main agent gets three tool variants and **chooses** which to use based on context:

| Tool | When to use |
|------|-------------|
| `research` | Synchronous — result needed before next step |
| `research_start` | Async — main agent has parallel work to do |
| `research_get` | Fetch result from a started job (partial if still running) |

All three share the same execution engine. Switching costs one word in the tool call.

---

## Architecture

```
Main agent
  │  research(query, context, sources)        ← sync
  │  research_start(query, context, sources)  ← async, returns job_id
  │  research_get(job_id)                     ← poll / collect
  ▼
ResearchTool.execute()
  │  emits StreamEvent("research_start", {query, sources})
  ▼
RoutingAgent  [haiku-class LLM, ~500 tokens in/out]
  │  input:  query + context
  │  output: {modules_to_run, sub_queries{}, parallel_ok: bool}
  │  emits StreamEvent("research_routing", {plan})
  ▼
ThreadPoolExecutor  (when parallel_ok)
  ├── PapersModule(sub_query, budget_tokens=50_000)
  │     emits StreamEvent("research_progress", {module:"papers", step, found_count})
  │     returns PapersResult
  ├── CodeModule(sub_query, budget_tokens=30_000)
  │     emits StreamEvent("research_progress", {module:"code", step, found_count})
  │     returns CodeResult
  └── WebModule(sub_query, budget_tokens=20_000)
        emits StreamEvent("research_progress", {module:"web", step, found_count})
        returns WebResult
  ▼
SynthesisAgent  [haiku-class LLM, ~2k tokens in/out]
  │  merges module results into structured output
  │  emits StreamEvent("research_done", {modules_ran, total_ms})
  ▼
ResearchResult
  {summary, papers[], code_examples[], web_refs[], follow_up_questions[]}
```

**Sync path:** `ResearchTool.execute()` returns `ResearchResult` directly.  
**Async path:** `ResearchTool.start()` submits to `JobRegistry`, returns `{job_id, estimated_seconds}` immediately. Background thread calls `execute()`. `ResearchTool.get(job_id)` returns partial results if still running.

---

## Tool Schemas

### `research`
```json
{
  "name": "research",
  "description": "Run a synchronous research query across papers, code, and web. Returns structured findings. Use when the result is needed before the next analysis step. For long queries (>60s), prefer research_start.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {"type": "string", "description": "What to research. Be specific — include domain, method name, constraints."},
      "context": {"type": "string", "description": "Optional. Relevant context from prior work that narrows the search (e.g. 'using LightGBM, binary target, imbalanced')."},
      "sources": {
        "type": "array",
        "items": {"type": "string", "enum": ["papers", "code", "web"]},
        "default": ["papers", "code", "web"],
        "description": "Which source modules to run. Omit to run all three."
      }
    },
    "required": ["query"]
  }
}
```

### `research_start`
```json
{
  "name": "research_start",
  "description": "Start a research query in the background and return a job_id immediately. Use when you have other tool calls or analysis to run in parallel. Retrieve results with research_get.",
  "input_schema": {
    "type": "object",
    "properties": {
      "query":   {"type": "string"},
      "context": {"type": "string"},
      "sources": {"type": "array", "items": {"type": "string", "enum": ["papers","code","web"]}, "default": ["papers","code","web"]}
    },
    "required": ["query"]
  }
}
```

### `research_get`
```json
{
  "name": "research_get",
  "description": "Fetch the result of a research_start job. Returns partial results if still running (check status field). Non-blocking.",
  "input_schema": {
    "type": "object",
    "properties": {
      "job_id": {"type": "string"}
    },
    "required": ["job_id"]
  }
}
```

---

## Source Modules

### PapersModule (`modules/papers.py`)

Three-source stack, priority order:

1. **HF Papers feed** (`https://huggingface.co/api/papers`) — best for recent ML (≤30 days). No API key. Used first when query contains recency signals ("recent", "new", "2024", "2025", "state of the art").

2. **Semantic Scholar** (`https://api.semanticscholar.org`) — citation graphs, high-citation search, paper details, section-by-section reading. Primary for landmark/foundational queries. Optional `S2_API_KEY` env var raises rate limits.

3. **ArXiv** (`https://export.arxiv.org/api/query`) — always-available fallback for full paper content. Used when S2 is rate-limited or a specific ArXiv ID is known.

**Operations the module can perform within its token budget:**
- Search by query (all three sources)
- Fetch paper metadata + abstract
- Traverse citation graph (S2) — downstream papers that cite the anchor
- Read specific sections (methodology, experiments, results) via ArXiv HTML
- Extract result-to-recipe mappings: "dataset X + method Y + lr Z → metric W"

**Return type:**
```python
@dataclass
class PapersResult:
    papers: list[PaperFinding]   # ranked by relevance
    crawl_depth: int             # how many hops the citation graph went

@dataclass
class PaperFinding:
    title: str
    arxiv_id: str | None
    year: int | None
    citation_count: int | None
    key_finding: str             # one sentence: what result + what recipe
    section_excerpts: list[str]  # relevant methodology/experiment quotes
    source: str                  # "hf_papers" | "semantic_scholar" | "arxiv"
```

### CodeModule (`modules/code.py`)

Uses `gh` CLI (already in environment). No additional auth needed if `GITHUB_TOKEN` is set.

**Operations:**
- `gh search code <query> --limit 20` — find relevant files
- `gh api repos/{owner}/{repo}/contents/{path}` — read file contents
- Filter by language, stars, recency

**Return type:**
```python
@dataclass
class CodeResult:
    examples: list[CodeExample]

@dataclass
class CodeExample:
    url: str
    repo: str
    file_path: str
    snippet: str       # relevant excerpt, ≤500 chars
    relevance: str     # one sentence: why this is relevant
    stars: int | None
```

### WebModule (`modules/web.py`)

Targeted fetch — not a general crawler. Takes specific URLs or search-derived URLs.

**Operations:**
- `httpx.get(url)` → strip HTML → extract relevant section
- Summarize with a small LLM call if content > 2000 chars

**Return type:**
```python
@dataclass
class WebResult:
    pages: list[WebPage]

@dataclass
class WebPage:
    url: str
    title: str
    summary: str   # ≤300 chars
```

---

## RoutingAgent

A single LLM call (haiku-class) that decides the execution plan.

**Input prompt (template):**
```
Query: {query}
Context: {context}
Available sources: {sources}

Decide:
1. Which modules to run (can be subset of available sources)
2. The sub-query for each module (may differ from the main query)
3. Whether modules can run in parallel (true unless one module's output feeds another's query)

Respond in JSON:
{
  "modules": ["papers", "code"],
  "sub_queries": {"papers": "...", "code": "..."},
  "parallel_ok": true,
  "rationale": "one sentence"
}
```

**Sequential example:** Query = "find code for the calibration method in the Platt 1999 paper" → papers first (get method details), then code with that specific method name. `parallel_ok: false`.

**Parallel example:** Query = "best isotonic calibration approaches" → papers and code simultaneously. `parallel_ok: true`.

---

## SynthesisAgent

A single LLM call (haiku-class) that merges module outputs.

**Input:** serialized module results + original query + context  
**Output:**
```python
@dataclass
class ResearchResult:
    summary: str                        # 2-4 sentences, direct answer to query
    papers: list[PaperFinding]          # from PapersModule
    code_examples: list[CodeExample]    # from CodeModule
    web_refs: list[WebPage]             # from WebModule
    follow_up_questions: list[str]      # what the agent should ask next if needed
    modules_ran: list[str]
    total_ms: int
```

---

## JobRegistry (`jobs.py`)

In-memory, session-scoped. No persistence.

```python
@dataclass
class Job:
    job_id: str
    status: Literal["running", "done", "failed"]
    started_at: float
    query: str
    sources: list[str]
    result: ResearchResult | None
    error: str | None
    partial: dict[str, Any]   # module results as they complete
    estimated_seconds: int
```

`research_get` returns:
```json
{
  "status": "running",
  "elapsed_seconds": 12,
  "estimated_seconds": 45,
  "progress": {"papers": "done", "code": "running", "web": "pending"},
  "partial_result": {"papers": [...]}   // whatever has finished
}
```

Completed jobs expire after 30 minutes (simple TTL check on access).

---

## SSE Events

All events flow through the existing `StreamEvent` system in `app/harness/stream_events.py`. The LLM never sees them — they are UI/observability only.

| Event type | Payload |
|-----------|---------|
| `research_start` | `{query, sources, job_id?}` |
| `research_routing` | `{modules, sub_queries, parallel_ok, rationale}` |
| `research_progress` | `{module, step, found_count, status}` |
| `research_done` | `{modules_ran, total_ms, paper_count, code_count}` |
| `research_error` | `{module, error}` |

---

## File Layout

```
backend/app/harness/research/
  __init__.py
  tool.py          ← ResearchTool: execute(), start(), get() + 3 ToolSchema defs
  router.py        ← RoutingAgent: one LLM call → execution plan
  synthesis.py     ← SynthesisAgent: one LLM call → ResearchResult
  jobs.py          ← JobRegistry: thread-safe dict + TTL expiry
  modules/
    __init__.py
    papers.py      ← PapersModule: HF Papers + Semantic Scholar + ArXiv
    code.py        ← CodeModule: gh CLI wrapper
    web.py         ← WebModule: httpx fetch + summarize
  types.py         ← PaperFinding, CodeExample, WebPage, ResearchResult, Job
  tests/
    test_router.py
    test_synthesis.py
    test_jobs.py
    test_papers.py
    test_code.py
```

**Integration point:** `app/harness/wiring.py` — register the three tool schemas and map `research` / `research_start` / `research_get` to `ResearchTool` methods.

**System prompt addition:** Three entries in the tool catalog with guidance on when to use `research` vs `research_start`.

---

## Error Handling

- **Module failure:** If one module fails, the others continue. `SynthesisAgent` receives whatever completed. Result includes `"modules_ran": ["papers"]` so the agent knows what was skipped.
- **RoutingAgent failure:** Fall back to running all requested modules with the original query, `parallel_ok: true`.
- **Rate limits (S2):** `PapersModule` catches 429s, waits up to 10s, then falls back to ArXiv.
- **Token budget exceeded:** Each module tracks estimated tokens via char count ÷ 4. When within 10% of budget, the module wraps up and returns what it has.
- **Async job not found:** `research_get` returns `{status: "not_found"}` — agent should retry `research` synchronously.

---

## What Is Not In Scope

- Persistent job storage across server restarts
- User-facing job management UI
- Web search (as opposed to targeted web fetch) — no general crawling
- PDF parsing — ArXiv HTML is used instead
- Authentication flows for S2 (just env var, optional)
