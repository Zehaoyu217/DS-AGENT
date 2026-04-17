# Second Brain v2 — Hybrid Retrieval Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Ship hybrid BM25 + vector retrieval fused via Reciprocal Rank Fusion, opt-in via `habits.retrieval.mode: hybrid`, measurable through an extended `sb eval retrieval --mode compare`.

**Architecture:** Additive. `.sb/vectors.sqlite` (sqlite-vec virtual tables) holds embeddings. New `VectorRetriever` mirrors the existing `Retriever` Protocol. New pure-function `rrf_fuse()` merges BM25 + vector ranked lists into a single `list[RetrievalHit]`. `HybridRetriever` composes both. Existing `BM25Retriever` unchanged; tool contracts unchanged; `sb_search` callers get better hits once habits flip.

**Tech Stack:** Python 3.13, sqlite-vec (pip), sentence-transformers (local fallback), Anthropic embeddings (cloud), pytest, ruamel.yaml.

---

## File Structure

```
src/second_brain/
├── embed/                        # NEW
│   ├── __init__.py
│   ├── base.py                   # Embedder Protocol + EmbeddingVector alias
│   ├── local.py                  # sentence-transformers wrapper
│   └── claude.py                 # Anthropic embeddings API
├── index/
│   ├── retriever.py              # existing — gains HybridRetriever
│   ├── vector_store.py           # NEW — sqlite-vec schema + upsert + topk
│   ├── vector_retriever.py       # NEW
│   └── rrf.py                    # NEW — pure function
├── habits/schema.py              # MODIFIED — add RetrievalHabits.mode, embedding_model, rrf_k
├── reindex.py                    # MODIFIED — gains --with-vectors pipeline
└── cli.py                        # MODIFIED — `sb reindex --with-vectors`, eval `--mode`
```

---

## Task 1: Habits additions

- Add `mode: Literal["bm25", "hybrid"] = "bm25"`, `embedding_model: Literal["local", "claude"] = "local"`, `rrf_k: int = 60` to `RetrievalHabits` in `src/second_brain/habits/schema.py`.
- Test: `tests/test_habits_retrieval_mode.py` asserts defaults + pydantic roundtrip.
- Commit: `chore(sb): add retrieval.mode + embedding_model + rrf_k to habits`

## Task 2: Embedder Protocol + local impl

- Create `src/second_brain/embed/base.py`:
  ```python
  from typing import Protocol
  EmbeddingVector = list[float]
  class Embedder(Protocol):
      dim: int
      def embed(self, texts: list[str]) -> list[EmbeddingVector]: ...
  ```
- Create `src/second_brain/embed/local.py` — lazy import `sentence_transformers`, default model `all-MiniLM-L6-v2`, `dim=384`. Wrap `.encode(texts, normalize_embeddings=True)` → `list[list[float]]`.
- Test: `tests/test_embed_local.py` — skip if sentence-transformers not installed; when present, asserts `len(emb) == 384`, cosine(same-text, same-text) ≈ 1.0.
- Commit: `feat(sb): local embedder (sentence-transformers all-MiniLM-L6-v2)`

## Task 3: Claude embedder

- Create `src/second_brain/embed/claude.py` using Anthropic SDK. Dim read from model metadata. Uses `_fake_client` env-var pattern from existing extract module so tests run hermetically.
- Test: `tests/test_embed_claude.py` — with fake payload env var, asserts batched call + shape.
- Commit: `feat(sb): claude cloud embedder with fake-client test pattern`

## Task 4: VectorStore (sqlite-vec)

- Create `src/second_brain/index/vector_store.py` — context-managed wrapper over `.sb/vectors.sqlite`.
  - `ensure_schema(dim: int)` creates virtual tables `claim_vecs`, `source_vecs` via `vec0` module.
  - `upsert(kind, id, embedding)` — delete+insert.
  - `topk(kind, query_embedding, k) -> list[tuple[id, distance]]` via `MATCH` against `vec0`.
  - `Config.vectors_path` property → `sb_dir / "vectors.sqlite"`.
- Test: `tests/test_vector_store.py` — round-trip 10 vectors, topk returns them in cosine order.
- Commit: `feat(sb): sqlite-vec vector store (claim_vecs + source_vecs)`

## Task 5: pure RRF function

- Create `src/second_brain/index/rrf.py`:
  ```python
  def rrf_fuse(
      lists: list[list[str]],   # each inner list is ranked ids (best first)
      k_rrf: int = 60,
  ) -> list[tuple[str, float]]:
      scores: dict[str, float] = {}
      for ranked in lists:
          for rank, id_ in enumerate(ranked):
              scores[id_] = scores.get(id_, 0.0) + 1.0 / (k_rrf + rank + 1)
      return sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
  ```
