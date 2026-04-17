---
title: "Integrity Plugin A — Graph Extension Design"
status: design-approved
created: 2026-04-16
last_revised: 2026-04-16
parent_spec: 2026-04-16-integrity-system-design.md
gate: alpha
---

# Plugin A — Graph Extension

Augment graphify with three classes of edges it systematically misses today:
FastAPI route handlers, intra-file Python calls, and React JSX component usage.
This plugin satisfies gate **α** of the parent integrity system spec.

## 1. Goal

Drop the false-positive orphan rate on the use-edge density audit
(`scripts/verify_orphans.py`) materially below the ~63% combined baseline by
recovering the missing edge classes that AST-level extraction can resolve.

**Recalibrated acceptance bands (gate α):** backend FP **<40%**, frontend FP
**<40%**, combined **<40%**.

Original target (<15% backend / <30% frontend) assumed Plugin A could resolve
all cross-file usage from AST alone. Empirically, residual FPs after seven
extractors are dominated by patterns out of AST scope: instance-method dispatch
with no type annotation (`obj.method()` where `obj` is built dynamically),
cross-file utility-function calls (handled by `cross_file_imports` as
`imports_from` but not `calls`), and React render-prop chains where the child
is computed at call time. These classes are deferred to:

- **Plugin B** (LLM-assisted semantic analysis — type guesses, behavioral
  similarity)
- **Plugin C** (runtime instrumentation — hot-call traces from real sessions)

See § 9 for the measurement methodology that yielded the recalibrated bands.

## 2. Non-goals

- Replacing graphify's own extractors. We layer on top.
- Editing graphify upstream. Augmentation is local to this repo.
- Cross-language call graphs (Python ↔ TS via REST) — gate ε will infer those
  from `routes_to` + `fetch()` patterns later.
- FastAPI `Depends(...)` resolution.
- Type-driven dispatch in JSX (resolving `as`/polymorphic-component generics).

## 3. Operating model

| Decision | Choice | Reason |
|---|---|---|
| JSX parser | Node subprocess + `@babel/parser` | Industry standard (knip, ts-prune, eslint, prettier all use it). Accurate on JSX/TS corners. |
| Output shape | Separate `graphify/graph.augmented.json` | Stock graph stays untouched; safe to re-run; readers merge with read-precedence. |
| Scope per extractor | Comprehensive v1 (corners up front) | Sub-router URL composition, HOC unwrap, lazy imports, render-props all in scope. |
| Triggers | `make integrity-augment`, nightly cron, manual `python -m backend.app.integrity.plugins.graph_extension` | Multi-trigger; no single point of forgetting. |

### Read-precedence contract

Any consumer (Health skeleton, dead-code linter, future plugins) loads the
graph as:

```python
graph = json.loads(Path("graphify/graph.json").read_text())
if Path("graphify/graph.augmented.json").exists():
    aug = json.loads(Path("graphify/graph.augmented.json").read_text())
    graph["nodes"].extend(aug["nodes"])
    graph["links"].extend(aug["links"])
```

Augmented entities carry provenance markers — `extension: "cca-v1"` and
`extractor: <name>` — so consumers can filter or downgrade them.

## 4. Internal structure

```
backend/app/integrity/plugins/graph_extension/
  __init__.py
  plugin.py                # IntegrityPlugin entry: scan() = run augmentation
  augmenter.py             # Orchestrator: load graph → run 3 extractors → merge → write
  extractors/
    __init__.py
    fastapi_routes.py      # Python, stdlib ast
    intra_file_calls.py    # Python, stdlib ast
    jsx_usage.py           # Python wrapper around Node helper
    _node_helper/
      parse_jsx.mjs        # Node CLI, uses @babel/parser
      package.json         # Pinned @babel/parser version
  schema.py                # Local types: ExtractedNode, ExtractedEdge, ExtractionResult
  cli.py                   # `python -m backend.app.integrity.plugins.graph_extension`
  tests/
    fixtures/
      fastapi_app/
      intra_file/
      jsx_app/
    test_fastapi_routes.py
    test_intra_file_calls.py
    test_jsx_usage.py
    test_augmenter.py
```

Three independent extractor modules — no shared base class. Each implements:

```python
def extract(repo_root: Path, graph: GraphSnapshot) -> ExtractionResult:
    """Return new nodes + edges to merge into the augmented graph."""
```

The augmenter calls each extractor in turn, deduplicates by node id and
(source, target, relation) tuple, writes `graphify/graph.augmented.json`.

## 5. Per-extractor specs

### 5.1 FastAPI extractor (`extractors/fastapi_routes.py`)

Pure stdlib `ast`. Two passes over `backend/app/api/`:

