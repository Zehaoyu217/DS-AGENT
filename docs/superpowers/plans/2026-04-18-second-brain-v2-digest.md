# Second Brain v2 — Daily Digest Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Ship the hands-off maintenance → daily digest pipeline. Five LLM passes (reconciliation, wiki↔KB drift, taxonomy drift, stale review, edge audit) run autonomously, write one-line actionable entries to `~/second-brain/digests/YYYY-MM-DD.md` + replay-able `actions.jsonl`. `sb digest apply <id>` is the only mutation path. Nothing silently mutates the KB.

**Architecture:** New `digest/` package. Each pass is a `Pass` Protocol impl taking `Config` + fake/real Anthropic client, returning `list[DigestEntry]`. `DigestBuilder` orchestrates, renders markdown + jsonl. `DigestApplier` replays `actions.jsonl` entries through the same tool handlers `sb_promote_claim` and friends already use. `sb maintain --digest` wires it into the Plan 5 maintain pipeline.

**Tech Stack:** Python 3.13, Anthropic SDK (tool-use), ruamel.yaml, pytest. Reuses the extract / reconcile fake-client patterns already in the repo.

---

## File Structure

```
src/second_brain/digest/         # NEW
├── __init__.py
├── schema.py                    # DigestEntry, DigestAction (TypedDict per-pass)
├── builder.py                   # orchestrates passes → markdown + actions.jsonl
├── writer.py                    # renders List[DigestEntry] → markdown
├── applier.py                   # replays actions.jsonl
└── passes/
    ├── __init__.py
    ├── base.py                  # Pass Protocol
    ├── reconciliation.py
    ├── wiki_bridge.py
    ├── taxonomy_drift.py
    ├── stale_review.py
    └── edge_audit.py

src/second_brain/
├── maintain/runner.py           # MODIFIED — --digest path
└── cli.py                       # MODIFIED — `sb digest {build,apply,skip,read,ls}`

src/second_brain/habits/schema.py  # MODIFIED — add DigestHabits
src/second_brain/config.py         # MODIFIED — digests_dir property

tests/digest/                    # NEW — unit tests + hermetic fixtures per pass
```

---

## Task 1: Config.digests_dir + habits additions

- Add `Config.digests_dir` → `home / "digests"`.
- Add `DigestHabits` model (`enabled: bool = False`, `passes: dict[str, bool]` for 5 keys defaulting True, `min_entries_to_emit: int = 0`, `skip_ttl_days: int = 14`) and hang it off `Habits.digest`.
- Tests: `tests/test_config.py` path + `tests/test_habits_digest.py` schema roundtrip.
- Commit: `chore(sb): add digests_dir + DigestHabits schema`

## Task 2: DigestEntry + DigestAction types

- Create `src/second_brain/digest/schema.py`:
  ```python
  from dataclasses import dataclass, field
  @dataclass(frozen=True)
  class DigestEntry:
      id: str               # e.g. "r01" — pass-prefix + zero-padded counter
      section: str          # "Reconciliation" | "Wiki ↔ KB drift" | ...
      line: str             # one-line actionable sentence ending with "?"
      action: dict          # JSON-serialisable payload replayed by DigestApplier
  ```
- Test: dataclass asdict + json round-trip.
- Commit: `feat(sb): DigestEntry + action payload types`

## Task 3: Pass Protocol + base

- Create `src/second_brain/digest/passes/base.py`:
  ```python
  from typing import Protocol, runtime_checkable
  @runtime_checkable
  class Pass(Protocol):
      prefix: str  # "r" | "w" | "t" | "s" | "e"
      section: str
      def run(self, cfg: Config, client: Any | None) -> list[DigestEntry]: ...
  ```
- Test: protocol runtime check against a fake impl.
- Commit: `feat(sb): Pass protocol for digest passes`

## Task 4: Reconciliation pass

- `src/second_brain/digest/passes/reconciliation.py`:
  - Input: from `run_lint(cfg)` and the graph — open contradictions + `confidence: low` claims older than 60 days.
  - Claude tool-use with schema `{action: "upgrade_confidence"|"resolve_contradiction"|"keep", target_id: str, rationale: str}`. Fake-client pattern via env var `SB_DIGEST_FAKE_RECONCILIATION=<json file>`.
  - Returns `DigestEntry` list with prefix `r`.
