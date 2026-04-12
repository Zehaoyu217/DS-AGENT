# Data Science Iteration — Design Spec

**Date:** 2026-04-12
**Skill name:** `data-science-iteration`
**Location (target):** `~/.claude/skills/data-science-iteration/`
**Status:** Design approved, ready for implementation planning
**Independence:** Standalone skill, not coupled to the `superpowers` plugin. May reference superpowers patterns but does not require the plugin installed.

---

## 1. Purpose

Give Claude a disciplined, iterative, reproducible data-science workflow that behaves like a suspicious-yet-creative data scientist:

- Starts from a dataset and a loose goal.
- Produces **v1 → v2 → v3 …** plans, each informed by findings of the previous.
- Treats disproven hypotheses as first-class, high-value artifacts.
- Is bullet-proof about validation (no leakage, honest CV, locked holdout, uncertainty required).
- Pulls in prior art (Kaggle, GitHub, papers, mature packages) when moving beyond baseline modeling.
- Runs a live, always-open browser **leaderboard dashboard** that tracks every experiment since project inception.

**Non-goals:** production MLOps, drift monitoring, AutoML bandits, a tutorial for beginners, owning the data pipeline.

---

## 2. Architecture (Hybrid orchestrator)

One orchestrator skill that owns loop state and invokes specialized sub-roles (personas) at defined gates. Heavy persona work dispatched as subagents.

```
~/.claude/skills/data-science-iteration/
├── SKILL.md                        # orchestrator: loop state machine, Iron Laws, gate logic, entry flow
├── iron-laws.md                    # the 11 rules + enforcement notes
├── loop-state-machine.md           # phases, events, transitions, stop criteria
├── workspace-layout.md             # ds-workspace/ spec (per-project)
├── dashboard-spec.md               # leaderboard UI contract, data format, design system
├── personas/
│   ├── skeptic.md
│   ├── explorer.md
│   ├── literature-scout.md
│   ├── statistician.md
│   ├── validation-auditor.md
│   └── engineer.md
├── playbooks/
│   ├── phase-frame.md
│   ├── phase-audit.md
│   ├── phase-eda.md
│   ├── phase-feature-model.md
│   ├── phase-validate.md
│   ├── phase-findings.md
│   ├── event-leakage-found.md
│   ├── event-assumption-disproven.md
│   ├── event-metric-plateau.md
│   ├── event-cv-holdout-drift.md
│   └── event-novel-modeling-flag.md
├── templates/
│   ├── plan-vN.md
│   ├── finding-card.md
│   ├── disproven-card.md
│   ├── literature-memo.md
│   └── state.schema.json
├── checklists/
│   ├── leakage-audit.md
│   ├── cv-scheme-decision.md
│   ├── assumption-tests.md
│   ├── reproducibility.md
│   └── ship-gate.md
├── dashboard-template/             # static assets copied into ds-workspace/dashboard/ on init
│   ├── index.html
│   ├── assets/styles.css
│   ├── assets/app.js
│   └── assets/charts.js
└── slash/
    └── ds.md                        # /ds entry command
```

**Decoupling rules (per user direction):**

- No `superpowers:*` prefix in any skill reference.
- No hard invocation of any superpowers skill.
- Patterns borrowed from superpowers (parallel subagents, systematic debugging) are re-implemented inline in this skill's own files.
- Compatible with but not dependent on superpowers.

---

## 3. Loop state machine

### Phases within an iteration vN

```
FRAME → AUDIT → EDA → FEATURE_MODEL → VALIDATE → FINDINGS → (SHIP | NEXT_V)
```

### Phase entry gates

