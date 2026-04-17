---
title: Integrity Plugin E (config_registry) — gate δ
status: design-approved
created: 2026-04-17
last_revised: 2026-04-17
owner: jay
parent_spec: 2026-04-16-integrity-system-design.md
gate: δ
depends_on:
  - 2026-04-16-integrity-plugin-a-design.md   # gate α — shipped (consumes graph.augmented.json for routes)
  - 2026-04-17-integrity-plugin-b-design.md   # gate β — shipped (engine + report aggregator)
---

# Plugin E — `config_registry`

> Sub-spec for gate δ of the integrity system. Parent: `2026-04-16-integrity-system-design.md` §5.4. This document is the single source of truth for Plugin E's scope, design, and acceptance criteria. Edit in place; bump `last_revised`.

## 1. Goal

Materialise `claude-code-agent`'s **single source of truth** for what is wired into the system, committed and diffable across commits:

`config/manifest.yaml` — a deterministically sorted YAML inventory covering:

1. **Skills** — every entry under `backend/app/skills/` discoverable by `SkillRegistry`.
2. **Scripts** — every `scripts/**/*.{py,sh,ts,js}` with interpreter + content sha.
3. **Routes** — every FastAPI route extracted by Plugin A (`graph.augmented.json`).
4. **Configs** — every well-known config file (`pyproject.toml`, `.claude/settings.json`, `package.json`, `vite.config.*`, `Dockerfile*`, `Makefile`, `.env.example`, `infra/**`, etc.) with detected type + content sha.
5. **Functions** — Python entry-point functions decorated with `@router/@app/@api_router` plus FastAPI event handlers (`startup`/`shutdown`/`lifespan`), captured by AST.

The plugin emits 3 drift rules:
- `config.added` (INFO) — entry present in current scan but absent from prior committed manifest.
- `config.removed` (INFO normally; WARN if still referenced per dep graph).
- `config.schema_drift` (WARN) — config file violates its per-type schema validator.

All checks build on the engine, snapshots, and aggregator shipped at gate β. Plugin E does not depend on any other plugin (no `depends_on` entries); it gracefully degrades when `graph.augmented.json` is absent.

## 2. Non-goals

- **Schema authoring.** Per-type schemas live in `plugins/config_registry/schemas/`; they encode the shape that we already enforce informally. Generic JSON Schema authoring is out of scope.
- **Auto-fix.** Plugin E reports drift; gate ζ (Plugin F) is the autofix gate.
- **Cross-repo manifests.** Single repo only.
- **Frontend route inventory.** SPA route extraction is out of scope for δ; can be added in a future Plugin E.1 once frontend has a router.
- **Static type-check of configs.** We hash content + run schema validators; we don't type-check.
- **Live config reloading.** Manifest is built at scan time; the engine doesn't watch for changes.

## 3. Decisions locked from brainstorm

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Manifest format | YAML, deterministically sorted, committed at `config/manifest.yaml` | Diffable in PRs; source of truth; matches `config/integrity.yaml` co-location |
| Hash algorithm | Git blob SHA-1 (`blob {len}\0{content}`) | Matches `git ls-files -s`; survives identical-content moves; avoids reinventing |
| Skill id format | Dotted path from `skills_root` (e.g. `reporting.dashboard_builder`) | Matches `SkillRegistry._index` key shape (parity for acceptance gate) |
| Script interpreter detection | Shebang first, then extension fallback (`.py`→python3, `.sh`→bash, `.ts`/`.js`→node) | Shebang is authoritative; extension is a safe default |
| Routes source | Re-export from `graph.augmented.json` if present, empty list otherwise | No duplicated extraction; honours Plugin A as upstream |
| Config type detection | Filename + extension matchers in `builders/configs.py` | Explicit table beats heuristics; new types added by extending the table |
| Function extraction | Python AST walker; matches `@<name>.<verb>(...)` and `@app.on_event("...")` | AST is robust vs regex; trivial to extend |
| Manifest writer | Custom YAML emitter (sorted keys, block style, stable quoting) | `yaml.safe_dump` non-deterministic across PyYAML versions; we own emission |
| Schema validators | Pure-Python per-type modules in `plugins/config_registry/schemas/` | No new dep; each schema is a small focused module |
| Removed-with-references upgrade | If a removed entry's id appears in any node id / source_file in graph → severity `WARN` not `INFO` | Catches dead-but-referenced configs without false-positive flood |
| Diff cadence | Each scan compares current build vs prior committed `config/manifest.yaml` | Manifest is the canonical "prior"; integrity-out artifacts are journal, not source |
| .gitignore semantics | Skip files matching `.gitignore` (read repo `.gitignore` once per scan) | Avoids spurious entries for build artifacts |
| Plugin output artifact | `integrity-out/{date}/config_registry.json` (delta + counts + failures) | Mirrors Plugin B/C pattern |

## 4. Architecture

### 4.1 File layout

