---
title: Integrity Plugin F (autofix) — gate ζ
status: design-approved
created: 2026-04-17
last_revised: 2026-04-17
owner: jay
parent_spec: 2026-04-16-integrity-system-design.md
gate: ζ
depends_on:
  - 2026-04-17-integrity-plugin-b-design.md   # gate β — graph_lint (provides dead-directive signal)
  - 2026-04-17-integrity-plugin-c-design.md   # gate γ — doc_audit (provides claude_md_link, doc_link_renamed sources)
  - 2026-04-17-integrity-plugin-e-design.md   # gate δ — config_registry (provides manifest_regen source)
---

# Plugin F — `autofix`

> Sub-spec for gate ζ of the integrity system. Parent: `2026-04-16-integrity-system-design.md` §5.6. Single source of truth for Plugin F scope, design, and acceptance criteria. Edit in place; bump `last_revised`. This is the **terminal plugin** — the integrity roadmap is complete after gate ζ.

## 1. Goal

Convert mechanical integrity drift into reviewable PRs without ever touching code logic.

Plugin F reads sibling plugin artifacts under `integrity-out/{date}/` and emits a *diff plan* — one PR per whitelisted fix class — covering five mechanical drift categories:

- `claude_md_link` — append CLAUDE.md index entry for an unindexed doc (source: `doc.unindexed`)
- `doc_link_renamed` — rewrite a broken link target whose unique rename is provable from `git log --diff-filter=R --follow` (source: `doc.broken_link`)
- `manifest_regen` — regenerate `config/manifest.yaml` when the inventory drifts (source: `config.added`/`config.removed`)
- `dead_directive_cleanup` — remove `# noqa: <code>` / `// eslint-disable-next-line <rule>` comments whose underlying lint warning no longer triggers (driven by lint output, not a single rule)
- `health_dashboard_refresh` — regenerate `docs/health/latest.md` + `docs/health/trend.md` from the day's report (driven by aggregator output)

Two operating modes:

- `--dry-run` (default) — write `integrity-out/{date}/autofix.json` with the proposed diffs + PR metadata. Zero git side effects. Safe for nightly runs.
- `--apply` — run the dispatcher: per fix class, branch off `main`, apply diffs, commit, push, open or update one PR. Gated by `--apply` CLI flag *and* `autofix.apply: true` in `config/integrity.yaml` (both required, defense in depth).

Acceptance gate ζ requires every fix class to produce a valid dry-run diff for the real repo's current state (or a representative synthetic fixture if no real issue exists for that class right now), `make integrity-autofix` to exit 0, and the full `make integrity` pipeline to remain green.

All execution builds on the engine, snapshots, and aggregator shipped at gates β/γ/δ/ε. Plugin F shares Plugin D/E's plugin/builder layering verbatim.

## 2. Non-goals

- **Code logic changes.** Anything that touches a function body, a conditional, an import semantics — not in scope. Forever.
- **File deletion.** No fix class deletes files. Removal is always a human decision.
- **Auto-merge.** Plugin F opens PRs; review and merge stay human.
- **Direct commits to main.** Hard rule. Branches are mandatory.
- **Hand-edited `config/manifest.yaml` patches.** `manifest_regen` regenerates the whole file via Plugin E's emitter; partial diffs would diverge.
- **PR description prose generation.** Body is a structured list of issue evidence — no LLM authoring.
- **Cross-repo PRs.** Single repository only.
- **Auto-rollback.** If a PR turns out wrong, the human reverts. The circuit breaker disables the *class*, not individual PRs.
- **Per-issue PRs.** Concurrency is per-class, capped at one open PR. Bundling reduces review noise and matches the parent spec's "one PR per fix class" rule.