| Phase | Gate to enter |
|---|---|
| FRAME | goal + primary metric + data contract declared |
| AUDIT | Validation Auditor signs off on holdout carve-out + CV scheme |
| EDA | `plans/vN.md` committed; Explorer persona loaded |
| FEATURE_MODEL | baseline recorded (Iron Law #5); literature memo present if novel-modeling-flag |
| VALIDATE | CV results + uncertainty present; no fit-on-full-data violations |
| FINDINGS | every hypothesis from vN resolves to finding-card OR disproven-card |

### Cross-cutting events (fire any time, abort current phase, open vN+1)

| Event | Trigger | Response |
|---|---|---|
| `leakage-found` | Validation Auditor or leakage-audit grep finds target/time/group leak | Abort vN, open vN+1 with leakage remediation as first hypothesis; mark affected runs invalidated in leaderboard |
| `assumption-disproven` | Statistician or Skeptic shows a framing assumption is false | File disproven-card, update `data-contract.md`, open vN+1 |
| `metric-plateau` | 2 consecutive vN with no stat-significant CV improvement | Literature Scout required for vN+1 (auto full-depth review) |
| `cv-holdout-drift` | Gap between CV and holdout at ship gate exceeds predicted interval | Do NOT ship; open vN+1 investigating drift source |
| `novel-modeling-flag` | Orchestrator detects move beyond {linear, tree, GBM} families | Trigger Full Literature Scout before FEATURE_MODEL |

### Stop criteria

Run ends when ALL of:

1. User says `ship`, AND
2. All Skeptic / Validation Auditor CRITICAL blockers cleared, AND
3. CV metric meets pre-declared target, AND
4. Locked holdout evaluated exactly once → final report generated.

OR diminishing-returns gate: 3 consecutive vN without stat-significant CV improvement → orchestrator proposes `ship` or `pivot` (redefine problem).

OR user says `abort`.

---

## 4. Per-project workspace (`ds-workspace/`)

```
<project-root>/
└── ds-workspace/
    ├── state.json                  # { current_v, phase, seed, data_sha256, env_lock_hash,
    │                               #   holdout_locked_at, holdout_reads, active_hypotheses,
    │                               #   open_blockers, events_history }
    ├── data-contract.md            # schema, grain, units, known-dirtiness, provenance
    ├── holdout/
    │   ├── HOLDOUT_LOCK.txt        # sha256 + timestamp + "do not read until ship"
    │   └── holdout.parquet
    ├── plans/
    │   └── vN.md
    ├── findings/
    │   └── vN-fNNN.md
    ├── disproven/                  # high-value learning artifacts
    │   └── vN-dNNN.md
    ├── literature/
    │   └── vN-memo.md
    ├── audits/
    │   ├── vN-skeptic.md
    │   ├── vN-leakage.md
    │   ├── vN-cv-scheme.md
    │   ├── vN-assumptions.md
    │   ├── vN-repro.md
    │   └── vN-ship-gate.md
    ├── runs/
    │   └── vN/
    │       ├── metrics.json        # CV mean/std, bootstrap CIs, lift vs baseline
    │       ├── env.lock
    │       ├── seed.txt
    │       ├── data.sha256
    │       └── plots/
    ├── nb/                         # notebook track (optional)
    │   └── vN_*.ipynb              # must only call src/ — enforced
    ├── src/                        # library code (both tracks)
    │   └── data/ features/ models/ evaluation/
    └── dashboard/                  # live leaderboard (Section 6)
```

**Promotion target (outside the project):**
`~/.claude/skills/ds-learnings/YYYY-MM-DD-<project>-<lesson-slug>.md`
Created only when a disproven-card or finding generalizes beyond this project AND both Skeptic and Statistician vote yes.

**Retention:** orchestrator never auto-prunes. Runs marked `invalidated` or `superseded` stay in place so the dashboard shows full history until the user manually deletes.

---

## 5. Personas

Each persona is an `.md` the orchestrator loads at specific gates. Heavy work dispatched as a subagent.

| Persona | Invoked at | Output artifact | Can block? |
|---|---|---|---|
| **Skeptic** | every plan gate; before `ship` | `audits/vN-skeptic.md` | Yes — unresolved CRITICAL blocks phase entry |
| **Validation Auditor** | end of FRAME; before FEATURE_MODEL; before `ship` | `audits/vN-leakage.md`, `audits/vN-cv-scheme.md` | Yes — any leakage fires `leakage-found` |
| **Statistician** | end of VALIDATE; before parametric inference; before `ship` | `audits/vN-assumptions.md` | Yes — blocks parametric inference on failed assumptions |
| **Explorer** | EDA phase | candidate hypotheses → plan-v(N+1); plots in `runs/vN/plots/` | No |
| **Literature Scout** | on `novel-modeling-flag` or `metric-plateau`; optional at FRAME | `literature/vN-memo.md` | No |
| **Engineer** | after any `src/` change; before `ship` | `audits/vN-repro.md` | Yes — non-reproducible run invalidates vN |

**Tension resolution:** Explorer runs BEFORE Skeptic/Auditor/Statistician in each cycle. Creative ideation produces candidates; the suspicious roles cull at the gate. Creativity is not blocked, but promotion past the gate requires rigor sign-off.

**Dispatch pattern:** lightweight inline checklist application; heavy checks (Literature Scout full review, multi-file leakage grep, reproducibility re-run) dispatched as parallel subagents.

---

## 6. Live leaderboard dashboard

### Purpose

Always-open browser page showing the full experiment history and current winner while the loop runs. Doubles as the persistent visual log.

### Layout on disk

```
ds-workspace/dashboard/
├── index.html
├── assets/
│   ├── styles.css              # oklch palette tokens; editorial/bento aesthetic
│   ├── app.js                  # fetches data/leaderboard.json, renders
│   └── charts.js               # uPlot-based chart primitives
└── data/
    ├── leaderboard.json        # source of truth for UI
    └── events.ndjson           # append-only event log
```

### Serving model

- Orchestrator runs `python -m http.server` on an auto-picked free port at run start.
- URL written to `ds-workspace/dashboard/URL.txt` and printed in chat.
- On macOS, orchestrator attempts `open <url>` to pop the page.
- Page polls `data/leaderboard.json` every 3 seconds. No websockets.
- Server killed on `ship` or `abort`.
- Dashboard assets seeded from the skill's `dashboard-template/` directory on workspace init.

### `leaderboard.json` schema

```json
{
  "project": "churn-v1",
  "primary_metric": { "name": "PR-AUC", "direction": "max" },
  "current_state": { "v": 3, "phase": "FEATURE_MODEL", "updated_at": "ISO8601" },
  "runs": [
    {
      "id": "v2-r07",
      "v": 2,
      "created_at": "ISO8601",
      "model": "lightgbm",
      "params_summary": "300 trees, lr=0.05, max_depth=6",
      "features_used": 42,
      "feature_groups": ["rfm", "tenure", "support_tickets"],
      "cv_mean": 0.714,
      "cv_std": 0.011,
      "cv_ci95": [0.701, 0.727],
      "lift_vs_baseline": 0.082,
      "status": "valid",
      "invalidation_reason": null,
      "notes_ref": "plans/v2.md#H-v2-03",
      "seed": 42,
      "data_sha256": "ab…",
      "env_lock_hash": "cd…"
    }
  ],
  "disproven": [
    { "id": "v2-d001", "claim": "…", "lesson": "…", "date": "ISO8601" }
  ],
  "events": [
    { "type": "leakage-found", "v": 2, "ref": "audits/v2-leakage.md", "at": "ISO8601" }
  ]
}
```

`status` ∈ `{ valid, invalidated, superseded }`. Runs never deleted automatically.

### UI sections

1. **Headline band** — current winner (model, metric with CI, lift vs baseline, date). Large scale contrast.
2. **Leaderboard table** — all runs ever; sortable; color-coded by status; metric + CI, lift, feature count, date, seed. Row click opens detail drawer.
3. **Version timeline** — horizontal vN strip with phase chips and event markers.
4. **Metric-over-time chart** — one line per model family; uncertainty bands from `cv_std`; dashed baseline reference.
5. **Disproven wall** — card grid ("museum of wrong ideas") with lesson excerpts. Intentional visual weight.
6. **Audit strip** — latest Skeptic / Auditor / Statistician verdicts and open CRITICAL blockers (red chip).

### Design discipline

Per `~/.claude/rules/web/design-quality.md`:

- Editorial / bento direction. **Not** a dashboard-by-numbers template.
- Palette declared via CSS tokens (`oklch`).
- Typography pairing: serif display face for headline metric; mono for numbers; system sans for body.
- Animation restricted to `transform` and `opacity`.
- Bundle budget: **< 80 kB gzipped total**. Stack: vanilla JS + uPlot (~40 kB). No React, no Tailwind.

### Writer contract

Every orchestrator mutation to a run, event, finding, or disproven card must also:

1. Update `leaderboard.json` atomically.
2. Append one line to `events.ndjson`.

Runs that never appear on the dashboard are considered not to exist (Iron Law #11).

---

## 7. Iron Laws (enforcement-backed)

| # | Law | Enforcement |
|---|---|---|
| 1 | Locked holdout exists before any modeling | `HOLDOUT_LOCK.txt` + `state.holdout_reads` counter; orchestrator refuses VALIDATE/holdout reads outside ship gate; any unlogged read invalidates run |
| 2 | CV scheme chosen before features | FRAME exit requires signed `audits/vN-cv-scheme.md`; downstream phases refuse without it |
| 3 | No target-dependent fit on full data | Leakage-audit grep over `src/`; patterns in `checklists/leakage-audit.md`; hits fire `leakage-found` |
| 4 | Every metric reported with uncertainty | Statistician rejects `metrics.json` lacking CI or CV-std; VALIDATE cannot sign off |
| 5 | Baseline before complexity | FEATURE_MODEL gate checks for `baseline` entry in `runs/*/metrics.json`; refuses non-baseline until present |
| 6 | Disproven hypotheses are artifacts | FINDINGS exit requires every hypothesis to have finding-card OR disproven-card |
| 7 | Literature review before novel modeling | Novel-modeling-flag requires `literature/vN-memo.md` before FEATURE_MODEL |
| 8 | Assumption tests before parametric stats | Statistician assumption checklist gates parametric inference in findings |
| 9 | Reproducibility: seed, env, data hash | Engineer re-runs one random CV fold and compares; mismatch = block |
| 10 | Notebooks call `src/` only | Auditor grep on `nb/*.ipynb` for class/function defs or sklearn fits inside cells |
| 11 | Every modeled run appears on the dashboard | FEATURE_MODEL and VALIDATE exits refuse if run is not written to `leaderboard.json` |

Enforcement is mechanical: phase transitions happen only when the required files exist and have been signed (persona artifact = signature). Persona checks at each gate can be dispatched as parallel subagents.

---

## 8. Entry flow (user perspective)

```
User: /ds   (or types something data/model-shaped in a project with ds-workspace/ or data/)
  ↓
Skill loads → asks 4 framing questions, one at a time:
  1. What decision does this model support? (grounds the metric)
  2. What is the data unit/grain and time structure? (grounds CV scheme)
  3. Is there a hard success threshold? (grounds ship gate)
  4. Track: notebook or script?
  ↓
Creates ds-workspace/ scaffold + dashboard (seeded from skill's dashboard-template/)
Starts local http server; prints dashboard URL; attempts to open browser
  ↓
Writes v1 plan draft → Skeptic + Validation Auditor review → signed
  ↓
Enters loop. Orchestrator narrates phase transitions and gate results in chat
  ↓
User commands at any time:
  - status           → print current phase, blockers, leaderboard top-3
  - ship             → open ship gate sequence
  - abort            → graceful teardown; dashboard preserved
  - force v+1 <why>  → close vN early, open v(N+1)
  - dig <hypothesis> → branch investigation without leaving current vN
```

**Slash command:** `/ds` registered by this skill's `slash/ds.md`.

**Auto-trigger:** skill announces itself when the user mentions data/model/dataset/notebook in a project that already contains `ds-workspace/` or a top-level `data/` folder. User can decline.

---

## 9. Compatibility notes (not dependencies)

These can be used **if present**, but the skill never requires them:

- `superpowers:brainstorming` — useful upstream if the decision/metric is fuzzy; out of scope for this skill.
- `superpowers:systematic-debugging` — when a *bug* surfaces (as opposed to a hypothesis being wrong); pattern replicated inline in `playbooks/event-*.md`.
- `superpowers:dispatching-parallel-agents` — pattern replicated inline for gate-time parallel reviews.
- `superpowers:test-driven-development` — applies to `src/` code, not to the modeling loop.
- Existing user skills `python-patterns`, `python-testing`, `eval-harness`, `ai-regression-testing`, `exa-search`, `deep-research`, `continuous-learning` — referenced by Literature Scout and Engineer where useful, but not required.

---

## 10. Open items carried into implementation planning

- Dashboard atomic write strategy: write-temp-then-rename for `leaderboard.json` to avoid UI reading a partial file during a mutation.
- HTTP server port selection + teardown: PID file and ownership check to avoid killing a different process on restart.
- Holdout lock is disciplinary (orchestrator honors `HOLDOUT_LOCK.txt`); filesystem-level immutability (e.g., `chflags uchg` on macOS) optional enhancement for later versions.
- Activation of promoted `~/.claude/skills/ds-learnings/` entries in future runs: v1 uses them as Literature Scout references; a later version may auto-inject matching lessons into relevant FRAME prompts.
- Exact hypothesis-ID scheme and collision handling across branches from `dig` command.
- Notebook-track leakage grep must handle `.ipynb` JSON; tooling choice (nbconvert vs `jq` on cells) to be decided in the implementation plan.

---

## 11. Success criteria for this skill

A data-science iteration run under this skill should:

1. Never ship a model whose CV-holdout gap exceeds the predicted range without an explicit investigation.
2. Produce a `disproven/` directory with at least one card per iteration in almost every real project — absence is a smell to investigate.
3. Run an always-visible dashboard that the user can point at to answer "what's the current best model, and how did we get here?" without asking Claude.
4. Never allow a non-baseline model to be trained before baseline metrics exist.
5. Make Iron Law violations impossible to commit silently: the file/gate mechanism blocks phase progression when a rule is broken.
6. Be delete-safe: the user can `rm -rf ds-workspace/` without corrupting anything outside the project.
