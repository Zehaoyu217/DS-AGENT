# Gardener — Autonomous LLM Knowledge Maintenance

**Status:** Draft
**Date:** 2026-04-19
**Surface:** Knowledge page (wiki + second-brain)

## Goal

Add a fourth pipeline phase — **Gardener** — that runs LLM-driven passes over
the wiki and second brain to extract claims, maintain abstracts, surface
cross-links, and keep the knowledge base coherent as it grows. Currently,
LLM work happens only during chat turns; structural maintenance (Digest,
Maintain) is rule-based. The Gardener closes that gap without breaking the
existing evidence-gated promotion flow.

## Context

Three-layer knowledge stack:

```
Wiki (per-project, Karpathy pattern)  — agent-authored during chat turns
  ↕
Second Brain (personal, cross-project) — typed atomic claims + digest + graph
  ↕
Gardener (NEW)                         — autonomous LLM passes, proposal-only
```

The Gardener extends the existing **proposal/confirmation split**: today the
chat agent writes to `digests/pending.jsonl` via `sb_digest_propose`; Digest
emits. The Gardener becomes another proposer alongside the agent.

## Non-goals

- Post-emit rollback. Proposals can be edited/deleted in `pending.jsonl`
  before Digest emits; after emit, same story as today.
- Event-triggered firing (after N claims, after Ingest). Deferred — triggers
  are hard to tune and waste tokens on small deltas.
- Moving the existing rule-based Digest passes. They stay; Gardener passes
  run separately and merge into the same `pending.jsonl`.

## Architecture

### Phases

Four pipeline phases total:

```
Ingest    → stage source
Gardener  → LLM passes (extract, re_abstract, semantic_link, …)
             writes to pending.jsonl + gardener.log.jsonl
Digest    → rule passes + gardener proposals → markdown
Maintain  → lint + analytics + reindex
```

`Gardener` fires on-demand via a new **Tend** button alongside
Ingest/Digest/Maintain. Scheduler is a v2 habit knob, not implemented in v1.
Claim extraction — previously a manual agent-tool invocation — becomes the
`extract` pass inside Gardener.

### Authority modes (configurable)

`habits.gardener.mode: "proposal" | "autonomous"` — default `"proposal"`.

- `proposal`: every pass writes to `pending.jsonl`; human reviews via Digest.
- `autonomous`: passes can directly write `claims/*.md`, `wiki/*`, and
  `taxonomy/*` edits. Every write still lands in `gardener.log.jsonl` for
  audit/rollback.

Even in `autonomous` mode, **extraction never overwrites an existing claim
file** without an explicit `force: true` flag. Rewrites are new files with
`supersedes:` frontmatter.

### Passes (7)

Each pass lives at `second-brain/src/second_brain/gardener/passes/{name}.py`
and implements a `GardenerPass` protocol: `run(cfg, client, habits) -> list[Proposal]`.

| Pass              | Tier    | Default | Purpose                                              |
| ----------------- | ------- | ------- | ---------------------------------------------------- |
| `extract`         | default | ON      | Source → atomic claims with `ClaimKind`/`confidence` |
| `re_abstract`     | cheap   | ON      | Rewrite claims flagged in `stale_abstracts`          |
| `semantic_link`   | default | ON      | Propose claim↔claim and claim↔wiki cross-links       |
| `dedupe`          | cheap   | OFF     | Embedding + LLM adjudicated near-duplicate merge     |
| `contradict`      | deep    | OFF     | Read claim pairs for subtle contradictions           |
| `taxonomy_curate` | default | OFF     | Propose new roots, relocate misfiled claims          |
| `wiki_summarize`  | cheap   | OFF     | Compact long findings, promote hypotheses            |

Toggled via `habits.gardener.passes.{name}: bool` and mirrored in the UI
settings drawer.

### Model tiers

Three configurable model slots in `habits.gardener.models`:

```yaml
gardener:
  models:
    cheap: anthropic/claude-haiku-4-5
    default: anthropic/claude-sonnet-4-6
    deep: anthropic/claude-opus-4-7
```

Each pass declares a tier; user picks the model for each tier. Advanced
users can override per-pass in `habits.gardener.passes.{name}.model_override`.

Model list comes from the existing `_OPENROUTER_MODELS` — untouched per the
saved rule that file is user-owned.

### Cost controls (configurable)

```yaml
gardener:
  max_cost_usd_per_run: 0.50        # hard stop if exceeded mid-run
  max_tokens_per_source: 8000       # per-pass input cap
  dry_run: false                    # estimate tokens/cost, no API calls
```