## 3. Decisions locked from brainstorm

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Default mode | `--dry-run` | Safe by default; nightly cron runs dry; CI promotes to `--apply` only when explicit |
| Apply gate | `--apply` flag AND `autofix.apply: true` config | Two independent kill switches; either off = dry-run |
| Sibling-data sourcing | Reads `integrity-out/{date}/{plugin}.json`; never re-scans | Idempotent; trivial test fixtures; no upstream coupling |
| Missing upstream artifact | Skip the dependent fix class with INFO note; siblings continue | Plugin F never crashes on partial data |
| Upstream plugin failure | Skip *all* fix classes; emit one INFO `autofix.skipped_upstream_failure` issue | "Don't act on a partial picture" — parent spec hard rule |
| Branch naming | `integrity/autofix/<fix_class>/<YYYY-MM-DD>` | Date-stamped; one per class per day; greppable in `gh pr list` |
| PR title | `chore(integrity): <fix_class>` | Predictable; conventional commits compatible |
| PR body shape | Structured: `## Issues fixed` (list with rule + evidence), `## Diffs` (file table), `## How to verify` (per-class commands) | Reviewer scans evidence, runs verification, merges |
| PR concurrency per class | 1 open PR max; if exists, fetch its branch, replay diffs, force-push (with-lease), update body | Avoids duplicate-PR storm; idempotent re-runs |
| `gh` invocation | Subprocess; `gh` must be on PATH; auth via existing token (no plugin-managed secrets) | Reuses developer's auth; no new secret surface |
| Apply requires clean tree | `git status --porcelain` empty; otherwise abort with ERROR | Refuses to mix autofix changes with in-progress work |
| Apply refuses on main | `git rev-parse --abbrev-ref HEAD == "main"` triggers branch creation; never edits main directly | Belt-and-braces; hard rule from parent spec |
| Diff representation | `Diff(path, original_content, new_content, rationale, source_issues)` — full-file replacement | Trivial to apply (`Path.write_text`); trivial to diff in PR; no merge conflicts |
| `original_content` snapshot timing | Captured at propose-time; if file changed between propose and apply, abort that fix class with `apply.stale_diff` ERROR | Catch concurrent edits; never overwrite human work |
| Empty diff plan | `manifest_regen` skipped if regenerated file is byte-identical to current; same for `health_dashboard_refresh` | Don't open empty PRs |
| Circuit breaker storage | `config/autofix_state.yaml` (committed); per-class rolling 30-day counters of `merged_clean` / `human_edited` | Diffable; survives runs; visible in PR review |
| Circuit breaker trigger | `human_edited > 2` in last 30 days → set `enabled: false` in `config/integrity.yaml` for that class + open INFO issue | Auto-disable bad classes; human re-enables once root cause fixed |
| Circuit breaker bookkeeping | Updated by a separate `sync` subcommand (`make integrity-autofix-sync`) that diffs merged PRs vs originally-proposed diffs | Decoupled from scan; safe to fail independently |
| Dispatcher subprocess timeout | 60s per `git`/`gh` call | Bounds blast radius if `gh` hangs |
| Apply error policy | Per-class try/except; one failing class doesn't abort siblings | Mirrors per-rule pattern from D/E |
| Plugin `depends_on` | `("graph_lint", "doc_audit", "config_registry")` — soft deps via `dataclasses.replace` for `--plugin autofix` | Standalone-runnable; respects topo order in full pipeline |
| Plugin output artifact | `integrity-out/{date}/autofix.json` | Mirrors Plugin B/C/D/E pattern |
| Makefile targets | `integrity-autofix` (dry-run), `integrity-autofix-apply` (apply), `integrity-autofix-sync` (circuit breaker bookkeeping) | Three explicit verbs; the dangerous one is last and explicitly named |
| `config/integrity.yaml` block | `autofix: { enabled, apply, fix_classes, pr_concurrency_per_class, circuit_breaker, gh_executable }` | All knobs explicit; matches Plugin D/E config style |
| Frontend integration | New "Autofix" tile in Health section showing per-class state (open PR / disabled / clean) | Read-only; mutations stay CLI-driven |

## 4. Architecture

### 4.1 File layout