```
backend/app/integrity/plugins/config_registry/
  __init__.py
  plugin.py                          # ConfigRegistryPlugin (mirrors GraphLintPlugin / DocAuditPlugin shape)
  manifest.py                        # read/write config/manifest.yaml deterministically
  hashing.py                         # git-compatible blob SHA helpers
  builders/
    __init__.py
    skills.py                        # SkillsBuilder — walks skills_root tree
    scripts.py                       # ScriptsBuilder — walks scripts_root + detects interpreter
    routes.py                        # RoutesBuilder — re-export from graph.augmented.json
    configs.py                       # ConfigsBuilder — type-detected, glob-driven
    functions.py                     # FunctionsBuilder — Python AST for @router/@app + FastAPI events
  rules/
    __init__.py
    added.py                         # config.added
    removed.py                       # config.removed (INFO/WARN escalation)
    schema_drift.py                  # config.schema_drift (per-type schema validators)
  schemas/
    __init__.py
    base.py                          # SchemaValidator Protocol + ValidationFailure dataclass
    pyproject.py                     # validates pyproject.toml shape
    package_json.py                  # validates package.json shape
    claude_settings.py               # validates .claude/settings.json shape
    integrity_yaml.py                # validates config/integrity.yaml shape (self-check)
    makefile.py                      # validates Makefile (target name pattern, .PHONY consistency)
    dockerfile.py                    # validates Dockerfile (FROM stage names referenced, etc.)
    env_example.py                   # validates .env.example (KEY=VALUE pattern)
    vite_config.py                   # validates vite.config.{ts,js} (export default present)
    tsconfig.py                      # validates tsconfig*.json (compilerOptions present, JSON shape)
  tests/
    __init__.py
    conftest.py                      # tiny_repo fixture builder + helpers
    fixtures/
      tiny_repo/                     # synthetic mini-repo
        backend/app/skills/
          alpha/
            SKILL.md                 # frontmatter: name=alpha, version=1.0.0
            skill.yaml               # dependencies.packages=[]
            __init__.py
          beta/
            sub_skill/
              SKILL.md               # nested skill (parity for tree shape)
              __init__.py
            SKILL.md
            __init__.py
        scripts/
          deploy.sh                  # bash interpreter
          gen_data.py                # python interpreter
          build.ts                   # node interpreter
        config/
          integrity.yaml             # plugins.config_registry.enabled=true
        graphify/
          graph.augmented.json       # contains 2 route nodes + 1 dead-route node (id no longer in code)
        backend/app/api/foo_api.py   # @router.get("/foo") + @app.on_event("startup")
        pyproject.toml               # valid + an intentional drift variant per test
        package.json
        .claude/settings.json
        Dockerfile
        Makefile
        .env.example
        vite.config.ts
        tsconfig.json
        .gitignore
        config/manifest.yaml         # prior committed manifest (for diff tests)
    test_hashing.py                  # git-blob sha matches `git hash-object`
    test_manifest_roundtrip.py       # write→read deterministic; sorted; idempotent
    test_builder_skills.py           # parity with SkillRegistry._index size + ids
    test_builder_scripts.py          # interpreter detection (shebang + ext)
    test_builder_routes.py           # graph re-export; absent graph → empty list
    test_builder_configs.py          # type detection table; .gitignore respected
    test_builder_functions.py        # @router.<verb>, @app.on_event, lifespan
    test_rule_added.py               # new entry → config.added INFO
    test_rule_removed.py             # removed entry → INFO; with graph reference → WARN
    test_rule_schema_drift.py        # invalid pyproject → schema_drift WARN
    test_schemas_pyproject.py        # one (+) and one (–) per schema module
    test_schemas_package_json.py
    test_schemas_claude_settings.py
    test_schemas_integrity_yaml.py
    test_schemas_makefile.py
    test_schemas_dockerfile.py
    test_schemas_env_example.py
    test_schemas_vite_config.py
    test_schemas_tsconfig.py
    test_skill_count_parity.py       # acceptance-gate proof: manifest skill count == SkillRegistry._index size
    test_plugin_integration.py       # full scan against tiny_repo with exact issue counts
    test_round_trip_add_fixture.py   # acceptance-gate proof: add-test-fixture-config → scan → diff catches it
```

### 4.2 Plugin shape

Mirrors `GraphLintPlugin` and `DocAuditPlugin`:

```python
@dataclass
class ConfigRegistryPlugin:
    name: str = "config_registry"
    version: str = "1.0.0"
    depends_on: tuple[str, ...] = ()                           # no plugin deps
    paths: tuple[str, ...] = (
        "backend/app/skills/**/SKILL.md",
        "backend/app/skills/**/skill.yaml",
        "scripts/**/*.py",
        "scripts/**/*.sh",
        "scripts/**/*.ts",
        "scripts/**/*.js",
        "pyproject.toml",
        "package.json",
        ".claude/settings.json",
        "vite.config.*",
        "tsconfig*.json",
        "Dockerfile*",
        "Makefile",
        ".env.example",
        "infra/**",
        "config/**",
        "backend/app/api/**/*.py",
    )
    config: dict[str, Any] = field(default_factory=dict)
    today: date = field(default_factory=date.today)
    rules: dict[str, Rule] | None = None

    def scan(self, ctx: ScanContext) -> ScanResult:
        # 1. Run all builders → assemble current manifest dict.
        # 2. Read prior manifest from config/manifest.yaml (if present).
        # 3. Write current manifest back to config/manifest.yaml (deterministic).
        # 4. Run each enabled rule (added / removed / schema_drift), per-rule try/except.
        # 5. Emit IntegrityIssue list + write integrity-out/{date}/config_registry.json.
```