Pre-flight: every pass declares `estimate(cfg) -> CostEstimate` so the UI can
show "this run will cost ~$0.12" before the user confirms. Hard stop trips
mid-run if actual tokens exceed budget; partial results still land in
`pending.jsonl`.

### Audit

**Dual-layer** logging:

1. `second-brain/.sb/.state/gardener.log.jsonl` — append-only, one row per
   proposal emitted: `{ts, pass, input_ref, output_summary, model, tokens,
   cost_usd, accepted: null}`. `accepted` gets flipped to `true`/`false`
   when Digest emits or skips the proposal.

2. Pipeline state ledger — add `gardener` as fourth phase alongside
   ingest/digest/maintain. Last-run summary: `{passes_run, proposals_added,
   total_tokens, total_cost_usd, duration_ms, errors}`.

HUD shows a fourth phase dot for Gardener. Clicking opens an activity panel
that tails `gardener.log.jsonl`.

## UI changes (Knowledge page)

### Toolbar (header)

Add **Tend** button between Maintain and the Graph toggle:

```
[Ingest] [Digest] [Maintain] [Tend] │ [Graph]
```

Same `PipelineToolbarButton` component; dims when no pending sources/claims
to tend. Click opens the Gardener drawer.

### Gardener drawer

Drawer slot (same pattern as Ingest/Digest/Graph):

```
┌─ GARDENER ────────────────────────────────────┐
│ Tier models                                   │
│   cheap    [claude-haiku-4-5       ▾]         │
│   default  [claude-sonnet-4-6      ▾]         │
│   deep     [claude-opus-4-7        ▾]         │
│                                               │
│ Passes                                        │
│   ☑ extract         (default)                 │
│   ☑ re_abstract     (cheap)                   │
│   ☑ semantic_link   (default)                 │
│   ☐ dedupe          (cheap)                   │
│   ☐ contradict      (deep)                    │
│   ☐ taxonomy_curate (default)                 │
│   ☐ wiki_summarize  (cheap)                   │
│                                               │
│ Budget                                        │
│   max cost per run    [ $0.50    ]            │
│   max tokens / source [ 8000     ]            │
│   ☐ dry run                                   │
│                                               │
│ Authority                                     │
│   ( ) proposal-only (safe)                    │
│   ( ) autonomous (direct writes)              │
│                                               │
│ ──────────                                    │
│ Estimate: ~2,400 tokens · ~$0.08              │
│                                               │
│ [ Run gardener ]                              │
└───────────────────────────────────────────────┘
```

All settings persist to `habits.yaml`; changing them POSTs to a new
`/api/sb/gardener/habits` endpoint. Run button POSTs to
`/api/sb/gardener/run` with overrides (e.g., dry-run toggle).

### Activity panel

Bottom drawer slot showing last 50 lines of `gardener.log.jsonl`, filterable
by pass, with "accepted/rejected" status pulled from Digest emit outcome.

## Files

### Backend — new

```
second-brain/src/second_brain/gardener/
  __init__.py
  runner.py           # orchestrates passes, budget enforcement, audit write
  protocol.py         # GardenerPass protocol, Proposal dataclass, CostEstimate
  passes/
    __init__.py
    extract.py
    re_abstract.py
    semantic_link.py
    dedupe.py
    contradict.py
    taxonomy_curate.py
    wiki_summarize.py
  audit.py            # gardener.log.jsonl append/read helpers
  cost.py             # per-model pricing table, tokenizer adapter

backend/app/api/sb_gardener.py   # /api/sb/gardener/{status,run,habits,log,estimate}
backend/app/tools/sb_pipeline_state.py  # extend with gardener phase slot
```

### Backend — modified

- `backend/app/tools/sb_pipeline_state.py` — add `gardener` phase key, extend
  `read_state`/`write_phase` literal types.
- `second-brain/src/second_brain/habits/schema.py` — add `GardenerHabits`
  with `mode`, `models`, `passes`, `max_cost_usd_per_run`,
  `max_tokens_per_source`, `dry_run`.
- `second-brain/src/second_brain/digest/pending.py` — mark proposals with
  `origin: "gardener" | "agent"` so audit can flip `accepted` correctly.

### Frontend — new

