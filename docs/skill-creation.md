# Skill Creation Guide

Skills are organized in a tree. The agent sees top-level (Level 1) skills in the system
prompt. Loading a skill reveals its children. This is progressive exposure — the agent
loads only what the current task needs.

## Skill Levels

| Level | Description | Example |
|-------|-------------|---------|
| 1 | Hub or standalone skill; always visible to agent | `statistical_analysis`, `sql_builder` |
| 2 | Sub-skill; visible after loading its parent | `correlation`, `altair_charts` |
| 3 | Reference/deep-doc; visible after loading its parent | `correlation_methodology` |

**Hub rule:** Only create a hub (a skill with children) when it has 2+ children.
A hub with one child is just indirection — make the child a Level 1 standalone instead.

## File Structure

```
backend/app/skills/
  my_hub/                    ← Level 1 hub
    SKILL.md                 ← hub guidance doc
    __init__.py              ← required for Python import traversal
    child_skill/             ← Level 2
      SKILL.md
      pkg/
        __init__.py
      skill.yaml
      tests/
      deep_reference/        ← Level 3 (reference)
        SKILL.md
        skill.yaml

  standalone_skill/          ← Level 1 standalone (no hub)
    SKILL.md
    pkg/
    skill.yaml
    tests/
```

**`__init__.py` rule:** Any skill directory that has children (is a hub at any depth)
must have `__init__.py`. This lets Python traverse the module path to reach nested
`pkg/` packages. The `make skill-new parent=X` command handles this automatically.

## Scaffolding Commands

```bash
# Level 1 standalone skill
make skill-new name=my_skill

# Level 2 sub-skill under an existing hub
make skill-new name=my_skill parent=my_hub

# Level 3 reference skill (no pkg/, [Reference] description template)
make skill-new name=my_ref parent=my_hub type=reference
```

## SKILL.md Format

**Operational skill (Level 1 or 2):**

```yaml
---
name: my_skill
description: One-line description of what this skill does.
version: "0.1"
---
```

Body: what it does, when to use it, contract (inputs/outputs), usage examples.
Max 200 lines. Put implementation in `pkg/`.

**Hub skill (Level 1, has children):**

```yaml
---
name: my_hub
description: "Domain description. Sub-skills: child_a, child_b."
version: "0.1"
---
```

Body: decision table for choosing sub-skills, workflow guidance. No code examples.
Typically 30-60 lines.

**Reference skill (Level 3):**

```yaml
---
name: my_reference
description: "[Reference] What this documents and when to load it. Be specific —
  the agent uses this one-liner to decide whether to load the reference."
version: "0.1"
---
```

Body: deep technical documentation, methodology, limitations, edge cases.
No length limit. Never advertised in the always-on catalog — only visible after
the parent is loaded.

**Rules:**
- Never add a `level:` field — depth is computed from directory position.
- `[Reference]` prefix belongs in the `description` field, not a separate field.
- Description must be one line (or two short lines) — it appears in the sub-skill catalog.
- YAML descriptions containing `[` must be quoted (e.g. `description: "[Reference] ..."`)
  to prevent YAML parse failures.

## skill.yaml

```yaml
dependencies:
  requires: []         # skill names this skill depends on at runtime
  used_by: []          # skills that depend on this
  packages: []         # Python packages needed in the sandbox
errors:
  MY_ERROR:
    message: "Description with {placeholder}"
    guidance: "What the agent should do."
    recovery: "Concrete recovery step."
```

## Hub SKILL.md Guidelines

Hub skills are navigation aids, not instruction documents. Their body should contain:
- A decision table: "task X → use sub-skill Y"
- Workflow notes: what order to load sub-skills, when to combine them
- No code examples (code lives in leaf skills)

The sub-skill catalog is auto-appended by the system — do not write it yourself.

## Validation

```bash
make skill-check    # validates dependency graph
```