- Tests: hermetic fixture with 1 open contradiction + 1 low-conf stale claim → 2 entries.
- Commit: `feat(sb): digest reconciliation pass`

## Task 5: Wiki bridge pass

- `src/second_brain/digest/passes/wiki_bridge.py`:
  - Input: wiki findings from `claude-code-agent/knowledge/wiki/` (configurable via env `SB_WIKI_DIR`; skip if unset or absent). Plus stale KB claims un-cited > 90d.
  - Action payloads: `{action: "promote_wiki_to_claim"|"backlink_claim_to_wiki", …}`.
- Tests: with a tmp_path wiki dir containing 1 mature finding → 1 entry; with env unset → 0 entries (no crash).
- Commit: `feat(sb): digest wiki↔KB bridge pass`

## Task 6: Taxonomy drift pass

- `src/second_brain/digest/passes/taxonomy_drift.py`:
  - Input: histogram of claim taxonomies vs `habits.taxonomy.roots`. If N ≥ 5 claims share a prefix outside roots, emit entry with `{action: "add_taxonomy_root", root: <str>}`.
- Pure Python, no Claude call needed (deterministic heuristic). No fake-client needed.
- Tests: inject 5 fake claims under `papers/security/*` → 1 entry; <5 → 0.
- Commit: `feat(sb): digest taxonomy drift pass`

## Task 7: Stale review pass

- `src/second_brain/digest/passes/stale_review.py`:
  - Input: claims with abstracts untouched > 120d (filesystem mtime) in taxonomies with status active.
  - Action: `{action: "re_abstract_batch", claim_ids: [...], taxonomy: "papers/ml/*"}`.
  - Batched: group by taxonomy prefix. Batch size cap from habits or default 10.
- Tests: 3 stale claims under `papers/ml/*` → 1 grouped entry.
- Commit: `feat(sb): digest stale review pass`

## Task 8: Edge audit pass

- `src/second_brain/digest/passes/edge_audit.py`:
  - Input: edges whose target claim has `status: retracted`. Emit `{action: "drop_edge", src_id, dst_id, relation}`.
- Pure graph walk over the graph.duckdb (or FS fallback).
- Tests: fixture with 1 retracted claim cited by 2 edges → 2 entries.
- Commit: `feat(sb): digest edge audit pass`

## Task 9: DigestBuilder

- `src/second_brain/digest/builder.py`:
  ```python
  class DigestBuilder:
      def __init__(self, cfg: Config, client: Any | None = None): ...
      def build(self, date: date | None = None) -> DigestReport: ...
      # runs each habits-enabled pass, assigns stable ids (prefix + 2-digit counter),
      # writes `digests/YYYY-MM-DD.md` + `digests/YYYY-MM-DD.actions.jsonl`
  ```
- Skips passes disabled in habits. Suppresses empty digests when `min_entries_to_emit > 0`.
- Tests: end-to-end with all 5 passes stubbed; asserts markdown file + jsonl file shape + counts.
- Commit: `feat(sb): DigestBuilder — orchestrates passes + writes digest artifacts`

## Task 10: DigestWriter (pure renderer)

- `src/second_brain/digest/writer.py`: `def render(entries: list[DigestEntry], date: date) -> str` — renders entries grouped by section with a `# Digest YYYY-MM-DD` header. Kept pure for testability.
- Tests: snapshot-style comparison of rendered string against expected fixture.
- Commit: `feat(sb): digest markdown writer (pure render)`

## Task 11: DigestApplier

- `src/second_brain/digest/applier.py`:
  ```python
  class DigestApplier:
      def __init__(self, cfg: Config): ...
      def apply(self, date: date, entry_ids: list[str] | Literal["*"]) -> ApplyReport: ...
      # reads actions.jsonl, dispatches by `action` field to handlers
  ```
- Handlers:
  - `upgrade_confidence` → modifies claim frontmatter
  - `resolve_contradiction` → writes `claims/resolutions/<a>__vs__<b>.md`
  - `promote_wiki_to_claim` → calls `sb_promote_claim` logic directly
  - `backlink_claim_to_wiki` → writes backlink into wiki file
  - `add_taxonomy_root` → appends to `habits.yaml` taxonomy roots
  - `re_abstract_batch` → stub that emits a log entry (real re-abstract is a future extension)
  - `drop_edge` → modifies claim frontmatter list