```
backend/app/integrity/plugins/autofix/
  __init__.py
  plugin.py                            # AutofixPlugin (mirrors HooksCheckPlugin shape)
  diff.py                              # Diff dataclass + apply helpers
  loader.py                            # read sibling artifacts from integrity-out/{date}/
  fixers/
    __init__.py                        # FIXER_REGISTRY — name → propose callable
    claude_md_link.py                  # propose(issues, repo_root) -> list[Diff]
    doc_link_renamed.py                # uses git log --diff-filter=R --follow
    manifest_regen.py                  # invokes config_registry's emitter
    dead_directive_cleanup.py          # parses lint output → strips dead noqa/eslint-disable
    health_dashboard_refresh.py        # rebuilds docs/health/{latest,trend}.md
  pr_dispatcher.py                     # apply diffs + git/gh subprocess orchestration
  safety.py                            # preflight checks (clean tree, not main, upstream green, gh available)
  circuit_breaker.py                   # load/update config/autofix_state.yaml, decide enabled
  schemas/
    __init__.py
    autofix_state.py                   # AutofixStateValidator — shape-checks autofix_state.yaml
  fixtures/                            # synthetic upstream artifacts for tests
    doc_audit_unindexed.json
    doc_audit_broken_link.json
    config_registry_drift.json
    graph_lint_dead_directive.json
    report_aggregate.json
  tests/
    __init__.py
    conftest.py                        # tiny_repo_with_artifacts fixture (synthetic integrity-out/)
    test_loader.py                     # read sibling artifacts; missing file → INFO + skip
    test_diff.py                       # apply_diff round-trip; stale_diff detection
    test_fixer_claude_md_link.py       # +/− pair
    test_fixer_doc_link_renamed.py     # +/− pair (mock git log)
    test_fixer_manifest_regen.py       # +/− pair (skipped when byte-identical)
    test_fixer_dead_directive_cleanup.py  # +/− pair
    test_fixer_health_dashboard_refresh.py  # +/− pair
    test_pr_dispatcher.py              # mock subprocess; verifies branch/commit/gh-pr-create command shape
    test_pr_dispatcher_update.py       # existing PR detected → force-push-with-lease + body update
    test_safety.py                     # dirty tree refused; on main refused; upstream-failure refused; missing gh refused
    test_circuit_breaker.py            # 3-strike disable; auto-recovery on counter reset
    test_plugin_integration.py         # full scan against tiny_repo with exact diff counts
    test_acceptance_gate.py            # 5-fixer fixture → 5 dry-run diffs; no git side effects
```

### 4.2 Plugin shape

```python
@dataclass
class AutofixPlugin:
    name: str = "autofix"
    version: str = "1.0.0"
    depends_on: tuple[str, ...] = ("graph_lint", "doc_audit", "config_registry")
    paths: tuple[str, ...] = (
        "config/integrity.yaml",
        "config/autofix_state.yaml",
    )
    config: dict[str, Any] = field(default_factory=dict)
    today: date = field(default_factory=date.today)
    apply: bool = False                # CLI --apply flag; AND-gated with config.apply
    fixers: dict[str, Fixer] | None = None

    def scan(self, ctx: ScanContext) -> ScanResult:
        # 1. Safety preflight (upstream artifacts present, clean tree if apply, not main if apply, gh available if apply).
        #    Any failure → emit INFO/ERROR issue, return early with no diffs.
        # 2. Load sibling artifacts via loader.read_today(integrity_out_root, today).
        # 3. Load circuit breaker state; mask out disabled fix classes.
        # 4. Per fix class: try/except → fixer.propose(issues, repo_root) → list[Diff].
        # 5. Skip empty diff plans.
        # 6. If apply: pr_dispatcher.run(diffs_by_class).
        # 7. Write integrity-out/{date}/autofix.json (always — dry-run or apply).
        # 8. Emit one INFO issue per produced (or skipped) class for visibility.
```

`config` keys (read from `config/integrity.yaml::plugins.autofix`):

| Key | Default | Purpose |
|-----|---------|---------|
| `enabled` | `true` | Master switch |
| `apply` | `false` | When false, dry-run regardless of CLI flag |
| `fix_classes` | all five enabled | Per-class enable/disable (`{claude_md_link: {enabled: true}, ...}`) |
| `pr_concurrency_per_class` | `1` | Max simultaneously-open PRs per class |
| `gh_executable` | `"gh"` | Path to `gh`; preserved for hermetic CI |
| `circuit_breaker.window_days` | `30` | Rolling window for human-edit counter |
| `circuit_breaker.max_human_edits` | `2` | Threshold past which a class auto-disables |
| `branch_prefix` | `"integrity/autofix"` | Composable for forks/test repos |
| `commit_author` | `"Integrity Autofix <integrity@local>"` | Local commit identity for autofix branches |
| `dispatcher_subprocess_timeout_seconds` | `60` | Per `git`/`gh` invocation cap |

