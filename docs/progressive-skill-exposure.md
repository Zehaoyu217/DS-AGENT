# Progressive Skill Exposure

## Mental Model

The agent always sees the top of the skill tree (Level 1 skills). Loading a skill
reveals its children. Loading a child reveals its children. The agent traverses as
deeply as the task requires — no deeper.

```
System prompt (every turn) — Level 1 only:
  statistical_analysis  [5 sub-skills]
  charting              [1 sub-skill]
  reporting             [3 sub-skills]
  data_profiler
  sql_builder
  analysis_plan

Agent loads statistical_analysis → sees body + sub-skill catalog:
  correlation
  distribution_fit
  group_compare
  stat_validate
  time_series

Agent loads correlation → sees body + sub-skill catalog:
  correlation_methodology  [Reference] — load only for algorithmic depth
```

## Why This Exists

The original system injected all skill descriptions into every turn. The new system
injects 6 Level-1 descriptions. Sub-skill catalogs only appear after an explicit
`skill()` call. Token reduction: ~65% per turn.

Beyond tokens: the flat catalog gave the agent no information about skill relationships.
The progressive model makes the domain structure explicit and navigable.

## What the Agent Sees

**System prompt (always-on):**
```
## Skills

Use the `skill` tool to load any skill before using it. Hub skills expand into sub-skills
when loaded — read the sub-skill catalog before deciding which to use.

- `statistical_analysis` — Statistical tests and analysis. [5 sub-skills]
- `charting` — Visualization capabilities using Altair. [1 sub-skill]
- `reporting` — Build HTML reports, dashboards, and tables. [3 sub-skills]
- `data_profiler` — Full-dataset profile: schema, types, nulls, distributions.
- `sql_builder` — Write and execute SQL queries against loaded datasets.
- `analysis_plan` — Generate a structured analysis plan before diving into data.
```

**After `skill("statistical_analysis")`:**
```
# statistical_analysis

[hub body]

---
## Sub-skills

- `correlation` — Selects and runs the right correlation method.
- `distribution_fit` — Fits parametric distributions to a column.
- `group_compare` — Compares means/medians across groups.
- `stat_validate` — Validates statistical assumptions before analysis.
- `time_series` — Decomposes and forecasts time-series data.
```

## Access Rules

- Discovery is progressive — the agent navigates via hub→sub-skill.
- Access is permissive — `skill("correlation")` works even without loading
  `statistical_analysis` first. This supports power-users who name a sub-skill directly.
- Reference skills signal themselves via `[Reference]` in their description.
  The agent self-selects — the system never forces a reference skill load.
- YAML descriptions with `[` must be quoted to prevent silent parse failures.

## Implementation

- **Registry:** `SkillRegistry.list_top_level()` → Level 1 only (for system prompt).
  `SkillRegistry.get_children(name)` → direct children (for sub-skill catalog).
  Both structures maintained in a single recursive `discover()` pass.
- **Skill tool:** `_load_skill_body()` auto-appends the sub-skill catalog when
  `get_children()` returns results. Never shown for leaf skills.
- **Injector:** `PreTurnInjector._skill_menu()` calls `list_top_level()`, annotates
  hubs with `[N sub-skills]`.
- **Hierarchy:** Filesystem nesting IS the hierarchy. No metadata field for level.
  Depth is computed from directory position during discovery.
