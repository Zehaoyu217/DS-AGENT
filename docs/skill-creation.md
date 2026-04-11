# Skill Creation Guide

## Anatomy of a Skill

```
backend/app/skills/<name>/
├── SKILL.md          # Agent reads this (<200 lines)
├── skill.yaml        # Metadata, triggers, dependencies
├── pkg/              # Python package (agent imports in sandbox)
│   ├── __init__.py   # Public API
│   └── <modules>.py  # Implementations (unlimited length)
├── references/       # Agent loads on demand
├── tests/            # Unit tests (pytest)
└── evals/            # SEALED — never loaded to agent
    ├── eval.yaml     # Test cases + assertions
    └── fixtures/     # Sample data
```

## Step-by-Step

1. **Scaffold:** `make skill-new name=my_skill`
2. **Write skill.yaml:** Define name, level, errors, dependencies
3. **Write pkg/:** Implement functions with `@skill_function` decorator
4. **Write SKILL.md:** Agent instructions (<200 lines)
5. **Write tests/:** Unit tests for pkg functions
6. **Write evals/:** Sealed behavioral tests
7. **Validate:** `make skill-check` then `make skill-eval skill=my_skill`

## Key Rules

- SKILL.md < 200 lines — it's instructions, not implementation
- Python packages have no line limit — they're libraries
- Every error must be declared in skill.yaml with message + guidance + recovery
- Parameter names must be self-documenting
- evals/ is never loaded into the agent's context
- Level 1 skills are leaf functions, level 2 compose level 1, level 3 orchestrates level 2