- Applied entries get a `applied_at` line appended to a sidecar `digests/YYYY-MM-DD.applied.jsonl`. Re-applying is a no-op.
- Tests: each handler has a round-trip test (input fixture → apply → assert filesystem effect).
- Commit: `feat(sb): DigestApplier — replay actions to mutate KB`

## Task 12: Skip registry

- `src/second_brain/digest/skips.py`: tiny JSON file at `.sb/digest_skips.json` tracking `{entry_signature_hash: expires_at}`. `DigestBuilder` filters out entries whose signature hash matches an unexpired skip.
- Signature = sha256 of `section + action_type + primary target id`.
- Tests: skip TTL honoured + expired skip reappears.
- Commit: `feat(sb): digest skip registry with TTL`

## Task 13: CLI commands

- Extend `src/second_brain/cli.py` with group `sb digest`:
  - `sb digest build [--date YYYY-MM-DD]` — runs `DigestBuilder`.
  - `sb digest apply [--date] <ids...> [--all]` — runs `DigestApplier`.
  - `sb digest skip [--date] <ids...>` — registers skips from today's digest.
  - `sb digest read [--mark YYYY-MM-DD]` — marks digest as read (for the unread-penalty term).
  - `sb digest ls` — lists digests with read/unread state.
- Tests: CliRunner smoke tests per subcommand.
- Commit: `feat(sb): sb digest {build,apply,skip,read,ls} CLI`

## Task 14: Wire into `sb maintain --digest`

- Modify `src/second_brain/maintain/runner.py`: when `--digest`, after existing pipeline, call `DigestBuilder(cfg).build()`. `MaintainReport` gains `digest_entries: int`, `digest_path: str | None`.
- Modify CLI + JSON output shape.
- Tests: flag on/off produces expected report keys.
- Commit: `feat(sb): sb maintain --digest runs DigestBuilder after maintenance`

## Task 15: Health-score digest_unread_penalty

- Extend `src/second_brain/stats/health.py`: new term — for each digest file older than 3 days without a corresponding entry in the read-marker index, deduct 2 points (capped at 10). Tunable via `HealthWeights.digest_unread_cap`.
- Tests: 0 unread → no deduction; 4 unread digests older than 3d → -8 capped check.
- Commit: `feat(sb): stats health includes digest_unread_penalty`

## Task 16: Eval suite for digest passes

- `src/second_brain/eval/suites/digest.py`: for each pass, given fixture input (claims + wiki state), run the pass and compare its `DigestEntry` list against a golden list (by id + action.keys + target ids). Mismatch counts as failure.
- Fixtures under `tests/eval/fixtures/digest/<pass>/{inputs.yaml, golden.yaml}`.
- `sb eval --suite digest` wired.
- Tests: CLI smoke test; one pass passes, one fixture intentionally fails.
- Commit: `feat(sb): sb eval digest suite (per-pass golden comparison)`

## Task 17: Docs + changelog

- `second-brain/README.md`: new `Digest` section. Bump version.
- `claude-code-agent/docs/log.md`: changelog entry for the hands-off maintenance flow.
- Commit (sb): `docs(sb): document daily digest + sb digest commands`
- Commit (cc-agent): `docs(sb): changelog — hands-off digest maintenance`

## Task 18: Coverage gate

- `.venv/bin/pytest --cov=second_brain --cov-fail-under=75 --ignore=tests/test_ingest_pdf.py` must stay green.

---

## Self-review

- Spec coverage: §3.1 non-mutation → enforced via architecture (passes write only to `digests/`, never to `claims/`). §3.2 entry shape → Tasks 2, 10. §3.3 apply path → Task 11. §3.4 pipeline → Task 14. §3.5 five passes → Tasks 4-8. §3.6 health integration → Task 15. §4 habits → Task 1.
- Each pass hermetic: fake-client env-var pattern where Claude is called; pure Python where not.
- Idempotency: apply writes `applied.jsonl` sidecar; skips tracked by stable signature hash.
- No placeholders. No TBDs.
