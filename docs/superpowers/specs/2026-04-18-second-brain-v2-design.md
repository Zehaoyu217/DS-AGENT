# Second Brain v2 — design spec

**Date:** 2026-04-18
**Status:** Draft (awaiting implementation plan)
**Scope:** Post-v1 refinement of the second-brain KB. Two themes: (1) retrieval quality via hybrid BM25+embeddings, (2) hands-off LLM maintenance surfaced as a single daily digest — never auto-mutating the KB.

## 0. One-paragraph summary

v1 shipped a working KB with filesystem-as-truth, graph + BM25 indexes, hook-driven injection, and the full 5-tool bridge to claude-code-agent. v2 keeps that foundation unchanged and adds two things. First, **hybrid retrieval**: BM25 stays the baseline; embeddings (sqlite-vec or DuckDB VSS) provide a second ranked list; both are fused via Reciprocal Rank Fusion. `RetrievalHit` shape is preserved, the eval suite from Plan 6 is the fairness gate. Second, **autonomous maintenance → daily digest**: `sb reconcile` is generalised into a nightly Claude-driven pass that reads low-confidence claims, detects wiki↔KB drift, spots taxonomy clusters outside existing roots, and re-evaluates contradiction rationales — but writes nothing to the KB. Everything flows into `digests/YYYY-MM-DD.md` as one-line actionable entries. The user reads the digest; `sb digest apply <entry-id>` (or a conversational "yes, apply 3 and 7") is the only mutation path.

## 1. Goals and non-goals

### Goals
- Retrieval quality: hybrid BM25+embeddings with RRF, measurable via the existing `sb eval retrieval` suite (nDCG@10 must not regress; target +10% on paraphrase queries).
- Hands-off maintenance: the LLM does all the reasoning; the human reads one digest per day.
- Zero silent mutation: every KB write remains a human-approved action.
- Backward compatible: v1 tools, filesystem shape, and hooks unchanged.

### Non-goals (v2)
- MCP server (explicitly dropped by user preference).
- Auto-apply maintenance actions (even under "high confidence" — everything goes through the digest).
- Multi-user / shared KBs.
- Real-time re-embedding mid-conversation (embeddings are built in the same batch as `sb reindex`).
- Graph visualization UI (defer to v3 if needed).

## 2. Hybrid retrieval

### 2.1 Storage