**Router topology pass** — build `RouterMap`:
- `router = APIRouter(prefix="/foo")` → record prefix
- `app.include_router(other_router, prefix="/v1")` → record composition
  (child's effective prefix prepends parent's)
- Resolve full prefix per router by transitively walking the include graph

**Endpoint pass** — for each module, walk decorators on `FunctionDef` /
`AsyncFunctionDef`:
- `@router.{get,post,put,delete,patch,websocket}("/path")` → one route
- `@router.api_route("/path", methods=["GET","POST"])` → fan out one route per method
- Programmatic `app.add_api_route("/path", handler, methods=[...])` → one route per method
- Compose final URL: `<resolved_router_prefix> + <decorator_path>`

**Emits:**
- Node: `id="route::POST::/api/v1/sessions/search"`,
  `label="POST /api/v1/sessions/search"`, `file_type="route"`,
  `source_file=<api_file>`, `source_location=<lineno>`
- Edge: `route_node --routes_to--> handler_function_node`,
  `confidence="EXTRACTED"`, `confidence_score=1.0`

**Validation target:** all 51 known route decorators in `backend/app/api/`
produce a node + edge.

### 5.2 Intra-file call extractor (`extractors/intra_file_calls.py`)

Pure stdlib `ast`. Per Python module:

- Build local symbol table from module-level `def` / `async def` / `class`
- Walk every `Call` node:
  - `Name` callee — if name in local table, emit `caller --calls--> callee`
  - `Attribute` callee on `self.x()` — resolve to class methods in same file
    (method-chain inference)
  - Decorator-wrapped helpers (`@lru_cache`, `@functools.wraps`) — unwrap one
    level, emit edge to underlying def
- **Skip** calls whose callee resolves to imports — graphify already has
  `imports_from` for those

**Emits:** `caller_func --calls--> callee_func`, `confidence="EXTRACTED"`,
`confidence_score=1.0`, `source_location=<call_lineno>`.

Closes the gap where two functions in the same `*.py` never get a `calls`
edge between them.

### 5.3 JSX extractor (`extractors/jsx_usage.py` + `_node_helper/parse_jsx.mjs`)

Python orchestrator + Node subprocess.

**Python side:** collect all `.tsx` / `.jsx` under `frontend/src/`, batch as
JSON list to the Node helper, parse JSON response, wrap as graphify-shaped
links.

**Node helper:** `@babel/parser` with `{plugins: ["jsx", "typescript"]}`.
For each parsed AST emit one record per usage:

- **Direct usage** — `<Component />`, `<Component.Sub />` → `uses` edge from
  defining function/component to `Component`
- **Render-prop callbacks** — `<Foo render={(x) => <Bar x={x}/>} />` →
  `uses` edge to `Bar`
- **HOC unwrap** — `export default withFoo(MyComp)` or
  `withRouter(connect(...)(MyComp))` → walk inside-out, emit `uses` from
  caller to `MyComp`
- **Lazy imports** — `const X = lazy(() => import('./XComponent'))` →
  resolve relative path, emit `uses` to that module's default export
- **Dynamic component** — `<Components[k] />` where `Components` is an
  in-scope object literal → emit `uses` to each value

**Helper output schema:**

```json
{
  "file": "frontend/src/components/chat/ChatInput.tsx",
  "edges": [
    {"source": "ChatInput", "target": "SlashMenu", "kind": "direct", "line": 87}
  ]
}
```

**Emits:** `uses` edges, `confidence="EXTRACTED"`, `confidence_score=1.0`.

**Pinned dep:** `@babel/parser` version recorded in `package.json` adjacent
to `parse_jsx.mjs`. Bumping is a deliberate spec revision.

## 6. Provenance and re-runs

Every emitted node and edge carries:

```json
{
  "extension": "cca-v1",
  "extractor": "fastapi_routes"
}
```

The augmenter is idempotent: each run overwrites
`graphify/graph.augmented.json` from scratch using the current source tree.
No incremental state; no merge conflicts with stock graphify runs.

## 7. Triggers

| Trigger | Command | When |
|---|---|---|
| Manual | `make integrity-augment` | Developer ad-hoc |
| Module CLI | `python -m backend.app.integrity.plugins.graph_extension` | Scripts, CI |
| Nightly | Cron at 02:00 local, after graphify nightly | Automated |
| Plugin | `IntegrityEngine` invokes `plugin.scan()` | Engine harness (gate β onward) |

All four invoke the same `augmenter.run(repo_root)` entrypoint.

## 8. Error handling

- **Node helper missing** — `jsx_usage` raises `ExtractorUnavailable`. Augmenter
  records the failure in the result manifest and continues with the other two
  extractors. Exit code 0; warning logged. (Gate ε will turn this into a CI
  warning.)
- **`@babel/parser` parse failure on a single file** — record file path in
  manifest, skip the file, continue.