```
frontend/src/components/gardener/
  GardenerPanel.tsx        # drawer contents (passes/models/budget/authority)
  GardenerActivity.tsx     # activity tail panel
  ModelTierPicker.tsx      # 3 dropdowns bound to habits.models
  PassToggleList.tsx       # 7 checkboxes with tier badges
  BudgetControls.tsx       # cost + token cap + dry-run toggle
  AuthorityRadio.tsx       # proposal / autonomous
```

### Frontend — modified

- `frontend/src/sections/KnowledgeSurface.tsx` — add Tend button, drawer route.
- `frontend/src/lib/pipeline-store.ts` — add `gardener` phase slot + `runGardener` action.
- `frontend/src/lib/surfaces-store.ts` — `knowledgeDrawer` union gains `'gardener'`.

## Contracts

### `GardenerPass` protocol

```python
class GardenerPass(Protocol):
    name: str                        # stable id, e.g. "extract"
    tier: Literal["cheap", "default", "deep"]
    prefix: str                      # pending.jsonl id prefix, e.g. "gx"

    def estimate(self, cfg: Config, habits: Habits) -> CostEstimate: ...
    def run(
        self,
        cfg: Config,
        habits: Habits,
        client: LLMClient,
        budget: Budget,          # tripped when exceeded
    ) -> Iterator[Proposal]: ...
```

### `Proposal`

```python
@dataclass(frozen=True)
class Proposal:
    pass_name: str
    section: str           # target digest section (reconciliation, wiki_bridge, ...)
    line: str              # human-readable one-liner
    action: dict[str, Any] # action payload (same shape as DigestEntry.action)
    input_refs: list[str]  # claim ids / source ids consulted
    tokens_in: int
    tokens_out: int
    cost_usd: float
```

### Run endpoint

`POST /api/sb/gardener/run`

```json
{
  "passes": ["extract", "semantic_link"],  // override habits, optional
  "dry_run": false,
  "budget_override": { "max_cost_usd_per_run": 1.0 }
}
```

Response:

```json
{
  "ok": true,
  "passes_run": ["extract", "semantic_link"],
  "proposals_added": 23,
  "total_tokens": 14800,
  "total_cost_usd": 0.12,
  "duration_ms": 8400,
  "errors": []
}
```

## Testing

- Unit: each pass with a stubbed `LLMClient` returning canned outputs;
  assert `Proposal` structure, `input_refs`, and budget accounting.
- Integration: `runner.run()` against a tmp `.sb` with 3 sources + 10
  claims; assert `pending.jsonl` growth, `gardener.log.jsonl` appends,
  ledger update.
- Budget: test hard-stop mid-run when cost cap tripped; assert partial
  proposals land and `errors` reports `budget_exceeded`.
- Frontend: `GardenerPanel` with mocked habits; toggle passes,
  change tiers, verify POST payload; click Run and assert button state
  transitions + activity panel update.
- E2E (Playwright): open Knowledge → Tend drawer, change default tier
  model, click Run in dry-run mode, assert estimate shown, no network
  hit to Anthropic/OpenRouter.

## Risks / open questions

- **Token estimation accuracy** — tokenizer-level estimates are cheap but
  can under-count ~5%. Budget check uses actual usage when available; pre-flight
  estimate is advisory, not a contract.
- **Proposal quality in `semantic_link`** — embedding recall is easy; LLM
  judgement on "is this link useful?" is the hard part. Ship with a
  conservative prompt; iterate based on rejection rate in activity panel.
- **`autonomous` mode and skills** — gardener can trigger skill calls
  (e.g., claim extraction via existing sandbox). Deferred: for v1 gardener
  calls LLM directly, no skill dispatch.
- **OpenRouter rate limits** — concurrent passes could hit per-minute
  caps. Runner serializes passes by default; concurrency is a later habit.

## Build order

Rough phases for the implementation plan:

1. **Scaffolding** — `GardenerPass` protocol, `Proposal`, audit, cost, budget.
2. **Runner + first pass** — `extract`, wired end-to-end from UI button.
3. **Remaining Tier 1/2** — `re_abstract`, `semantic_link`.
4. **Settings UI** — model tiers, pass toggles, budget controls, authority
   radio, dry-run.
5. **Activity panel + ledger** — `gardener.log.jsonl` tail, phase dot in HUD.
6. **Remaining passes** — `dedupe`, `contradict`, `taxonomy_curate`,
   `wiki_summarize`.
7. **Autonomous mode** — direct writes path + `supersedes:` frontmatter.

Scheduler (cron habit) stays deferred to a follow-up spec.