### 4.3 Rule signature

Reuses Plugin B/C's `Rule` type, extended with `current` and `prior` manifest dicts (passed via the config dict to keep the protocol stable):

```python
Rule = Callable[[ScanContext, dict[str, Any], date], list[IntegrityIssue]]
```

The plugin populates `cfg["_current_manifest"]`, `cfg["_prior_manifest"]`, and `cfg["_dep_graph"]` (built from `ctx.graph`) before invoking each rule. This matches the existing engine's `Rule` shape — no new protocol.

### 4.4 Manifest schema

`config/manifest.yaml` shape (top-level keys sorted; entries within each key sorted by id):

```yaml
# AUTO-GENERATED by integrity Plugin E (config_registry).
# Do not edit by hand — re-run `make integrity-config` after intended changes.
# See docs/superpowers/specs/2026-04-17-integrity-plugin-e-design.md.

generated_at: "2026-04-17"
generator_version: "1.0.0"
manifest_version: 1

configs:
  - id: "Dockerfile"
    type: "dockerfile"
    path: "Dockerfile"
    sha: "<git-blob-sha>"
  - id: "Makefile"
    type: "makefile"
    path: "Makefile"
    sha: "<git-blob-sha>"
  - id: ".claude/settings.json"
    type: "claude_settings"
    path: ".claude/settings.json"
    sha: "<git-blob-sha>"
  # ...

functions:
  - id: "backend.app.api.chat_api.trace_endpoint"
    path: "backend/app/api/chat_api.py"
    line: 1173
    decorator: "router.post"
    target: "/api/trace"
  - id: "backend.app.main.startup"
    path: "backend/app/main.py"
    line: 42
    decorator: "app.on_event"
    target: "startup"

routes:
  - id: "route::POST::/api/trace"
    method: "POST"
    path: "/api/trace"
    source_file: "backend/app/api/chat_api.py"
    source_location: 1173
    extractor: "fastapi_routes"

scripts:
  - id: "scripts/deploy.sh"
    path: "scripts/deploy.sh"
    interpreter: "bash"
    sha: "<git-blob-sha>"
  - id: "scripts/gen_data.py"
    path: "scripts/gen_data.py"
    interpreter: "python3"
    sha: "<git-blob-sha>"

skills:
  - id: "analysis_plan"
    path: "backend/app/skills/analysis_plan/SKILL.md"
    yaml_path: "backend/app/skills/analysis_plan/skill.yaml"
    version: "1.0.0"
    description: "Build a structured analysis plan…"
    parent: null
    children: []
    sha_skill_md: "<git-blob-sha>"
    sha_skill_yaml: "<git-blob-sha>"
  - id: "reporting.dashboard_builder"
    path: "backend/app/skills/reporting/dashboard_builder/SKILL.md"
    yaml_path: "backend/app/skills/reporting/dashboard_builder/skill.yaml"
    version: "1.0.0"
    description: "Compose KPI/chart dashboards…"
    parent: "reporting"
    children: []
    sha_skill_md: "<git-blob-sha>"
    sha_skill_yaml: "<git-blob-sha>"
  # ...
```

### 4.5 Builders

Each builder is a callable returning a `list[dict[str, Any]]` ready to merge into the manifest, plus a `failures: list[str]` field for non-fatal issues.

#### `builders/skills.py`

```python
@dataclass(frozen=True)
class SkillEntry:
    id: str                          # dotted path
    path: str                        # rel SKILL.md path
    yaml_path: str | None            # rel skill.yaml path (None if absent)
    version: str                     # from frontmatter or "0.0.0"
    description: str
    parent: str | None
    children: list[str]
    sha_skill_md: str
    sha_skill_yaml: str | None

class SkillsBuilder:
    def __init__(self, skills_root: Path): ...
    def build(self) -> tuple[list[SkillEntry], list[str]]: ...
```

Walks `skills_root` recursively. For every directory containing `SKILL.md`:
- `id` = posix relative path from `skills_root`, slashes → dots, no `SKILL.md` suffix.
- Reads SKILL.md frontmatter via the same YAML parser used in `SkillRegistry._split_frontmatter`.
- Reads `skill.yaml` if present (sibling file).
- `parent` = parent dotted path or `None`; `children` = direct child skill ids.
- Hashes both files via `hashing.git_blob_sha(path)`.

Acceptance-gate parity: `len(skills) == len(SkillRegistry(skills_root)._index)` — proven by `test_skill_count_parity.py`.

#### `builders/scripts.py`

```python
@dataclass(frozen=True)
class ScriptEntry:
    id: str                          # rel posix path
    path: str
    interpreter: str                 # "python3" | "bash" | "node" | "unknown"
    sha: str

class ScriptsBuilder:
    def __init__(self, scripts_root: Path, gitignore: GitignoreMatcher): ...
    def build(self) -> tuple[list[ScriptEntry], list[str]]: ...
```

