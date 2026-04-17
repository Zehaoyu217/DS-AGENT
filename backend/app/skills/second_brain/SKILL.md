---
name: second_brain
description: "[Reference] Second Brain KB — markdown-as-truth, graph-backed, BM25-indexed knowledge base. Use when the agent needs to retrieve grounded claims, walk typed edges, or write atomic findings into the KB via sb_search / sb_load / sb_reason / sb_ingest / sb_promote_claim."
---

# Second Brain skill — Level-1 reference

This is a **reference skill**. Load it when you need authoritative context about
the Second Brain KB (filesystem shape, tool contracts, edge semantics).

## The KB in one paragraph

Files on disk at `$SECOND_BRAIN_HOME` (default `~/second-brain/`). Sources live
in `sources/<slug>/_source.md` with `raw/*` attachments. Claims live in
`claims/<slug>.md` — one atomic statement per file. Edges (typed relations with
confidence) are derived from claim frontmatter and written to
`.sb/graph.duckdb`. A BM25 index lives at `.sb/kb.sqlite`. Contradictions are
first-class edges with `rationale:` notes, not merge conflicts.

## When to use tools vs shell

Inside claude-code-agent you have five JSON tools; prefer them over spawning
`sb` subprocesses during a conversation.

| Tool | Use for |
|---|---|
| `sb_search` | BM25 retrieval (natural prompt OK; OR-tokenised) |
| `sb_load` | Fetch a node + its 1-hop neighbourhood |
| `sb_reason` | Typed walk over `supports` / `refines` / `contradicts` |
| `sb_ingest` | Push a local file into the KB mid-conversation |
| `sb_promote_claim` | Persist a new atomic claim (writes `claims/<slug>.md`) |

All five return `{"ok": false, "error": "second_brain_disabled", ...}` when
`SECOND_BRAIN_ENABLED` is false. Don't treat that as failure — it means the user
hasn't initialised a KB.

## Grounding contract

1. When the user asks a factual question, always call `sb_search` first.
2. Cite claim ids (`clm_...`) when stating KB-derived facts.
3. Surface contradictions explicitly. Never silently pick one side.
4. Promote a finding into a claim only when it is atomic, falsifiable, and new.

## Sub-skills

- `schema.md` — full frontmatter schemas + id prefixes.
- `reasoning-patterns.md` — walk templates and anti-patterns.
