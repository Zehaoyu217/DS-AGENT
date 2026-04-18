# GAN Trace Corpus

The **GAN trace corpus** is the read-only view of the backend's YAML trace
store (`backend/app/trace/store.py`) that GAN evaluator agents consume to
score generator output. The corpus is the same data that powers the
`/api/trace/*` REST routes — this document describes the local CLI
bridge (`scripts/gan-trace-corpus.py`) that avoids a network hop.

## What lives in a trace?

Each trace is a `*.yaml` file under `$TRACE_DIR` (default: `traces/`).
It holds:

- A `summary` block (session id, timestamps, token totals, grade).
- A list of `events` (session start/end, llm_call, tool_call, scratchpad, …).
- A list of `judge_runs` (optional replay results).

Schema lives in `backend/app/trace/events.py` (`Trace`, `TraceSummary`).

## Producing traces

Traces are written by the harness whenever `TRACE_MODE` is `always` or
when a session fails with `on_failure`. Use:

```bash
# Full-trace every run
TRACE_MODE=always make eval

# Replay a trace without the live model
# (see backend/app/trace/recorder.py and judge_replay.py)
```

## Consuming traces from GAN evaluators

Evaluator agents should NOT import backend internals. Instead, shell
out to the CLI bridge:

```bash
# Latest 20 trace summaries as JSON (most recent first)
python scripts/gan-trace-corpus.py --list

# Full trace payload for a specific session
python scripts/gan-trace-corpus.py --load <session_id>

# Custom traces directory (overrides $TRACE_DIR)
python scripts/gan-trace-corpus.py --list --traces-dir backend/traces
```

### Summary shape (`--list`)

```json
[
  {
    "id": "sess-abc",
    "session_id": "sess-abc",
    "started_at": "2026-04-18T10:00:00Z",
    "ended_at": "2026-04-18T10:00:04Z",
    "duration_ms": 4000,
    "event_count": 12,
    "level": 3,
    "level_label": "eval-level3",
    "outcome": "ok",
    "final_grade": "A"
  }
]
```

`event_count` = `turn_count + llm_call_count`. Use it as a cheap proxy
for session complexity when sorting candidates.

### Full-trace shape (`--load`)

The `--load` output is the same JSON returned by
`GET /api/trace/traces/{trace_id}` — the `Trace` pydantic model
serialised with `model_dump()`. Agents can filter events with a
one-liner:

```bash
python scripts/gan-trace-corpus.py --load sess-abc \
  | jq '.events[] | select(.kind == "llm_call") | .prompt_text'
```

## Resolution order for `$TRACE_DIR`

When `--traces-dir` is not given, the CLI picks the first directory
that exists:

1. `$TRACE_DIR` env var
2. `<repo>/backend/traces/`
3. `<repo>/backend/data/traces/`
4. `<cwd>/traces/`

If none exist, `--list` returns `[]` and `--load` exits with code 2.

## Related

- `backend/app/trace/recorder.py` — writes traces.
- `backend/app/trace/judge_replay.py` — scores an existing trace with a
  fresh judge run.
- `backend/app/api/trace_api.py` — the HTTP equivalent of this CLI.
- `backend/tests/trace/test_gan_corpus_cli.py` — round-trip tests for
  the bridge.