### 4.3 Diff dataclass

```python
@dataclass(frozen=True)
class IssueRef:
    plugin: str
    rule: str
    message: str
    evidence: dict[str, Any]

@dataclass(frozen=True)
class Diff:
    path: Path                       # repo-relative
    original_content: str            # snapshot at propose-time; "" if creating new file
    new_content: str                 # full target content
    rationale: str                   # one-sentence explanation for PR body
    source_issues: tuple[IssueRef, ...]  # the integrity issues this diff resolves

    def is_noop(self) -> bool:
        return self.original_content == self.new_content

    def stale_against(self, repo_root: Path) -> bool:
        """True if `path` on disk no longer matches `original_content`. Apply must abort."""
```

`Diff` is full-file replacement — not unified-diff hunks. Rationale: every fix class regenerates a small file (CLAUDE.md, manifest.yaml, latest.md) or makes a localized edit on a single file. Full-content snapshots make staleness detection trivial (`current_text != original_content`).

### 4.4 Loader

```python
@dataclass(frozen=True)
class SiblingArtifacts:
    doc_audit: dict[str, Any] | None
    config_registry: dict[str, Any] | None
    graph_lint: dict[str, Any] | None
    aggregate: dict[str, Any] | None     # report.json — drives health_dashboard_refresh
    failures: dict[str, str]             # plugin name → "missing" | "parse_error: <msg>"

def read_today(integrity_out: Path, today: date) -> SiblingArtifacts: ...
```

A missing artifact is **not** an error — the dependent fix class is skipped with INFO. A *parse error* on a present artifact **is** an error — emits ERROR-severity `autofix.upstream_parse_error`.

### 4.5 Fixer protocol

```python
class Fixer(Protocol):
    name: str
    sources: tuple[str, ...]            # which sibling plugins it consumes ("doc_audit", ...)
    def propose(self, artifacts: SiblingArtifacts, repo_root: Path) -> list[Diff]: ...
```