- BM25 index: unchanged — `.sb/kb.sqlite` FTS5.
- Embeddings index: **new** — `.sb/vectors.sqlite` via [sqlite-vec](https://github.com/asg017/sqlite-vec) virtual table. One table per scope: `claim_vecs`, `source_vecs`. Row shape: `(id TEXT PRIMARY KEY, embedding BLOB)`.
- Embedding model: Claude's embedding endpoint when available; falls back to a local model (`sentence-transformers/all-MiniLM-L6-v2`) selected via `habits.retrieval.embedding_model`. Default: local, so `sb reindex` stays offline-capable.
- Vectors index is rebuilt by `sb reindex --with-vectors`. Plain `sb reindex` keeps BM25-only behaviour so existing pipelines are undisturbed.

### 2.2 Retriever layer

New class `HybridRetriever` alongside `BM25Retriever`, same `Retriever` Protocol, same `RetrievalHit` shape. Selected via `habits.retrieval.mode: bm25 | hybrid` (default `bm25` for backward compat; `hybrid` opt-in during v2 rollout, becomes default at v2.1).

Pseudocode:
```
bm25_hits  = BM25Retriever(cfg).search(q, k=k*3, scope=scope)
vec_hits   = VectorRetriever(cfg).search(q, k=k*3, scope=scope)
fused      = rrf_fuse(bm25_hits, vec_hits, k_rrf=60)  # standard RRF
return fused[:k]
```

RRF with k_rrf=60 is the standard; no per-list weight tuning in v2 (keep it honest, no knobs).

### 2.3 Eval gate

- `sb eval retrieval` gains a `--mode bm25|hybrid|compare` flag.
- `--compare` runs both and prints a side-by-side nDCG@10 + p95 latency table. CI-friendly (`--json`).
- Additional fixture: `tests/eval/fixtures/retrieval/paraphrase.yaml` with queries rephrased from seed.yaml. Hybrid should measurably win here; BM25-only should tie on seed.yaml.

### 2.4 What doesn't change

- `sb_search` tool contract unchanged. Callers get better hits for free.
- `sb inject` hook unchanged.
- `RetrievalHit.score` remains a normalized [0.3, 1.0] rank score (now post-RRF).

## 3. Daily digest — the maintenance surface

### 3.1 Core principle

**Nothing the LLM produces during maintenance touches the KB.** Maintenance output is a single markdown file at `~/second-brain/digests/YYYY-MM-DD.md`. The user reads it; `sb digest apply <entry-id>` (or conversational approval through claude-code-agent) is the only path that mutates claims, edges, or taxonomy.

### 3.2 Digest entry shape

Each entry is one line, with a stable entry id for later apply:

```markdown
# Digest 2026-04-18

## Reconciliation
- [r01] clm_foo low-conf since 2025-09; 2 newer sources support → upgrade confidence to medium?
- [r02] clm_bar vs clm_baz contradiction unresolved 47d → draft rationale attached, accept?

## Wiki ↔ KB drift
- [w01] wiki finding "feat/xyz" cited 4× this week → promote to clm_?
- [w02] clm_quux last-cited 180d ago; wiki doc references it → backlink?

## Taxonomy
- [t01] 7 claims cluster outside existing roots (suggested: `papers/security`) → add root?

## Stale
- [s01] 3 abstracts untouched > 120d under `papers/ml/*` → re-abstract batch?
```

Every entry fits one line, starts with a 3-char id (`r01`, `w01`, `t01`, `s01`), ends with an actionable `?`. No prose paragraphs. Skimmable in under 30 seconds.

### 3.3 Apply path

```bash
sb digest apply r01            # apply a single entry
sb digest apply r01 r02 w01    # apply a batch
sb digest apply --all          # approve everything (used sparingly)
sb digest skip r01             # explicit skip; disappears from future digests for N days
```

Each `apply` invokes the exact same tool-use handler the LLM drafted — so "apply" is deterministic replay of a pre-authored action, not a second Claude call. The draft action payload is stored alongside the digest in `digests/YYYY-MM-DD.actions.jsonl` (one JSON line per entry id).

### 3.4 Pipeline

```
sb maintain              # v1 behaviour: lint + analytics + compact
    +
sb maintain --digest     # v2: v1 pipeline + LLM-driven reconciliation pass
                         #     → writes digests/YYYY-MM-DD.md
                         #     → writes digests/YYYY-MM-DD.actions.jsonl
                         #     → NEVER touches claims/, sources/, or graph
```

Scheduled from launchd/cron/systemd (pattern from Plan 5 `docs/automation.md`) for daily runs.

### 3.5 LLM passes

Five autonomous passes, each a schema-constrained Claude call returning a list of digest entries:

1. **Reconciliation** — input: open contradictions + claims with `confidence: low` older than N days. Output: draft resolutions or confidence upgrades.
2. **Wiki↔KB drift** — input: claude-code-agent wiki findings above maturity threshold + stale KB claims. Output: promote / backlink proposals.
3. **Taxonomy drift** — input: claim taxonomies + habits.taxonomy.roots. Output: proposed new roots if >N claims cluster outside existing ones.
4. **Stale review** — input: claims + abstracts with `updated_at > N days` in taxonomies marked `active`. Output: re-abstract batches.
5. **Edge audit** — input: claims with outbound edges whose targets have `status: retracted`. Output: edge cleanup proposals.

Each pass gets a strict tool-use schema. The `claudeception`/eval pattern applies: every pass has a hermetic test fixture under `tests/eval/fixtures/digest/<pass>/`.

### 3.6 Digest coverage in `sb stats`

Health score gains one term: `digest_unread_penalty` — small linear penalty for every digest older than 3 days that hasn't been read (via `sb digest read --mark 2026-04-17`). This keeps the human in the loop without creating a triage queue.

## 4. Habits additions

```yaml
retrieval:
  mode: bm25 | hybrid              # default: bm25 in v2.0, hybrid in v2.1
  embedding_model: local | claude  # default: local
  rrf_k: 60                        # rarely touched

digest:
  enabled: true                    # gate the whole maintenance-to-digest flow
  passes:
    reconciliation: true
    wiki_bridge: true
    taxonomy_drift: true
    stale_review: true
    edge_audit: true
  min_entries_to_emit: 0           # suppress empty digests (set 0 = always emit)
  skip_ttl_days: 14                # how long a `digest skip` lasts
```

All habits optional; absence = v1 behaviour.

## 5. Repository layout deltas

```
src/second_brain/
├── index/
│   ├── retriever.py              # existing — gains HybridRetriever + rrf.py
│   ├── vector_retriever.py       # NEW
│   └── rrf.py                    # NEW — pure function
├── embed/                        # NEW
│   ├── __init__.py
│   ├── local.py                  # sentence-transformers wrapper
│   └── claude.py                 # Anthropic embedding call
├── digest/                       # NEW
│   ├── __init__.py
│   ├── builder.py                # orchestrates 5 passes → digest md + actions jsonl
│   ├── passes/
│   │   ├── reconciliation.py
│   │   ├── wiki_bridge.py
│   │   ├── taxonomy_drift.py
│   │   ├── stale_review.py
│   │   └── edge_audit.py
│   ├── writer.py                 # renders entries → markdown
│   └── applier.py                # replays actions.jsonl
└── cli.py                         # extended: `sb digest {apply,skip,read}`
```

## 6. Migration & rollout

- v2.0 ships `hybrid` and `digest` both opt-in (habits flags default to v1 behaviour).
- 2-week dogfood window on your own KB.
- v2.1 flips `retrieval.mode` default to `hybrid`. `digest.enabled` stays explicit-opt-in since it introduces a new user-facing artifact.
- No schema migrations needed — all new artefacts live under `.sb/vectors.sqlite` and `digests/`.

## 7. Testing

- Unit: `rrf.py` pure-function property tests, `VectorRetriever` against in-memory sqlite-vec table, each digest pass against hermetic fixtures with canned Claude responses.
- Eval: `sb eval retrieval --mode compare` gains its own fixture set. `sb eval digest` (new suite) — for each pass, given fixture input, compare generated entries against golden entries.
- Coverage gate: 75% (unchanged).

## 8. Open questions

- **Embedding cache invalidation:** re-embed on any `*.md` change, or only when `content_hash` changes? Lean `content_hash` — cheap and correct.
- **Digest for multi-day gaps:** if user skips 5 days, do we emit 5 digest files or one merged? Lean "one per day" for auditability + `sb digest ls` to navigate.
- **Apply atomicity:** if `sb digest apply r01 r02` fails halfway, roll back both, or persist partial? Lean all-or-nothing per-invocation; each entry is independent so batching is a UX choice, not a transactional requirement.

## Appendix — What v1 deliberately keeps

- BM25 remains the default retriever (opt-in, not rip-and-replace).
- No MCP (dropped by preference).
- Filesystem is still the source of truth.
- 5-tool bridge contract unchanged.
- Habit-learning proposal files under `proposals/` still work for "habits learn" — v2 doesn't collapse that into the digest because habits are a separate concern (user preferences) from KB state.
