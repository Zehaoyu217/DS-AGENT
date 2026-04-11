# Git Workflow

## Branch Naming

```
feat/<feature-name>
fix/<bug-description>
refactor/<what>
docs/<what>
```

## Commit Format

```
<type>: <description>

<optional body>
```

Types: feat, fix, refactor, docs, test, chore, perf

## Pull Requests

1. Branch from `main`
2. Make changes, commit with conventional commits
3. Push with `git push -u origin <branch>`
4. Create PR: `gh pr create --title "..." --body "..."`
5. Ensure all checks pass before merge