Glob `scripts_root/**/*.{py,sh,ts,js}` minus `.gitignore` matches.
Interpreter detection precedence:
1. First line shebang (`#!/usr/bin/env bash` → `bash`; `#!/usr/bin/env python3` → `python3`).
2. Extension fallback (`.py`→`python3`; `.sh`→`bash`; `.ts`/`.js`→`node`).
3. Otherwise `"unknown"` and a `failures.append("…")`.

#### `builders/routes.py`

```python
@dataclass(frozen=True)
class RouteEntry:
    id: str                          # graph node id, e.g. "route::POST::/api/trace"
    method: str
    path: str
    source_file: str | None
    source_location: int | None
    extractor: str

class RoutesBuilder:
    def __init__(self, graph: GraphSnapshot): ...
    def build(self) -> tuple[list[RouteEntry], list[str]]: ...
```

Iterates `graph.nodes` filtering `id.startswith("route::")`. If `graph` is empty (Plugin A never ran) → returns `[]` and adds a single `failures.append("graph.augmented.json absent — routes inventory is empty")`. Plugin still passes; consumers know.

#### `builders/configs.py`

```python
@dataclass(frozen=True)
class ConfigEntry:
    id: str                          # rel posix path
    type: str                        # "pyproject" | "package_json" | "claude_settings" | …
    path: str
    sha: str

class ConfigsBuilder:
    def __init__(self, repo_root: Path, globs: list[str], excluded: list[str], gitignore: GitignoreMatcher): ...
    def build(self) -> tuple[list[ConfigEntry], list[str]]: ...
```

Type detection table (extend in one place):

| Filename pattern | type |
|------------------|------|
| `pyproject.toml` | `pyproject` |
| `package.json` | `package_json` |
| `.claude/settings.json` | `claude_settings` |
| `config/integrity.yaml` | `integrity_yaml` |
| `vite.config.{ts,js,mjs}` | `vite_config` |
| `tsconfig*.json` | `tsconfig` |
| `Dockerfile*` | `dockerfile` |
| `Makefile` | `makefile` |
| `.env.example` | `env_example` |
| `infra/**/*.{yaml,yml}` | `infra_yaml` |
| `infra/**/*.tf` | `infra_terraform` |
| `*` (fallback under `config/**`) | `generic_config` |

Files not matching any pattern (and not under a config root) are skipped — we don't list random files. `.gitignore` matches and `excluded` globs are skipped.

#### `builders/functions.py`

```python
@dataclass(frozen=True)
class FunctionEntry:
    id: str                          # dotted path
    path: str
    line: int
    decorator: str                   # "router.post" | "app.on_event" | "app.get" | …
    target: str                      # the route path or event name

class FunctionsBuilder:
    def __init__(self, repo_root: Path, search_globs: list[str], decorators: list[str], event_handlers: list[str]): ...
    def build(self) -> tuple[list[FunctionEntry], list[str]]: ...
```

Walks `backend/app/api/**/*.py` (configurable). For each file, parses with `ast.parse` and visits `FunctionDef`/`AsyncFunctionDef`. For each decorator:
- `@router.<verb>("/path", …)` where `router` ∈ `decorators` → emits `FunctionEntry(decorator=f"{name}.{verb}", target=first_string_arg)`.
- `@app.on_event("startup"|"shutdown")` where `app` ∈ `decorators` → emits with `decorator="app.on_event"`, `target=event_name`.
- `@asynccontextmanager` on a function named in `event_handlers` (e.g. `lifespan`) → emits with `decorator="lifespan"`, `target="<function_name>"`.

`id` = full module dotted path + `.<func_name>` (e.g. `backend.app.api.chat_api.trace_endpoint`). Robust to import errors — uses AST, never imports the module.

### 4.6 Manifest writer (`manifest.py`)

```python
def read_manifest(path: Path) -> dict[str, Any]:
    """Returns empty manifest dict if path absent."""

def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    """Deterministic YAML emit: sorted top-level keys, sorted entries by id, block style,
    no anchors/aliases, double-quoted strings for safety. Writes a fixed header comment."""
```

Determinism guarantees:
- Top-level keys emitted in fixed order: `generated_at, generator_version, manifest_version, configs, functions, routes, scripts, skills`.
- Within each list, entries sorted by `id` (lexicographic ASCII).
- Strings always double-quoted; integers bare; null → `null`.
- LF line endings; trailing newline.
- Idempotent: `write_manifest(p, read_manifest(p))` is a no-op (`test_manifest_roundtrip.py` proves this).

`generated_at` is excluded from idempotency comparison — see §4.7.

### 4.7 Diff semantics

Diff compares **the entry sets** (id-keyed) between current and prior, ignoring `generated_at` (which always changes).

```python
def diff_manifests(current: dict, prior: dict) -> ManifestDelta:
    """Returns ManifestDelta(added, removed, changed) per top-level key.
    `changed` = same id, different content (e.g. sha bump)."""
```

`added.py` rule iterates `delta.added` per key → emits `IntegrityIssue(rule="config.added", severity="INFO")`.
`removed.py` rule iterates `delta.removed` → INFO, escalates to WARN if id appears in `cfg["_dep_graph"]` (any node id or `source_file` value). The dep-graph index is built once per scan from `ctx.graph`.
`schema_drift.py` runs the per-type schema validator on every config in `current.configs`, regardless of diff state — drift can be silent without an add/remove.