- Test: property — fused top hit is whichever id appears highest across lists; unknown ids from one list still merged.
- Commit: `feat(sb): RRF fusion helper (pure function)`

## Task 6: VectorRetriever

- Create `src/second_brain/index/vector_retriever.py`:
  - Constructor takes `Config` + `Embedder` factory (so tests inject fakes).
  - `search(query, k, scope)` → embeds query, calls `VectorStore.topk`, wraps as `RetrievalHit(kind=..., score=rank_normalized, matched_field="vector")`.
- Test: seeded store with 3 claims, query embedding close to one of them → that id is top.
- Commit: `feat(sb): VectorRetriever over sqlite-vec`

## Task 7: HybridRetriever

- Extend `src/second_brain/index/retriever.py`:
  - `class HybridRetriever`: constructor builds `BM25Retriever(cfg)` and `VectorRetriever(cfg)`. `search(query, k, scope)` runs both with `k*3`, extracts id lists, calls `rrf_fuse`, reconstructs `RetrievalHit` (preserves kind + matched_field = `"hybrid:bm25"` or `"hybrid:vec"` based on winning list, defaults to `"hybrid"`).
- Factory: `from second_brain.index.retriever import make_retriever(cfg)` — reads `habits.retrieval.mode` and returns the right impl. `BM25Retriever` stays default when mode is "bm25" OR vectors.sqlite is missing (graceful degrade).
- Test: with a fixture where BM25 alone misses the paraphrase but vector alone finds it, `HybridRetriever` surfaces the right claim at rank 1.
- Commit: `feat(sb): HybridRetriever (BM25 + vectors, RRF-fused)`

## Task 8: Reindex --with-vectors

- Modify `src/second_brain/reindex.py`: after the existing BM25 reindex pass, if `--with-vectors`, iterate claims + sources, embed abstract+statement (claims) / abstract+title (sources), upsert into vector store. Resilient: a batch embedding failure logs + continues.
- Modify `src/second_brain/cli.py`: add `--with-vectors` flag to `sb reindex`.
- Test: `tests/test_reindex_vectors.py` — after reindex, `VectorStore.topk` returns the seeded claim.
- Commit: `feat(sb): sb reindex --with-vectors populates vectors.sqlite`

## Task 9: Eval `--mode bm25|hybrid|compare`

- Modify `src/second_brain/eval/suites/retrieval.py`: accept `mode` parameter; when `mode="compare"`, run the suite twice and emit a two-row report. Default stays `bm25`.
- Modify `src/second_brain/cli.py`: add `--mode` option to `sb eval`.
- New fixture: `tests/eval/fixtures/retrieval/paraphrase.yaml` with queries rephrased from seed.yaml.
- Tests: CLI smoke test for each mode + `--compare` emits both rows.
- Commit: `feat(sb): sb eval retrieval --mode bm25|hybrid|compare`

## Task 10: Hook make_retriever into sb_search tool

- Modify `claude-code-agent/backend/app/tools/sb_tools.py::sb_search` — replace `BM25Retriever(cfg)` with `make_retriever(cfg)`.
- Test in claude-code-agent: assert hybrid path when habits set mode=hybrid AND vectors.sqlite exists; fallback to BM25 otherwise.
- Commit: `feat(sb): backend sb_search uses make_retriever (hybrid-aware)`

## Task 11: Docs + changelog

- `second-brain/README.md`: new `Hybrid retrieval` section under Commands. Bump version line.
- `claude-code-agent/docs/log.md`: one-line changelog entry.
- Commit (sb): `docs(sb): document hybrid retrieval + sb reindex --with-vectors`
- Commit (cc-agent): `docs(sb): changelog — hybrid retrieval`

## Task 12: Coverage gate

- Run `.venv/bin/pytest --cov=second_brain --cov-fail-under=75 --ignore=tests/test_ingest_pdf.py`. If below 75%, add focused tests.
- No commit if no changes needed.

---

## Self-review

- Spec coverage: §2.1 storage → Task 4. §2.2 retriever layer → Tasks 5-7. §2.3 eval gate → Task 9. §2.4 unchanged contracts → Task 10 preserves tool shape. §4 habits → Task 1.
- No placeholders. All tasks have concrete code or file paths.
- Type consistency: `Embedder` Protocol in embed/base.py referenced from both local + claude + VectorRetriever.
