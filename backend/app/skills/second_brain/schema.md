---
name: second_brain_schema
description: "[Reference] Second Brain schemas — source + claim frontmatter, edge relations, id prefixes. Loaded only after parent `second_brain` skill."
---

# Schema reference

## ID prefixes

| Prefix | Kind |
|---|---|
| `src_` | Source (paper, blog, repo, note, url) |
| `clm_` | Claim (atomic statement) |

IDs are deterministic slugs of title + disambiguator; see the `slugs` module.

## Source frontmatter (`sources/<slug>/_source.md`)

```yaml
id: src_...
slug: "..."
title: "..."
kind: paper | blog | url | repo | note | other
ingested_at: <iso ts>
origin: { uri: "...", kind: "file" | "url" | "gh" }
content_hash: sha256-...
taxonomy: "papers/ml"   # optional
abstract: "..."         # optional
```

## Claim frontmatter (`claims/<slug>.md`)

```yaml
id: clm_...
statement: "..."                  # atomic, falsifiable
kind: empirical | theoretical | definitional | opinion | prediction
confidence: low | medium | high
scope: ""                          # optional: narrows applicability
supports: [clm_..., ...]           # outbound edges
contradicts: [clm_..., ...]
refines: [clm_..., ...]
extracted_at: <iso ts>
status: active | superseded | retracted | disputed
resolution: "..."                  # set when a contradiction is resolved
abstract: "..."
```

## Edge relations

| Relation | Semantics |
|---|---|
| `cites` | Claim cites a source (implicit via body markdown link) |
| `supports` | A supports B (strengthens) |
| `refines` | A refines B (narrows or improves precision) |
| `contradicts` | A contradicts B (open until `rationale`/`resolution` set) |

A contradiction is **resolved** when either side's claim has `resolution:` set
OR the corresponding edge row carries a non-empty `rationale`.