### 4.8 Schema validators

Each schema module exports:

```python
class SchemaValidator(Protocol):
    type_name: str                                            # e.g. "pyproject"
    def validate(self, path: Path, content: str) -> list[ValidationFailure]: ...

@dataclass(frozen=True)
class ValidationFailure:
    rule: str                                                 # short id, e.g. "missing_field"
    location: str                                             # e.g. "[project].name"
    message: str
```

Per-type validators (each file ≤ 200 LOC, focused):

| Module | Validates |
|--------|-----------|
| `pyproject.py` | TOML parses; `[project]` table present; `[project].name` and `version` set; `[project.optional-dependencies]` shape if present |
| `package_json.py` | JSON parses; `name` + `version` set; `scripts` is object; `dependencies`/`devDependencies` are objects |
| `claude_settings.py` | JSON parses; top-level `hooks` (if present) maps to list-of-objects with `matcher`/`command` |
| `integrity_yaml.py` | YAML parses; `plugins` is mapping; each entry has `enabled: bool` |
| `makefile.py` | `.PHONY` line covers all top-level targets that don't produce a file; targets are kebab-case |
| `dockerfile.py` | First non-comment line is `FROM`; multi-stage `AS` names referenced in later `COPY --from=<name>` exist |
| `env_example.py` | Every non-comment line matches `KEY=value` (value may be empty); KEY is `[A-Z_][A-Z0-9_]*` |
| `vite_config.py` | File loads as Python text (we don't exec); contains `export default` |
| `tsconfig.py` | JSON-with-comments parses; `compilerOptions` present; `extends` (if present) points to existing file |

Schemas registry (`schemas/__init__.py`):

```python
SCHEMA_REGISTRY: dict[str, SchemaValidator] = {
    "pyproject": PyprojectSchema(),
    "package_json": PackageJsonSchema(),
    "claude_settings": ClaudeSettingsSchema(),
    "integrity_yaml": IntegrityYamlSchema(),
    "makefile": MakefileSchema(),
    "dockerfile": DockerfileSchema(),
    "env_example": EnvExampleSchema(),
    "vite_config": ViteConfigSchema(),
    "tsconfig": TsconfigSchema(),
}
```

Configs whose `type` has no entry are skipped (no false positives for new types).

### 4.9 Reuse from existing engine

| Component | Reused from |
|-----------|-------------|
| `IntegrityIssue`, `carry_first_seen` | `backend/app/integrity/issue.py` |
| `ScanContext`, `ScanResult`, `IntegrityPlugin` protocol | `backend/app/integrity/protocol.py` |
| `GraphSnapshot.load(repo_root)` | `backend/app/integrity/schema.py` |
| Engine, snapshots, report aggregator (report.json, report.md, docs/health/latest.md, trend.md append) | `backend/app/integrity/{engine,snapshots,report}.py` |
| `python -m backend.app.integrity` CLI | `backend/app/integrity/__main__.py` (extend `KNOWN_PLUGINS` to include `config_registry`) |
| Frontend Health page | already renders `docs/health/latest.md` — no changes needed |
| Per-rule try/except pattern | `backend/app/integrity/plugins/{graph_lint,doc_audit}/plugin.py` (mirror) |
| Skill dotted-path conventions | `backend/app/skills/registry.py` (`_index` keys are the parity target) |

## 5. Configuration

Append to `config/integrity.yaml`:

```yaml
plugins:
  config_registry:
    enabled: true
    manifest_path: "config/manifest.yaml"
    skills_root: "backend/app/skills"
    scripts_root: "scripts"
    config_globs:
      - "pyproject.toml"
      - "package.json"
      - ".claude/settings.json"
      - "vite.config.*"
      - "tsconfig*.json"
      - "Dockerfile*"
      - "Makefile"
      - ".env.example"
      - "infra/**/*.yaml"
      - "infra/**/*.yml"
      - "infra/**/*.tf"
      - "config/integrity.yaml"
    excluded_paths:
      - "node_modules/**"
      - "**/__pycache__/**"
      - "integrity-out/**"
      - "build/**"
      - "dist/**"
    function_search_globs:
      - "backend/app/api/**/*.py"
      - "backend/app/main.py"
    function_decorators:
      - "router"
      - "app"
      - "api_router"
    function_event_handlers:
      - "startup"
      - "shutdown"
      - "lifespan"
    schema_drift:
      enabled: true
      strict_mode: false       # false = unknown types skip; true = unknown type → WARN
    removed_escalation:
      enabled: true            # WARN if removed id still in dep graph
    disabled_rules: []
```

Engine wiring (`backend/app/integrity/engine.py`): register `ConfigRegistryPlugin` with config from `integrity.yaml`. Topological order: A, B, C, E (E depends on graph but not formally on Plugin A — engine runs E after A completes when both are enabled, but E's `depends_on=()` so it can also run standalone).

## 6. Data flow

```
nightly cron / manual / hook
        ↓
IntegrityEngine.discover()         (loads enabled plugins from config)
        ↓
topo run order: A → {B, C, E}      (B, C, E independent; E reads A's output if present)
        ↓
ConfigRegistryPlugin.scan(ctx)
  ├── builders/skills.py   → SkillEntry list
  ├── builders/scripts.py  → ScriptEntry list
  ├── builders/routes.py   → RouteEntry list (from ctx.graph)
  ├── builders/configs.py  → ConfigEntry list
  ├── builders/functions.py→ FunctionEntry list
  ├── manifest.read_manifest(config/manifest.yaml)  → prior
  ├── manifest.write_manifest(config/manifest.yaml, current)  → on-disk source of truth
  ├── rules/added.py        (current vs prior delta → INFO issues)
  ├── rules/removed.py      (current vs prior delta → INFO/WARN issues)
  └── rules/schema_drift.py (per-type validation → WARN issues)
        ↓
write integrity-out/{ISO-date}/config_registry.json
        ↓
report.py aggregator (already shipped) merges A + B + C + E → report.json + report.md
        ↓
docs/health/latest.md updated (committed; same as gate β/γ)
docs/health/trend.md appended (rolling 30 days)
        ↓
frontend Health page picks up new content (no code change)
```

Plugin E **writes** `config/manifest.yaml` to disk. This is intentional: the manifest is committed and is the source of truth. The integrity-out artifact is the journal.

## 7. CLI / Make targets

- New: `make integrity-config` — runs `python -m backend.app.integrity --plugin config_registry`. Acceptance gate target.
- Modified: `make integrity` — already topologically dispatches all enabled plugins; no change beyond engine registration.
- Modified Make help text for `integrity` to read `Run the full integrity pipeline (A→B→C→E)`.
- Modified: `python -m backend.app.integrity --plugin config_registry` becomes a valid invocation (`KNOWN_PLUGINS` extended).
- New optional flag: `python -m backend.app.integrity --plugin config_registry --check` — dry-run that does not write `config/manifest.yaml`; exits non-zero if a write would have changed it. Useful in CI to fail PRs that forgot to regenerate the manifest.

## 8. Error handling

Per parent §8 + Plugin B/C pattern:
- Per-rule exception caught in `ConfigRegistryPlugin.scan` → `IntegrityIssue(severity="ERROR")` + `failures.append(...)`. Other rules continue.
- Per-builder exception caught at the plugin level → builder's section in current manifest = `[]` plus a failure entry. Other builders proceed; rules see partial manifest. Acceptance gate explicitly requires no builder failures on the real repo.
- Plugin-wide failure (PyYAML import error, malformed `integrity.yaml`) → engine catches at top level → plugin marked `failed`, siblings continue.
- Repo without `graphify/graph.augmented.json` (Plugin A never ran) → `routes` builder returns `[]` and logs failure entry. `removed_escalation` falls back to INFO-only (no graph means no references to check). Other rules unaffected.
- Repo without `config/manifest.yaml` (first run) → prior is empty dict. `config.added` will fire for everything; this is **expected** on first-ever run and not gate-blocking. Gate δ requires the count to settle to 0/0 after the first commit.
- Repo without git history (CI shallow clone) → `git_blob_sha` falls back to in-process Python implementation (`hashlib.sha1` over the same `blob {len}\0{content}` framing). Identical SHAs guaranteed.

## 9. Testing

Per parent §9 — every rule + every builder + every schema validator gets ≥1 positive + 1 negative test. Plus two acceptance-gate proof tests.

### 9.1 Synthetic `tiny_repo` fixture

Built once via `conftest.py`. Mirrors the real repo's shape minimally; about 25 files. See file layout in §4.1 under `tests/fixtures/tiny_repo/`. Fixture builder uses `pytest.tmp_path` with `git init` + initial commit so `git_blob_sha` works without falling back.

### 9.2 Per-builder + per-rule + per-schema tests

| Test file | Cases |
|-----------|-------|
| `test_hashing.py` | (+) `git_blob_sha("foo.txt")` matches `git hash-object foo.txt`. (+) Empty file SHA matches the well-known empty blob SHA. (+) Falls back to in-process when `.git` absent and still matches. |
| `test_manifest_roundtrip.py` | (+) `read(write(m)) == m` (excluding `generated_at`). (+) `write` is deterministic — same input → byte-identical output. (+) Sorting honoured (configs sorted by id). |
| `test_builder_skills.py` | (+) Builds 3 entries against `tiny_repo` (`alpha`, `beta`, `beta.sub_skill`). (+) `parent`/`children` populated correctly. (+) Skill without `skill.yaml` → `yaml_path: None`, `sha_skill_yaml: None`. (–) Empty `skills_root` → `[]`. |
| `test_builder_scripts.py` | (+) `deploy.sh` → bash. (+) `gen_data.py` → python3. (+) `build.ts` → node. (+) Shebang overrides extension. (–) Unknown extension without shebang → `"unknown"` + failure entry. |
| `test_builder_routes.py` | (+) Re-export from `tiny_repo/graphify/graph.augmented.json` produces 2 routes (matches fixture). (–) Absent graph → `[]` + failure. |
| `test_builder_configs.py` | (+) Detects pyproject, package.json, claude_settings, integrity_yaml, vite_config, tsconfig, dockerfile, makefile, env_example. (+) `.gitignore` match skipped. (+) Excluded glob skipped. (–) Random text file under repo root → not listed. |
| `test_builder_functions.py` | (+) `@router.get("/foo")` → 1 entry with `decorator="router.get"`, `target="/foo"`. (+) `@app.on_event("startup")` → 1 entry. (+) `@asynccontextmanager` named `lifespan` → 1 entry. (–) Plain undecorated function → not listed. (–) Module with syntax error → builder skips file + adds failure entry. |
| `test_rule_added.py` | (+) Add a script → `config.added` issue with `node_id="scripts/<id>"`, `severity="INFO"`. (–) No diff → 0 issues. |
| `test_rule_removed.py` | (+) Remove a config → `config.removed` INFO. (+) Removed id appears in graph node id → escalated to WARN. (–) Removed id not in graph → INFO. |
| `test_rule_schema_drift.py` | (+) Inject `pyproject.toml` missing `[project].version` → `config.schema_drift` WARN with `evidence["validation_failures"]` populated. (–) Valid pyproject → 0 issues. |
| `test_schemas_pyproject.py` | (+) Valid file → no failures. (–) Missing `[project]` → 1 failure. (–) Missing `name`/`version` → failure each. |
| `test_schemas_package_json.py` | (+) Valid. (–) Missing `name`. (–) `scripts` is array not object. |
| `test_schemas_claude_settings.py` | (+) Valid. (–) `hooks` malformed. (+) Missing `hooks` (optional) → no failure. |
| `test_schemas_integrity_yaml.py` | (+) Valid. (–) `plugins` not mapping → failure. (–) Plugin entry without `enabled` → failure. |
| `test_schemas_makefile.py` | (+) Valid. (–) Phony target missing from `.PHONY`. (–) `CamelCase` target. |
| `test_schemas_dockerfile.py` | (+) Valid. (–) Missing `FROM`. (–) `COPY --from=missing` references undeclared stage. |
| `test_schemas_env_example.py` | (+) Valid. (–) Lowercase key. (–) Line missing `=`. |
| `test_schemas_vite_config.py` | (+) Has `export default`. (–) Missing `export default`. |
| `test_schemas_tsconfig.py` | (+) Valid. (–) `compilerOptions` absent. (–) `extends` points to non-existent file. |
| `test_skill_count_parity.py` | **Acceptance proof**: build a real `SkillRegistry(repo_root="backend/app/skills")` and a `SkillsBuilder` over the same dir; assert `len(skills) == len(registry._index)` and id sets match exactly. Run against the **real** repo's `backend/app/skills/`, not a fixture. |
| `test_round_trip_add_fixture.py` | **Acceptance proof**: write a new fixture config (`tests/fixtures/scratch.yaml`) into `tiny_repo`, scan, assert `config.added` fires with the new id; remove it, scan, assert `config.removed` fires. |
| `test_plugin_integration.py` | Full plugin scan against `tiny_repo`: asserts exact issue counts per rule and `config_registry.json` artifact written with builders' `failures` aggregated. |

### 9.3 Smoke against real repo

- Plugin runs against `claude-code-agent` in CI's `make integrity` step → exit 0, no exceptions.
- `make integrity-config` produces `config/manifest.yaml` whose **diff vs HEAD** is reviewed; the manifest is committed manually after the first generation (then nightly runs only commit when content actually changes — the writer is idempotent).
- Manual gate verification:
  ```
  make integrity-config
  cat integrity-out/$(date +%F)/config_registry.json | jq '.rules_run, (.issues | length)'
  python -c "from backend.app.skills.registry import SkillRegistry; from pathlib import Path; \
             import yaml; m = yaml.safe_load(open('config/manifest.yaml')); \
             r = SkillRegistry(Path('backend/app/skills')); \
             assert len(m['skills']) == len(r._index), (len(m['skills']), len(r._index))"
  ```

## 10. Acceptance gate δ (per parent §7)

Pass condition (must hold for **7 consecutive nightly runs** to close gate δ):

1. ✅ `make integrity-config` exits 0 on the real repo.
2. ✅ Manifest covers every skill: `len(manifest.skills) == len(SkillRegistry._index)` against the live registry; id sets equal. Verified by `test_skill_count_parity.py` running against the real `backend/app/skills/`.
3. ✅ Manifest covers every script under `scripts/**`: `set(manifest.scripts.id) == set(rel(p) for p in glob('scripts/**/*.{py,sh,ts,js}') if not gitignored)`.
4. ✅ Manifest covers every route in `graph.augmented.json` (when present): `set(manifest.routes.id) == set(n.id for n in graph if n.id.startswith('route::'))`.
5. ✅ Manifest covers every well-known config type: every file matching `config_globs` is listed (verified by builder + smoke test).
6. ✅ Round-trip: add a test-fixture config to the repo, run `make integrity-config`, observe `config.added` issue with the new file's id (proven by `test_round_trip_add_fixture.py`).
7. ✅ `pytest backend/app/integrity/plugins/config_registry/` green (all builder + rule + schema + integration + parity + round-trip tests).
8. ✅ Plugin E results visible in `docs/health/latest.md` (renders via aggregator).
9. ✅ `python -m backend.app.integrity --plugin config_registry --check` exits 0 in CI on `main` (no uncommitted manifest drift).

INFO-severity issues (`config.added` for legitimate new entries) do not block the gate after the manifest is committed.

## 11. Operational defaults

| Setting | Default | Where to change |
|---------|---------|-----------------|
| Manifest path | `config/manifest.yaml` | `config/integrity.yaml: plugins.config_registry.manifest_path` |
| Skills root | `backend/app/skills` | `config/integrity.yaml: plugins.config_registry.skills_root` |
| Scripts root | `scripts` | `config/integrity.yaml: plugins.config_registry.scripts_root` |
| Config globs | 12 entries (pyproject, package.json, claude/settings.json, …) | `config/integrity.yaml: plugins.config_registry.config_globs` |
| Function search globs | `backend/app/api/**/*.py`, `backend/app/main.py` | `config/integrity.yaml: plugins.config_registry.function_search_globs` |
| Function decorators | `["router", "app", "api_router"]` | `config/integrity.yaml: plugins.config_registry.function_decorators` |
| Excluded paths | `node_modules`, `__pycache__`, `integrity-out`, `build`, `dist` | `config/integrity.yaml: plugins.config_registry.excluded_paths` |
| Schema drift mode | `strict_mode: false` (unknown types skip) | `config/integrity.yaml: plugins.config_registry.schema_drift.strict_mode` |
| Removed escalation | `enabled: true` | `config/integrity.yaml: plugins.config_registry.removed_escalation.enabled` |

## 12. Open knobs (deferred — record decisions when raised)

- **Frontend route extraction**: Should `frontend/src/**/*.tsx` router declarations be inventoried? Default no; revisit when the SPA gets a router with file-based routes (e.g. TanStack Router).
- **Manifest in two files**: Should we split per-domain (`config/manifest.skills.yaml`, `config/manifest.routes.yaml`, …)? Default no — one file is one diff. Revisit if the file exceeds ~2k lines.
- **Schema autogeneration**: Should we auto-generate JSON Schema files from the per-type validators? Out of scope for δ; could ship in E.1 if external tooling needs them.
- **Symlink handling**: Currently followed by `pathlib.Path.glob`. If symlinks become a vector for surprising entries, switch to `os.walk(followlinks=False)`. Not a concern today.
- **Per-skill schema versioning**: SkillRegistry today doesn't enforce a `version` in SKILL.md frontmatter. We capture whatever is there (or `"0.0.0"`). A future ADR could mandate semver.
- **Renamed-entry detection**: Today, `id` change → one `config.removed` + one `config.added`. We could detect rename via content-sha equality (same sha, new id) and emit a single `config.renamed`. Out of scope for δ; revisit if the noise becomes meaningful.

## 13. Dependencies

- New: `tomli >= 2.0` (Python ≤ 3.10 only — Python 3.11+ has `tomllib` in stdlib; we already require 3.12 per CLAUDE.md so this is conditional and likely unused).
- Reused: `PyYAML` (already in backend), `IntegrityIssue`, engine, report, snapshots — no new deps.
- AST parsing uses stdlib `ast`. Hashing uses stdlib `hashlib`.
- Frontend: none.

## 14. Migration / rollout

1. Land Plugin E with `enabled: true` in `config/integrity.yaml`.
2. First `make integrity-config` after merge generates `config/manifest.yaml` for the first time. Review the diff, commit.
3. Subsequent runs are idempotent unless a real change occurred.
4. CI gate: add `--check` invocation to PR pipeline — fails PRs that touched files in `paths` without re-running the manifest. (Optional; recommended after one settling cycle.)
5. Once gate criteria hold for 7 consecutive nightly runs → mark this spec `Status: shipped` and close gate δ in parent spec front matter.

## 15. Spec lifecycle

Per parent §10:
- This sub-spec is the source of truth for Plugin E.
- Edit in place; bump `last_revised`.
- On gate δ closure (7 green nightly runs): set `status: shipped` here.
- On deprecation: set `status: deprecated` with `replaced_by:` pointer; keep file.

## 16. References

- Parent: `docs/superpowers/specs/2026-04-16-integrity-system-design.md` (mega-spec, §5.4 / §7 / §8 / §9)
- Plugin A spec: `docs/superpowers/specs/2026-04-16-integrity-plugin-a-design.md` (gate α — provides graph + route extractor)
- Plugin B spec: `docs/superpowers/specs/2026-04-17-integrity-plugin-b-design.md` (gate β — provides engine + aggregator)
- Plugin C spec: `docs/superpowers/specs/2026-04-17-integrity-plugin-c-design.md` (gate γ — pattern reference for plugin shape, per-rule try/except, fixture style)
- `SkillRegistry` source: `backend/app/skills/registry.py` (parity target for skill inventory)
- Sample skill.yaml: `backend/app/skills/reporting/dashboard_builder/skill.yaml`
- Sample route node: `graphify/graph.augmented.json` — `{id: "route::POST::/api/trace", extractor: "fastapi_routes", source_file: "backend/app/api/chat_api.py", source_location: 1173}`
- Plugin B implementation reference: `backend/app/integrity/plugins/graph_lint/` (mirror plugin shape)
- Plugin C implementation reference: `backend/app/integrity/plugins/doc_audit/` (mirror per-rule try/except + tiny_repo fixture style)