Fixers are **pure** — no I/O beyond `repo_root` reads. They never invoke git, never run subprocesses (except `manifest_regen` which delegates to Plugin E's existing emitter, and `doc_link_renamed` which calls `git log` read-only). They never write files. The dispatcher does the writing.

### 4.6 Per-class fixer behavior

#### `claude_md_link`

1. Read `doc.unindexed` issues from `doc_audit.json`. Each issue's evidence has `path: docs/foo/bar.md`.
2. Compute the title: first H1 of the doc, or filename-titlecase fallback.
3. Determine the section to insert into: read CLAUDE.md, find the section whose existing entries share the deepest common prefix with the new doc's path. Default fallback: append to the last `## Deeper Context` list (or whichever section is configured under `claude_md_link.target_section`).
4. Emit one Diff for CLAUDE.md with the appended bullet — alphabetically inserted within the section, dedup-checked.
5. Bundle multiple unindexed docs into a *single* Diff for CLAUDE.md.

#### `doc_link_renamed`

1. Read `doc.broken_link` issues from `doc_audit.json`. Each evidence: `source: docs/a.md`, `link_target: docs/old/path.md`.
2. For each broken target, run `git log --diff-filter=R --follow --format=%H -- <link_target>` (read-only). If the rename is unambiguous (single rename event in last 365 days, single new path), record the new path.
3. Group by source file. For each source, emit one Diff with all link targets rewritten in a single full-file replacement.
4. Skip ambiguous renames (multiple candidates, no rename history) with `autofix.skipped_ambiguous_rename` INFO.

#### `manifest_regen`

1. Read `config.added` / `config.removed` issues from `config_registry.json`.
2. Invoke Plugin E's existing emitter (`backend.app.integrity.plugins.config_registry.emitter.emit_manifest`) to produce the regenerated content.
3. Compare to current `config/manifest.yaml` byte-for-byte. If identical → no diff (Plugin E already in sync). Otherwise → one Diff replacing the file.
4. No partial edits. Manifest is regenerated whole or not at all.

#### `dead_directive_cleanup`

1. Read `graph_lint.json` for each issue's evidence containing a `directive` field (a `# noqa: <code>` or `// eslint-disable-next-line <rule>` location whose underlying warning no longer fires after the most recent lint run).
2. For each file containing dead directives, parse the line(s), strip the directive (entire comment if directive-only; trailing-comment portion if shared with code), preserving indentation.
3. Emit one Diff per file with all dead directives in that file removed.
4. Conservative: only strips directives whose underlying rule code is *known* (`F401`, `react/no-unused-vars`, etc.). Unknown codes left alone with INFO note.

#### `health_dashboard_refresh`

1. Read `report.json` aggregate.
2. Regenerate `docs/health/latest.md` (current snapshot) and `docs/health/trend.md` (rolling 30 days, computed from `integrity-out/*/report.json` files in date order).
3. Compare to current files; emit Diff(s) only for changed files. Skip if both byte-identical.

### 4.7 PR dispatcher

```python
def run(diffs_by_class: dict[str, list[Diff]], cfg: AutofixConfig) -> dict[str, PRResult]: ...
```

Per fix class:

1. **Pre-check:** dispatch only if `diffs` is non-empty. Stale-check each Diff against current disk state (`stale_against`). Any stale → abort *this class*, emit `apply.stale_diff` ERROR; siblings continue.
2. **Capture lease SHA:** `git ls-remote origin refs/heads/<branch>` to capture the existing remote SHA (empty if branch doesn't exist remotely). This is the lease for the eventual force-push.
3. **Branch:** `git fetch origin main` then `git checkout -B integrity/autofix/<class>/<YYYY-MM-DD> origin/main` (force-create from origin/main). Any existing local branch is reset; the existing PR (if any) just re-points to the rewritten branch after push.
4. **Apply:** for each Diff, `Path(<repo>/diff.path).write_text(diff.new_content)`. `git add <path>` for each.
5. **Commit:** single commit per class, message `chore(integrity): <fix_class>\n\n<rationale per diff, bulleted>`. No `Co-Authored-By` footer (project policy).
6. **Push:** `git push --force-with-lease=<branch>:<lease_sha> origin <branch>` (lease_sha is empty for a brand-new branch, equivalent to `--force-with-lease` without a value). If the lease fails, abort with ERROR (someone pushed to the autofix branch — human investigates).
7. **Open or update PR:** `gh pr list --head <branch> --json number` → if exists, `gh pr edit <num> --body-file <body>`; else `gh pr create --title "<title>" --body-file <body> --base main`.
8. **Record result:** `PRResult(class, action="created"|"updated"|"skipped", pr_number, pr_url, branch, diff_count)`.

Subprocess discipline: every `git`/`gh` call uses `subprocess.run(..., timeout=cfg.dispatcher_subprocess_timeout_seconds, check=True, capture_output=True, text=True)`. Failures are caught at class level.

### 4.8 Safety preflight

Run before *any* fix class executes. Refusal modes:

| Check | Failure mode | Severity |
|-------|--------------|----------|
| Upstream plugins present in today's `integrity-out/` | Skip *all* fix classes | INFO `autofix.skipped_upstream_missing` |
| Any upstream plugin's `failures` non-empty | Skip *all* fix classes | INFO `autofix.skipped_upstream_failure` |
| `--apply` and `git status --porcelain` non-empty | Refuse apply (dry-run still produced) | ERROR `apply.dirty_tree` |
| `--apply` and current branch is `main` | Auto-checkout autofix branches; never edit main directly | (no error — handled in dispatcher) |
| `--apply` and `gh` not on PATH | Refuse apply | ERROR `apply.gh_unavailable` |
| `--apply` and `git remote get-url origin` fails | Refuse apply | ERROR `apply.no_remote` |
| Diff path escapes repo root (`Path.resolve()` not under `repo_root`) | Refuse *that diff* | ERROR `apply.path_escape` (per-diff fail-closed) |

`apply.path_escape` is the most important — it ensures a malicious or buggy fixer cannot write outside the repo. Tests cover this explicitly.

### 4.9 Circuit breaker

`config/autofix_state.yaml` (committed, edited by `make integrity-autofix-sync`):

```yaml
generated_at: 2026-04-17T03:00:00Z
generator_version: 1.0.0
window_days: 30
classes:
  claude_md_link:
    merged_clean: 4
    human_edited: 0
    pr_history:
      - {pr: 142, merged_at: 2026-03-25, action: clean}
      - {pr: 156, merged_at: 2026-04-02, action: clean}
  doc_link_renamed:
    merged_clean: 1
    human_edited: 3                # → exceeds max_human_edits (2) → class auto-disabled
    pr_history: [...]
```

`integrity-autofix-sync` is a separate subcommand:

1. Walks merged PRs in the last `window_days` whose head matches `integrity/autofix/*`.
2. For each, fetches the merge commit's diff vs the autofix branch's first commit. Identical → `clean`. Different → `human_edited` (someone amended before merge).
3. Updates `config/autofix_state.yaml` counts.
4. If any class crosses the threshold, sets `autofix.fix_classes.<class>.enabled: false` in `config/integrity.yaml` and emits one ERROR-severity issue in the next scan's report (`autofix.class_disabled`).

The breaker is **read** during scan (disabled classes are masked) and **written** by sync. Decoupling prevents sync failures from breaking dry-run.

### 4.10 Output artifact shape

`integrity-out/{date}/autofix.json`:

```json
{
  "plugin": "autofix",
  "version": "1.0.0",
  "date": "2026-04-17",
  "mode": "dry-run",                       // or "apply"
  "fix_classes_run": ["claude_md_link", "doc_link_renamed", "manifest_regen", "dead_directive_cleanup", "health_dashboard_refresh"],
  "fix_classes_skipped": {},               // class → reason
  "diffs_by_class": {
    "claude_md_link": [
      {
        "path": "CLAUDE.md",
        "rationale": "Index 2 unindexed docs under Deeper Context section",
        "source_issues": [
          {"plugin": "doc_audit", "rule": "doc.unindexed", "message": "...", "evidence": {...}}
        ],
        "is_noop": false,
        "diff_preview": "+- [Foo](docs/foo.md)\n+- [Bar](docs/bar.md)"
      }
    ],
    "manifest_regen": [],                  // empty — no changes needed
    ...
  },
  "pr_results": {                          // present only in apply mode
    "claude_md_link": {"action": "created", "pr_number": 173, "pr_url": "...", "branch": "...", "diff_count": 1}
  },
  "issues": [...],                         // standard IntegrityIssue list
  "failures": []                           // per-class failures (rare; mostly empty)
}
```

`diff_preview` is a unified-diff *display string* (computed via `difflib.unified_diff`) for human reading — the authoritative content lives in the in-memory `Diff` objects during apply.

## 5. Rule taxonomy

Plugin F emits issues for *visibility*, not for human-actionable drift. The fix classes themselves are the actions.

| Rule id | Severity | Meaning |
|---------|----------|---------|
| `autofix.proposed` | INFO | A fix class produced N diffs in dry-run. Evidence: `{class, diff_count, pr_branch}` |
| `autofix.applied` | INFO | A fix class produced and dispatched a PR. Evidence: `{class, pr_number, pr_url, action}` |
| `autofix.skipped_upstream_missing` | INFO | Sibling artifact missing; class skipped |
| `autofix.skipped_upstream_failure` | INFO | Sibling plugin reported failures; *all* classes skipped |
| `autofix.skipped_ambiguous_rename` | INFO | `doc_link_renamed` couldn't disambiguate a rename |
| `autofix.skipped_disabled` | INFO | Class disabled in config or by circuit breaker |
| `autofix.skipped_noop` | INFO | All proposed diffs were no-ops (e.g., manifest already in sync) |
| `autofix.upstream_parse_error` | ERROR | Sibling artifact present but unparseable |
| `apply.dirty_tree` | ERROR | `--apply` refused: working tree dirty |
| `apply.gh_unavailable` | ERROR | `--apply` refused: `gh` not on PATH |
| `apply.no_remote` | ERROR | `--apply` refused: no `origin` remote |
| `apply.stale_diff` | ERROR | Diff's `original_content` doesn't match disk; class aborted |
| `apply.path_escape` | ERROR | Diff path resolved outside repo_root; refused |
| `apply.git_failure` | ERROR | `git` subprocess failed during apply |
| `apply.gh_failure` | ERROR | `gh` subprocess failed during apply |
| `autofix.class_disabled` | ERROR | Circuit breaker disabled a class on this run |

Per-rule try/except: one rule's emission failing doesn't prevent siblings.

## 6. MVP scope (gate ζ)

The acceptance gate requires a *demonstration* per fix class — not a fleet of merged PRs. Trial period (1 week of nightly runs producing real PRs that merge cleanly) is post-gate, monitored via `integrity-autofix-sync` reports.

### 6.1 Five concrete diffs against the real repo (or fixture)

| Class | Real-repo expectation (2026-04-17) | Fallback if no real issue |
|-------|-----------------------------------|--------------------------|
| `claude_md_link` | Likely 0 issues today (CLAUDE.md is clean); fixture proves shape | Synthetic `docs/_autofix_fixture.md` not in CLAUDE.md → diff appends entry |
| `doc_link_renamed` | Likely 0; depends on recent renames | Synthetic doc with broken link to a path that `git log --diff-filter=R` can prove was renamed |
| `manifest_regen` | Possibly 0 if Plugin E already in sync | Touch-then-revert a tracked script to drift the manifest |
| `dead_directive_cleanup` | Depends on lint output; likely small list | Synthetic file with `# noqa: F401` whose F401 no longer fires |
| `health_dashboard_refresh` | Always produces a diff (today's report differs from yesterday's `latest.md`) | n/a |

### 6.2 What ships in this gate

- Five fixers, each with positive + negative test fixture
- Dispatcher with mock-subprocess test coverage (no real `gh` calls in CI)
- Safety preflight covering all seven refusal modes (2 skip-with-INFO + 5 hard ERROR refusals)
- Circuit breaker with state-file round-trip test
- `make integrity-autofix` (dry-run) wired into the engine
- `make integrity-autofix-apply` (apply) — runs but is gated by config + flag
- `make integrity-autofix-sync` — bookkeeping for the 30-day window
- `config/autofix_state.yaml` initialized with empty per-class counters
- Plugin registration in `engine.py` + `KNOWN_PLUGINS`
- `config/integrity.yaml` `autofix:` block
- `docs/log.md` entry
- Frontend Health "Autofix" tile (read-only) — counts of open PRs / disabled classes

## 7. Testing

### 7.1 Test taxonomy

- **Loader unit tests** — missing artifact → INFO + skip; parse error → ERROR
- **Diff round-trip tests** — apply, re-read, equals; stale-detection refuses overwrite
- **Per-fixer unit tests** — synthetic upstream artifact JSON → propose() returns expected diff list
- **Dispatcher tests** — mock `subprocess.run`; assert exact `git`/`gh` argv sequences for create + update flows
- **Safety preflight tests** — each refusal mode produces the right error severity and prevents apply
- **Circuit breaker tests** — counters round-trip; threshold disables class; recovery (counter reset) re-enables on next sync
- **Plugin integration test** — `tiny_repo_with_artifacts` fixture (fake `integrity-out/2026-04-17/*.json`) → AutofixPlugin scan produces the right diffs
- **Acceptance gate test** — 5-fixer synthetic fixture; dry-run produces 5 diff plans; no git side effects (asserts no branches created, no commits made via `git rev-parse HEAD` invariance)

### 7.2 Mocking discipline

- Subprocess calls mocked via `unittest.mock.patch("subprocess.run")` returning `CompletedProcess` with synthetic stdout
- `gh pr list --head <branch>` mocked to return `[]` (create path) or `[{"number": 123}]` (update path)
- Git operations never run for real in tests; the dispatcher's argv sequence is the contract

### 7.3 No-network guarantee

CI runs with `gh_executable=/bin/true` to make any accidental real-`gh` invocation safe. Tests assert mock invocation counts to detect regressions where real `gh` would otherwise be called.

## 8. Operational defaults

| Knob | Default | Notes |
|------|---------|-------|
| Trigger | Nightly cron (after Plugin B/C/E/D run) + manual `make integrity-autofix` | Dry-run only by default |
| Apply mode | Off in `config/integrity.yaml`; CI may override | Belt-and-braces — flag + config both required |
| PR open horizon | 30 days | After 30 days, sync closes stale autofix PRs with comment |
| Branch lifetime | Until PR merged or closed; sync deletes merged-branch artifacts | Standard cleanup |
| Storage | `integrity-out/{date}/autofix.json` (gitignored) + `config/autofix_state.yaml` (committed) + `config/integrity.yaml` updates from circuit breaker (committed) | Two committed surfaces — review-friendly |
| Concurrency | Per-class; 1 open PR max | Avoids storm |

## 9. Acceptance gate — ζ

Gate ζ is the **terminal gate** of the integrity roadmap. Pass criteria:

1. Five fixers implemented; each has positive + negative tests passing.
2. `make integrity-autofix` exits 0 against the real repo. Output `integrity-out/{date}/autofix.json` contains a `diffs_by_class` entry for every class (empty list is acceptable; no missing keys).
3. At least one fix class produces a non-empty diff plan against the real repo on the demo run (`health_dashboard_refresh` is always non-empty, satisfying this).
4. `make integrity` (full pipeline including F) exits 0.
5. Dispatcher tests prove correct `git`/`gh` argv sequences for both create and update flows.
6. Safety tests prove all seven preflight refusal modes work (2 skip-with-INFO + 5 hard ERROR).
7. Circuit breaker round-trips cleanly through `make integrity-autofix-sync`.
8. `--apply` is **not** exercised against the real repo during gate verification — that's reserved for the post-gate trial period. Apply path is verified via mocked subprocess only.
9. Frontend Autofix tile renders without errors (smoke test only — full UX is out of scope for the gate).

Post-gate (1-week trial): nightly cron runs `--apply` against a sandbox branch (or the real repo if user opts in via `apply: true`); each fix class should produce ≥1 PR; merge rate ≥ "1 clean PR per class without human edits" satisfies the "ready for daily use" bar.

## 10. Locked deferrals (post-MVP enhancements)

These are explicit decisions resolved at design time per the comprehensive/future-proof pre-approval. They are *deferred* (not implemented in gate ζ) but the resolution is locked so future iterations don't relitigate.

- **Sandbox branch for trial period.** Decision: trial period runs `--apply` against the real repo from day 1, scoped per fix class via `autofix.fix_classes.<class>.enabled`. User opts in by toggling each class to `enabled: true`; the per-class rollout pattern replaces a sandbox-branch dance.
- **`dead_directive_cleanup` linter coverage.** Decision: MVP ships ruff `# noqa: <code>` and `// eslint-disable-next-line <rule>` (line-form). Follow-up work adds mypy `# type: ignore[<code>]` and `// @ts-expect-error`. Block-form `eslint-disable` permanently out of scope (too hard to strip safely without parsing scope).
- **`claude_md_link` section selection.** Decision: heuristic uses deepest common path prefix; ties broken by `claude_md_link.target_section` config key (default `"## Deeper Context"`). LLM-driven section selection permanently out of scope (autofix is mechanical, not generative).
- **Stale autofix branch reaping.** Decision: `integrity-autofix-sync` deletes remote branches whose PRs are closed/merged >30 days ago. Opt-out via `autofix.sync.prune_branches: false` in `config/integrity.yaml`.
- **Apply rollback on partial failure.** Decision: no rollback. Per-class isolation throughout — successful PRs stand on their own; failed classes simply don't get PRs that run. Matches the per-class try/except discipline used in dispatcher and matches Plugin D/E per-rule isolation.
- **Multi-language directive support.** Decision: `dead_directive_cleanup` is language-agnostic via a `DirectiveStrategy` Protocol; MVP ships two strategies (Python ruff + TS eslint-line). New languages added via new strategy registration without touching the core fixer.

## 11. References

- Parent: `docs/superpowers/specs/2026-04-16-integrity-system-design.md` §5.6 + §7 (gate ζ definition)
- Sibling: `docs/superpowers/specs/2026-04-17-integrity-plugin-d-design.md` (mirrors plugin/builder layering)
- Sibling: `docs/superpowers/specs/2026-04-17-integrity-plugin-e-design.md` (provides `manifest_regen` emitter)
- Sibling: `docs/superpowers/specs/2026-04-17-integrity-plugin-c-design.md` (provides `claude_md_link` + `doc_link_renamed` sources)
- Sibling: `docs/superpowers/specs/2026-04-17-integrity-plugin-b-design.md` (provides `dead_directive_cleanup` source)
- `gh` CLI: https://cli.github.com/manual/gh_pr_create
- `git push --force-with-lease`: https://git-scm.com/docs/git-push#Documentation/git-push.txt---force-with-leaseltrefnamegt
- Conventional commits: https://www.conventionalcommits.org/