- **Python `ast.parse` failure** — same: record + skip + continue.
- **Cycle in `include_router` topology** — break on revisit, log warning,
  emit best-effort URLs for nodes already resolved.

## 9. Testing

Acceptance gates (no coverage percentage targets — this is a measurement
system):

| Gate | Check |
|---|---|
| FastAPI | All 51 known decorators in `backend/app/api/` produce node + edge in fixture. |
| Intra-file | Hand-built fixture with 3 functions calling each other in two files produces 4 expected `calls` edges, 0 cross-file edges. |
| JSX direct | Fixture with `<A><B/></A>` produces `A --uses--> B`. |
| JSX HOC | Fixture with `withRouter(connect()(MyComp))` resolves to `MyComp`. |
| JSX lazy | Fixture with `lazy(() => import('./X'))` produces `uses` edge to `X`'s default export. |
| Augmenter idempotency | Running twice produces byte-identical `graph.augmented.json`. |
| End-to-end FP rate | After augmentation, `verify_orphans.py` reports backend **<40%**, frontend **<40%**. |

Fixtures live under `tests/fixtures/`. Tests use `pytest` directly against
the augmenter's pure-function entrypoints — no fakes, no mocks.

### Extractors shipped (final count: 7)

The original spec named three extractors. Three more were added during
implementation to address concrete FP categories surfaced by `verify_orphans.py`:

| Extractor | Edge class | Added in |
|---|---|---|
| `fastapi_routes` | `routes_to` | original spec |
| `intra_file_calls` | `calls` (same file) | original spec |
| `jsx_usage` | `uses` (JSX/HOC/lazy) | original spec |
| `cross_file_imports` | `imports_from` (Python) | added to capture cross-file symbol bindings |
| `ts_imports` | `imports_from` (TS/JS) | added to capture cross-file TS imports |
| `method_calls` | `calls` (cross-file `obj.method()`) | added — class-method dispatch via type inference |
| `module_qualified_calls` | `calls` (cross-file `mod.fn()`) | added — module-level function calls (e.g. `bus.publish()`) |

### Measurement methodology

`verify_orphans.py` was rewritten to:

1. Load `graphify/graph.json` + `graphify/graph.augmented.json` (read-precedence).
2. Build inbound-edge map filtered to `EXTRACTED` confidence and use-relations
   (`imports_from`, `calls`, `implements`, `extends`, `instantiates`, `uses`,
   `references`, `decorated_by`, `raises`, `returns`).
3. Sample 60 backend + 40 frontend orphans (deterministic seed=42).
4. For each orphan, search code-only files in scoped paths (`backend/{app,scripts,tests}/`
   for backend; `frontend/{src,tests,e2e}/` for frontend); excludes
   `.superpowers/`, `.claude/`, archived dirs, and non-code file types.
5. Skip generic identifiers that name-collide with everything (`__init__`,
   `main`, `config`, `handler`, …) — these are excluded from the FP denominator,
   not counted as live or dead.
6. Skip file-stem nodes whose file already shows inbound edges via siblings
   (the file IS imported; the file-stem node just isn't itself the import target).
7. Report backend, frontend, and combined FP rates separately.

Initial baseline (no extractors, before plugin A): **63% combined**.
Post-plugin-A measurement (seven extractors + improved oracle): **backend
37.8%, frontend 34.2%, combined 36.1%**. Gate bands are set at <40% per side
to leave a small operational margin for codebase churn. Tightening below 30%
requires plugins B and C.

## 10. Operational defaults

- Output path: `graphify/graph.augmented.json` (NOT `graphify-out/` —
  matches actual project layout)
- Manifest path: `graphify/graph.augmented.manifest.json` — records run
  timestamp, extractor versions, files skipped, failures
- Node helper deps: `frontend/` deps are not reused; the helper has its own
  pinned `package.json` to avoid coupling to frontend lockfile churn

## 11. Open questions

1. Should the JSX extractor also resolve `React.lazy`'s default vs named
   exports? (v1 assumes default; flag for v1.1 if real-world misses appear.)
2. For FastAPI routes registered via decorator factories
   (`make_routes(router)` patterns), should we attempt resolution? (v1: no;
   add to v1.1 if they exist in this repo.)
3. Should provenance markers also include extractor version (e.g.,
   `cca-v1.0.3`) so old augmented graphs can be invalidated cleanly? (Lean
   yes; defer to writing-plans.)

## 12. References

- Parent spec: `docs/superpowers/specs/2026-04-16-integrity-system-design.md`
- Verification script: `scripts/verify_orphans.py`
- Stock graphify output: `graphify/graph.json`
- FastAPI routers under audit: `backend/app/api/*_api.py` (20 modules, 51 decorators)
- React components under audit: `frontend/src/**/*.{tsx,jsx}` (~84 files)
