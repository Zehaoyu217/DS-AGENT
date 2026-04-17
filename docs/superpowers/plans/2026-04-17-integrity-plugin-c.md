# Plugin C — Doc Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship gate γ of the integrity system: Plugin C (`doc_audit`) emits 6 markdown-drift rule classes, plugged into the engine + report aggregator that gate β already shipped, with markdown-it-py parsing and git-log/git-rename reuse from Plugin B.

**Architecture:** A new `DocAuditPlugin` (mirrors `GraphLintPlugin` shape) registers into the existing engine. A `parser/` layer pre-builds a `MarkdownIndex` (parsed docs + heading anchors + link graph + excluded/ignored sets) once per scan. Six rules consume that index plus `GraphSnapshot` (from gate α) plus `git_renames`/`git_log` helpers. Output goes to `integrity-out/{date}/doc_audit.json` and flows through the existing report aggregator → `docs/health/latest.md`. Frontend Health page picks up new content automatically — no UI changes.

**Tech Stack:** Python 3.12, `markdown-it-py >= 3.0` (CommonMark + GFM), reuses `IntegrityEngine`, `GraphSnapshot`, `IntegrityIssue`, `report.py`, `git_renames` shipped at gate β. pytest for tests.

---

## File Structure

### Backend — new files

| Path | Purpose |
|------|---------|
| `backend/app/integrity/plugins/doc_audit/__init__.py` | Package marker |
| `backend/app/integrity/plugins/doc_audit/plugin.py` | `DocAuditPlugin` dataclass; orchestrates rules; per-rule try/except |
| `backend/app/integrity/plugins/doc_audit/index.py` | `MarkdownIndex` builder (parse all docs, build reachability graph, anchors, excluded/ignored sets) |
| `backend/app/integrity/plugins/doc_audit/parser/__init__.py` | Package marker |
| `backend/app/integrity/plugins/doc_audit/parser/markdown.py` | `markdown-it-py` wrapper: `ParsedDoc`, `Heading`, `MarkdownLink`, `parse_doc` |
| `backend/app/integrity/plugins/doc_audit/parser/code_refs.py` | `CodeRef` dataclass + path/symbol extraction regex |
| `backend/app/integrity/plugins/doc_audit/parser/git_log.py` | `GitLog` class with cached `last_commit_iso(rel_path)` |
| `backend/app/integrity/plugins/doc_audit/parser/ignore.py` | `.claude-ignore` loader (gitignore-style globs) |
| `backend/app/integrity/plugins/doc_audit/rules/__init__.py` | Package marker |
| `backend/app/integrity/plugins/doc_audit/rules/unindexed.py` | `doc.unindexed` (BFS reachability) |
| `backend/app/integrity/plugins/doc_audit/rules/broken_link.py` | `doc.broken_link` + git-rename downgrade |
| `backend/app/integrity/plugins/doc_audit/rules/dead_code_ref.py` | `doc.dead_code_ref` (graph lookup) |
| `backend/app/integrity/plugins/doc_audit/rules/stale_candidate.py` | `doc.stale_candidate` (90d threshold, INFO) |
| `backend/app/integrity/plugins/doc_audit/rules/adr_status_drift.py` | `doc.adr_status_drift` (Accepted ADRs only) |
| `backend/app/integrity/plugins/doc_audit/rules/coverage_gap.py` | `doc.coverage_gap` |
| `backend/tests/integrity/plugins/doc_audit/__init__.py` | Package marker |
| `backend/tests/integrity/plugins/doc_audit/conftest.py` | `tiny_repo` fixture builder |
| `backend/tests/integrity/plugins/doc_audit/test_plugin.py` | Plugin shell + integration test against `tiny_repo` |
| `backend/tests/integrity/plugins/doc_audit/test_index.py` | `MarkdownIndex` builder tests |
| `backend/tests/integrity/plugins/doc_audit/parser/__init__.py` | Package marker |
| `backend/tests/integrity/plugins/doc_audit/parser/test_markdown.py` | Markdown parser tests |
| `backend/tests/integrity/plugins/doc_audit/parser/test_code_refs.py` | Code-ref regex tests |
| `backend/tests/integrity/plugins/doc_audit/parser/test_git_log.py` | Git-log helper tests |
| `backend/tests/integrity/plugins/doc_audit/parser/test_ignore.py` | `.claude-ignore` matcher tests |
| `backend/tests/integrity/plugins/doc_audit/rules/__init__.py` | Package marker |
| `backend/tests/integrity/plugins/doc_audit/rules/test_unindexed.py` | unindexed rule tests |
| `backend/tests/integrity/plugins/doc_audit/rules/test_broken_link.py` | broken_link rule tests |
| `backend/tests/integrity/plugins/doc_audit/rules/test_dead_code_ref.py` | dead_code_ref rule tests |
| `backend/tests/integrity/plugins/doc_audit/rules/test_stale_candidate.py` | stale_candidate rule tests |
| `backend/tests/integrity/plugins/doc_audit/rules/test_adr_status_drift.py` | adr_status_drift rule tests |
| `backend/tests/integrity/plugins/doc_audit/rules/test_coverage_gap.py` | coverage_gap rule tests |

### Backend — modified files

| Path | Change |
|------|--------|
| `backend/pyproject.toml` | Add `markdown-it-py>=3.0` to dependencies |
| `backend/app/integrity/config.py` | Add `doc_audit` defaults block to `DEFAULTS` |
| `backend/app/integrity/__main__.py` | Add `"doc_audit"` to `KNOWN_PLUGINS`, register `DocAuditPlugin` |
| `config/integrity.yaml` | Add `doc_audit:` block with overrides |
| `Makefile` | Add `integrity-doc` target; update `integrity` help text to `(A→B→C)` |

### Repo-level — possibly modified

| Path | Change |
|------|--------|
| `CLAUDE.md` | Optionally add links to currently-unreachable docs to clear `doc.unindexed` (gate criterion) |
| `.claude-ignore` | Optionally create with opt-out list for unreachable-by-design docs |

---

## Task Sequencing

Tasks are ordered so each can be implemented and tested in isolation by a fresh subagent. Dependencies are linear (no parallel tasks):

1. Skeleton + dependency (markdown-it-py + package dirs)
2. Config defaults
3. Parser: markdown
4. Parser: code_refs
5. Parser: git_log
6. Parser: ignore
7. MarkdownIndex builder
8. Plugin shell
9. Rule: coverage_gap (simplest, validates plugin shell)
10. Rule: unindexed
11. Rule: broken_link
12. Rule: dead_code_ref
13. Rule: stale_candidate
14. Rule: adr_status_drift
15. Engine wiring (CLI + KNOWN_PLUGINS)
16. Makefile + plugin integration test
17. Real-repo smoke + acceptance-gate verification

---

### Task 1: Skeleton + markdown-it-py dependency

**Files:**
- Modify: `backend/pyproject.toml`
- Create: `backend/app/integrity/plugins/doc_audit/__init__.py`
- Create: `backend/app/integrity/plugins/doc_audit/parser/__init__.py`
- Create: `backend/app/integrity/plugins/doc_audit/rules/__init__.py`
- Create: `backend/tests/integrity/plugins/doc_audit/__init__.py`
- Create: `backend/tests/integrity/plugins/doc_audit/parser/__init__.py`
- Create: `backend/tests/integrity/plugins/doc_audit/rules/__init__.py`

- [ ] **Step 1: Add markdown-it-py to backend deps**

Edit `backend/pyproject.toml`. Locate the `[project] dependencies` array (NOT the `[project.optional-dependencies] dev` array — `markdown-it-py` is a runtime dependency for the integrity engine). Add:

```toml
"markdown-it-py>=3.0",
```

Place it alphabetically. Confirm by running:

```bash
cd /Users/jay/Developer/claude-code-agent/backend && uv lock --upgrade-package markdown-it-py 2>&1 | tail -20
```

Expected: lockfile updated, exit 0.

- [ ] **Step 2: Create empty package markers**

```bash
mkdir -p /Users/jay/Developer/claude-code-agent/backend/app/integrity/plugins/doc_audit/parser \
         /Users/jay/Developer/claude-code-agent/backend/app/integrity/plugins/doc_audit/rules \
         /Users/jay/Developer/claude-code-agent/backend/tests/integrity/plugins/doc_audit/parser \
         /Users/jay/Developer/claude-code-agent/backend/tests/integrity/plugins/doc_audit/rules
for f in \
  backend/app/integrity/plugins/doc_audit/__init__.py \
  backend/app/integrity/plugins/doc_audit/parser/__init__.py \
  backend/app/integrity/plugins/doc_audit/rules/__init__.py \
  backend/tests/integrity/plugins/doc_audit/__init__.py \
  backend/tests/integrity/plugins/doc_audit/parser/__init__.py \
  backend/tests/integrity/plugins/doc_audit/rules/__init__.py; do
    : > /Users/jay/Developer/claude-code-agent/$f
done
```

- [ ] **Step 3: Verify import works**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && uv run python -c "import markdown_it; print(markdown_it.__version__)"
```

Expected: prints version `>=3.0`.

- [ ] **Step 4: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/pyproject.toml backend/uv.lock \
  backend/app/integrity/plugins/doc_audit \
  backend/tests/integrity/plugins/doc_audit && \
git commit -m "chore(integrity): scaffold doc_audit plugin + add markdown-it-py dep"
```

---

### Task 2: Config defaults for doc_audit

**Files:**
- Modify: `backend/app/integrity/config.py:11` (the `DEFAULTS` dict)
- Modify: `config/integrity.yaml`
- Test: `backend/tests/integrity/test_config.py` (existing test file — add new test)

- [ ] **Step 1: Write the failing test**

Append to `backend/tests/integrity/test_config.py`:

```python
def test_doc_audit_defaults_present(tmp_path):
    from backend.app.integrity.config import load_config

    cfg = load_config(tmp_path)
    da = cfg.plugins["doc_audit"]
    assert da["enabled"] is True
    assert da["thresholds"]["stale_days"] == 90
    assert "dev-setup.md" in da["coverage_required"]
    assert "testing.md" in da["coverage_required"]
    assert "gotchas.md" in da["coverage_required"]
    assert "skill-creation.md" in da["coverage_required"]
    assert "log.md" in da["coverage_required"]
    assert da["seed_docs"] == ["CLAUDE.md"]
    assert "docs/**/*.md" in da["doc_roots"]
    assert "knowledge/**/*.md" in da["doc_roots"]
    assert "*.md" in da["doc_roots"]
    assert "reference/**" in da["excluded_paths"]
    assert "docs/health/**" in da["excluded_paths"]
    assert "docs/superpowers/**" in da["excluded_paths"]
    assert da["claude_ignore_file"] == ".claude-ignore"
    assert da["rename_lookback"] == "30.days.ago"
    assert da["disabled_rules"] == []
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/test_config.py::test_doc_audit_defaults_present -v
```

Expected: FAIL with `KeyError: 'doc_audit'`.

- [ ] **Step 3: Add doc_audit defaults to config.py**

Edit `backend/app/integrity/config.py`. In the `DEFAULTS` dict (starts at line 11), add a new key under `"plugins"`:

```python
"doc_audit": {
    "enabled": True,
    "thresholds": {
        "stale_days": 90,
    },
    "coverage_required": [
        "dev-setup.md",
        "testing.md",
        "gotchas.md",
        "skill-creation.md",
        "log.md",
    ],
    "seed_docs": ["CLAUDE.md"],
    "doc_roots": [
        "docs/**/*.md",
        "knowledge/**/*.md",
        "*.md",
    ],
    "excluded_paths": [
        "reference/**",
        "node_modules/**",
        "**/__pycache__/**",
        "integrity-out/**",
        "docs/health/**",
        "docs/superpowers/**",
    ],
    "claude_ignore_file": ".claude-ignore",
    "rename_lookback": "30.days.ago",
    "disabled_rules": [],
},
```

- [ ] **Step 4: Add doc_audit block to config/integrity.yaml**

Append to `config/integrity.yaml`:

```yaml
  doc_audit:
    enabled: true
    thresholds:
      stale_days: 90
    coverage_required:
      - dev-setup.md
      - testing.md
      - gotchas.md
      - skill-creation.md
      - log.md
    seed_docs:
      - CLAUDE.md
    doc_roots:
      - "docs/**/*.md"
      - "knowledge/**/*.md"
      - "*.md"
    excluded_paths:
      - "reference/**"
      - "node_modules/**"
      - "**/__pycache__/**"
      - "integrity-out/**"
      - "docs/health/**"
      - "docs/superpowers/**"
    claude_ignore_file: ".claude-ignore"
    rename_lookback: "30.days.ago"
    disabled_rules: []
```

- [ ] **Step 5: Run test to verify it passes**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/test_config.py::test_doc_audit_defaults_present -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/app/integrity/config.py config/integrity.yaml \
  backend/tests/integrity/test_config.py && \
git commit -m "feat(integrity): add doc_audit config defaults"
```

---

### Task 3: Parser — markdown.py (markdown-it-py wrapper)

**Files:**
- Create: `backend/app/integrity/plugins/doc_audit/parser/markdown.py`
- Test: `backend/tests/integrity/plugins/doc_audit/parser/test_markdown.py`

- [ ] **Step 1: Write the failing test**

Create `backend/tests/integrity/plugins/doc_audit/parser/test_markdown.py`:

```python
from pathlib import Path

from backend.app.integrity.plugins.doc_audit.parser.markdown import (
    Heading,
    MarkdownLink,
    parse_doc,
    slug_for_heading,
)


def test_slug_for_heading_lowercases_and_hyphenates():
    assert slug_for_heading("My Section") == "my-section"
    assert slug_for_heading("API / Routes") == "api--routes"
    assert slug_for_heading("Hello, World!") == "hello-world"
    assert slug_for_heading("  Trim Me  ") == "trim-me"
    assert slug_for_heading("Numbers 123 OK") == "numbers-123-ok"


def test_parse_doc_extracts_headings_and_links(tmp_path: Path):
    md = tmp_path / "sample.md"
    md.write_text(
        "---\nstatus: accepted\n---\n\n"
        "# Top Heading\n\n"
        "Some prose with [a link](other.md) and an [anchor link](other.md#section).\n\n"
        "## Sub Heading\n\n"
        "Another [absolute](https://example.com/x) and an [in-page](#top-heading).\n\n"
        "```python\n"
        "# This code block should not produce link extractions\n"
        "[fake](should-not-extract.md)\n"
        "```\n",
        encoding="utf-8",
    )

    parsed = parse_doc(md, rel_path="sample.md")

    assert parsed.rel_path == "sample.md"
    assert parsed.front_matter == {"status": "accepted"}
    assert any(h.text == "Top Heading" and h.slug == "top-heading" and h.level == 1 for h in parsed.headings)
    assert any(h.text == "Sub Heading" and h.slug == "sub-heading" and h.level == 2 for h in parsed.headings)

    targets = [(link.target, link.anchor) for link in parsed.links]
    assert ("other.md", None) in targets
    assert ("other.md", "section") in targets
    assert ("https://example.com/x", None) in targets
    assert ("", "top-heading") in targets
    assert not any("should-not-extract.md" in (link.target or "") for link in parsed.links)


def test_parse_doc_handles_missing_front_matter(tmp_path: Path):
    md = tmp_path / "plain.md"
    md.write_text("# Hello\n\nNo front matter here.\n", encoding="utf-8")
    parsed = parse_doc(md, rel_path="plain.md")
    assert parsed.front_matter == {}
    assert parsed.headings[0].text == "Hello"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/parser/test_markdown.py -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement parser/markdown.py**

Create `backend/app/integrity/plugins/doc_audit/parser/markdown.py`:

```python
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from markdown_it import MarkdownIt
from markdown_it.token import Token


@dataclass(frozen=True)
class Heading:
    text: str
    slug: str
    level: int


@dataclass(frozen=True)
class MarkdownLink:
    target: str
    anchor: str | None
    text: str
    line: int  # 1-based source line


@dataclass(frozen=True)
class ParsedDoc:
    path: Path
    rel_path: str
    headings: list[Heading]
    links: list[MarkdownLink]
    front_matter: dict[str, Any]
    raw_text: str


_SLUG_KEEP = re.compile(r"[^a-z0-9\- ]+")
_SLUG_WHITE = re.compile(r"\s+")
_FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def slug_for_heading(text: str) -> str:
    """GitHub-style slug: lowercase, drop punctuation (keep `-`), spaces → `-`."""
    s = text.strip().lower()
    s = _SLUG_KEEP.sub("", s)
    s = _SLUG_WHITE.sub("-", s)
    return s


def _strip_front_matter(text: str) -> tuple[dict[str, Any], str]:
    m = _FRONT_MATTER_RE.match(text)
    if not m:
        return {}, text
    try:
        data = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        data = {}
    if not isinstance(data, dict):
        data = {}
    return data, text[m.end():]


def _heading_text(tokens: list[Token], idx: int) -> str:
    inline = tokens[idx + 1] if idx + 1 < len(tokens) else None
    if inline is None or inline.type != "inline":
        return ""
    parts: list[str] = []
    for child in inline.children or []:
        if child.type == "text":
            parts.append(child.content)
        elif child.type == "code_inline":
            parts.append(child.content)
    return "".join(parts).strip()


def parse_doc(path: Path, rel_path: str) -> ParsedDoc:
    raw = path.read_text(encoding="utf-8", errors="replace")
    fm, body = _strip_front_matter(raw)
    md = MarkdownIt("commonmark", {"html": False})
    tokens = md.parse(body)

    headings: list[Heading] = []
    links: list[MarkdownLink] = []

    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok.type == "heading_open":
            level = int(tok.tag.lstrip("h"))
            text = _heading_text(tokens, i)
            slug = slug_for_heading(text)
            headings.append(Heading(text=text, slug=slug, level=level))
        elif tok.type == "inline" and tok.children:
            j = 0
            children = tok.children
            line = (tok.map[0] + 1) if tok.map else 0
            while j < len(children):
                ch = children[j]
                if ch.type == "link_open":
                    href = ""
                    for name, value in ch.attrs.items() if isinstance(ch.attrs, dict) else (ch.attrs or []):
                        if name == "href":
                            href = value
                    text_parts: list[str] = []
                    k = j + 1
                    while k < len(children) and children[k].type != "link_close":
                        if children[k].type == "text":
                            text_parts.append(children[k].content)
                        k += 1
                    target = href
                    anchor: str | None = None
                    if "#" in href:
                        target, anchor = href.split("#", 1)
                        anchor = anchor or None
                    links.append(
                        MarkdownLink(
                            target=target,
                            anchor=anchor,
                            text="".join(text_parts).strip(),
                            line=line,
                        )
                    )
                    j = k
                j += 1
        i += 1

    return ParsedDoc(
        path=path,
        rel_path=rel_path,
        headings=headings,
        links=links,
        front_matter=fm,
        raw_text=raw,
    )
```

Note on `ch.attrs` shape: in `markdown-it-py >= 3`, `Token.attrs` is a `dict[str, str]`. The compatibility loop above tolerates both shapes.

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/parser/test_markdown.py -v
```

Expected: 3 PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/app/integrity/plugins/doc_audit/parser/markdown.py \
  backend/tests/integrity/plugins/doc_audit/parser/test_markdown.py && \
git commit -m "feat(integrity): doc_audit markdown parser"
```

---

### Task 4: Parser — code_refs.py

**Files:**
- Create: `backend/app/integrity/plugins/doc_audit/parser/code_refs.py`
- Test: `backend/tests/integrity/plugins/doc_audit/parser/test_code_refs.py`

- [ ] **Step 1: Write the failing test**

Create `backend/tests/integrity/plugins/doc_audit/parser/test_code_refs.py`:

```python
from backend.app.integrity.plugins.doc_audit.parser.code_refs import (
    CodeRef,
    extract_code_refs,
)


def test_extracts_path_line_pattern():
    text = "See `backend/app/foo.py:42` for the function."
    refs = extract_code_refs(text)
    matching = [r for r in refs if r.kind == "path_line"]
    assert any(r.path == "backend/app/foo.py" and r.line == 42 for r in matching)


def test_extracts_path_pattern_with_slash_required():
    text = "Open `backend/app/foo.py` and edit it. Also see `bar.py` (no slash, ignored)."
    refs = extract_code_refs(text)
    paths = {r.path for r in refs if r.kind == "path"}
    assert "backend/app/foo.py" in paths
    # bare `bar.py` lacks `/` → not captured as path
    assert "bar.py" not in paths


def test_extracts_qualified_symbol():
    text = "Calls `Module.do_thing` and `pkg.sub.func`."
    refs = extract_code_refs(text)
    syms = {r.symbol for r in refs if r.kind == "symbol"}
    assert "Module.do_thing" in syms
    assert "pkg.sub.func" in syms


def test_skips_fenced_code_blocks():
    text = (
        "Above the fence: `path/foo.py`.\n\n"
        "```python\n"
        "# `path/inside_fence.py` should be skipped\n"
        "```\n\n"
        "Below the fence: `path/bar.py`.\n"
    )
    refs = extract_code_refs(text)
    paths = {r.path for r in refs if r.kind == "path"}
    assert "path/foo.py" in paths
    assert "path/bar.py" in paths
    assert "path/inside_fence.py" not in paths


def test_skips_inline_indented_code_blocks():
    text = "Normal `path/a.py`\n\n    `path/indented.py` is in indented code\n\nAnd `path/b.py`.\n"
    refs = extract_code_refs(text)
    paths = {r.path for r in refs if r.kind == "path"}
    assert "path/a.py" in paths
    assert "path/b.py" in paths
    assert "path/indented.py" not in paths


def test_does_not_match_bare_unqualified_word():
    text = "The word `config` should not match as a symbol candidate."
    refs = extract_code_refs(text)
    syms = {r.symbol for r in refs if r.kind == "symbol"}
    # `config` lacks `.`, so not extracted as a qualified symbol candidate
    assert "config" not in syms


def test_source_line_recorded():
    text = "first line\nsecond `path/x.py:7` line\nthird line\n"
    refs = extract_code_refs(text)
    pl = [r for r in refs if r.kind == "path_line"][0]
    assert pl.source_line == 2
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/parser/test_code_refs.py -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement parser/code_refs.py**

Create `backend/app/integrity/plugins/doc_audit/parser/code_refs.py`:

```python
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

CodeRefKind = Literal["path", "path_line", "symbol"]


@dataclass(frozen=True)
class CodeRef:
    text: str
    kind: CodeRefKind
    path: str | None
    line: int | None
    symbol: str | None
    source_line: int  # 1-based line in the doc


_PATH_LINE_RE = re.compile(r"`([\w./\-]+\.[A-Za-z]{1,5}):(\d+)`")
_PATH_RE = re.compile(r"`([\w./\-]+/[\w./\-]+\.[A-Za-z]{1,5})`")
_SYMBOL_RE = re.compile(r"`([A-Za-z_][\w]*(?:\.[A-Za-z_][\w]*)+)`")
_FENCE_RE = re.compile(r"^(?:```|~~~)")


def _strip_code_blocks(text: str) -> list[tuple[int, str]]:
    """Yield `(line_number_1based, content)` for lines OUTSIDE fenced or
    indented code blocks. Inline backticks on a non-code line still flow through."""
    out: list[tuple[int, str]] = []
    in_fence = False
    for idx, line in enumerate(text.splitlines(), start=1):
        if _FENCE_RE.match(line.lstrip()):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # Indented code block: 4+ leading spaces (or 1 tab) on an otherwise blank-led line
        if line.startswith("    ") or line.startswith("\t"):
            continue
        out.append((idx, line))
    return out


def extract_code_refs(text: str) -> list[CodeRef]:
    refs: list[CodeRef] = []
    seen: set[tuple[str, int, str | None]] = set()
    for line_no, line in _strip_code_blocks(text):
        for m in _PATH_LINE_RE.finditer(line):
            path, line_str = m.group(1), m.group(2)
            key = ("path_line", line_no, f"{path}:{line_str}")
            if key in seen:
                continue
            seen.add(key)
            refs.append(
                CodeRef(
                    text=m.group(0),
                    kind="path_line",
                    path=path,
                    line=int(line_str),
                    symbol=None,
                    source_line=line_no,
                )
            )
        for m in _PATH_RE.finditer(line):
            path = m.group(1)
            key = ("path", line_no, path)
            if key in seen:
                continue
            # Skip if this match is the prefix of a path:line we already captured
            if any(
                r.kind == "path_line" and r.source_line == line_no and r.path == path
                for r in refs
            ):
                continue
            seen.add(key)
            refs.append(
                CodeRef(
                    text=m.group(0),
                    kind="path",
                    path=path,
                    line=None,
                    symbol=None,
                    source_line=line_no,
                )
            )
        for m in _SYMBOL_RE.finditer(line):
            symbol = m.group(1)
            # Symbol pattern requires at least one `.` (enforced by `+` in regex)
            key = ("symbol", line_no, symbol)
            if key in seen:
                continue
            # Skip if symbol overlaps a captured path on the same line
            if any(
                r.source_line == line_no
                and r.path is not None
                and symbol in r.path
                for r in refs
            ):
                continue
            seen.add(key)
            refs.append(
                CodeRef(
                    text=m.group(0),
                    kind="symbol",
                    path=None,
                    line=None,
                    symbol=symbol,
                    source_line=line_no,
                )
            )
    return refs
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/parser/test_code_refs.py -v
```

Expected: 7 PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/app/integrity/plugins/doc_audit/parser/code_refs.py \
  backend/tests/integrity/plugins/doc_audit/parser/test_code_refs.py && \
git commit -m "feat(integrity): doc_audit code-ref extraction"
```

---

### Task 5: Parser — git_log.py

**Files:**
- Create: `backend/app/integrity/plugins/doc_audit/parser/git_log.py`
- Test: `backend/tests/integrity/plugins/doc_audit/parser/test_git_log.py`

- [ ] **Step 1: Write the failing test**

Create `backend/tests/integrity/plugins/doc_audit/parser/test_git_log.py`:

```python
import subprocess
from pathlib import Path

import pytest

from backend.app.integrity.plugins.doc_audit.parser.git_log import GitLog


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(cwd), check=True, capture_output=True)


@pytest.fixture
def tiny_git_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "test")
    (repo / "a.txt").write_text("hello\n")
    _git(repo, "add", "a.txt")
    _git(repo, "commit", "-q", "-m", "initial")
    return repo


def test_returns_iso_timestamp_for_committed_file(tiny_git_repo: Path):
    gl = GitLog(tiny_git_repo)
    iso = gl.last_commit_iso("a.txt")
    assert iso is not None
    # Strict ISO 8601-ish: starts with YYYY-MM-DD
    assert len(iso) >= 10 and iso[4] == "-" and iso[7] == "-"


def test_returns_none_for_unknown_path(tiny_git_repo: Path):
    gl = GitLog(tiny_git_repo)
    assert gl.last_commit_iso("does/not/exist.txt") is None


def test_returns_none_when_not_a_git_repo(tmp_path: Path):
    not_a_repo = tmp_path / "plain"
    not_a_repo.mkdir()
    (not_a_repo / "a.txt").write_text("hi\n")
    gl = GitLog(not_a_repo)
    assert gl.last_commit_iso("a.txt") is None


def test_caches_results(tiny_git_repo: Path):
    gl = GitLog(tiny_git_repo)
    first = gl.last_commit_iso("a.txt")
    second = gl.last_commit_iso("a.txt")
    assert first == second
    # Cache hit: same dict-stored value identity
    assert gl._cache["a.txt"] == first
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/parser/test_git_log.py -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement parser/git_log.py**

Create `backend/app/integrity/plugins/doc_audit/parser/git_log.py`:

```python
from __future__ import annotations

import subprocess
from pathlib import Path


class GitLog:
    """Cached `git log -1 --format=%cI` for repo-relative paths.

    Returns ISO 8601 committer date (e.g. `2026-04-17T03:21:18+00:00`) or
    `None` if the path is unknown to git, the repo has no history, or git
    is unavailable.
    """

    def __init__(self, repo_root: Path, *, git_bin: str = "git") -> None:
        self.repo_root = repo_root
        self.git_bin = git_bin
        self._cache: dict[str, str | None] = {}

    def last_commit_iso(self, rel_path: str) -> str | None:
        if rel_path in self._cache:
            return self._cache[rel_path]
        cmd = [self.git_bin, "log", "-1", "--format=%cI", "--", rel_path]
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(self.repo_root),
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            self._cache[rel_path] = None
            return None
        out = proc.stdout.strip()
        result = out if (proc.returncode == 0 and out) else None
        self._cache[rel_path] = result
        return result
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/parser/test_git_log.py -v
```

Expected: 4 PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/app/integrity/plugins/doc_audit/parser/git_log.py \
  backend/tests/integrity/plugins/doc_audit/parser/test_git_log.py && \
git commit -m "feat(integrity): doc_audit git-log helper with caching"
```

---

### Task 6: Parser — ignore.py (.claude-ignore matcher)

**Files:**
- Create: `backend/app/integrity/plugins/doc_audit/parser/ignore.py`
- Test: `backend/tests/integrity/plugins/doc_audit/parser/test_ignore.py`

- [ ] **Step 1: Write the failing test**

Create `backend/tests/integrity/plugins/doc_audit/parser/test_ignore.py`:

```python
from pathlib import Path

from backend.app.integrity.plugins.doc_audit.parser.ignore import IgnoreMatcher


def test_empty_when_file_missing(tmp_path: Path):
    matcher = IgnoreMatcher.load(tmp_path / "missing", repo_root=tmp_path)
    assert not matcher.matches("docs/anything.md")
    assert matcher.patterns == ()


def test_matches_glob_patterns(tmp_path: Path):
    ignore = tmp_path / ".claude-ignore"
    ignore.write_text(
        "# top comment\n"
        "docs/draft/**\n"
        "knowledge/wiki/scratch/*.md\n"
        "\n"  # blank line
        "*.tmp.md\n",
        encoding="utf-8",
    )
    matcher = IgnoreMatcher.load(ignore, repo_root=tmp_path)
    assert matcher.matches("docs/draft/notes.md")
    assert matcher.matches("docs/draft/sub/deep.md")
    assert matcher.matches("knowledge/wiki/scratch/idea.md")
    assert matcher.matches("anything.tmp.md")
    assert not matcher.matches("docs/dev-setup.md")
    assert not matcher.matches("knowledge/wiki/working.md")


def test_normalizes_windows_separators(tmp_path: Path):
    ignore = tmp_path / ".claude-ignore"
    ignore.write_text("docs/draft/**\n", encoding="utf-8")
    matcher = IgnoreMatcher.load(ignore, repo_root=tmp_path)
    assert matcher.matches("docs\\draft\\notes.md")
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/parser/test_ignore.py -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement parser/ignore.py**

Create `backend/app/integrity/plugins/doc_audit/parser/ignore.py`:

```python
from __future__ import annotations

import fnmatch
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class IgnoreMatcher:
    patterns: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def load(cls, file_path: Path, *, repo_root: Path) -> IgnoreMatcher:
        if not file_path.exists():
            return cls(patterns=())
        text = file_path.read_text(encoding="utf-8", errors="replace")
        patterns: list[str] = []
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(line)
        return cls(patterns=tuple(patterns))

    def matches(self, rel_path: str) -> bool:
        normalized = rel_path.replace("\\", "/")
        for pat in self.patterns:
            if _glob_match(normalized, pat):
                return True
        return False


def _glob_match(path: str, pattern: str) -> bool:
    # Normalize gitignore-style `**` to fnmatch-friendly form.
    # We translate `dir/**` so that it matches `dir/anything/under/here`.
    pattern_norm = pattern.replace("\\", "/")
    if pattern_norm.endswith("/**"):
        prefix = pattern_norm[: -len("/**")]
        return path == prefix or path.startswith(prefix + "/")
    if "**" in pattern_norm:
        # Translate `a/**/b.md` → regex by hand: split on `**`
        parts = pattern_norm.split("**")
        # fnmatch.translate handles `*` but not `**`; emulate with substring tests
        # Simple form: anchor first part, last part, allow any depth between
        if len(parts) == 2:
            head, tail = parts[0].rstrip("/"), parts[1].lstrip("/")
            if head and not (path == head or path.startswith(head + "/")):
                return False
            return path.endswith(tail) if tail else True
    return fnmatch.fnmatch(path, pattern_norm)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/parser/test_ignore.py -v
```

Expected: 3 PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/app/integrity/plugins/doc_audit/parser/ignore.py \
  backend/tests/integrity/plugins/doc_audit/parser/test_ignore.py && \
git commit -m "feat(integrity): doc_audit .claude-ignore matcher"
```

---

### Task 7: MarkdownIndex builder

**Files:**
- Create: `backend/app/integrity/plugins/doc_audit/index.py`
- Test: `backend/tests/integrity/plugins/doc_audit/test_index.py`

- [ ] **Step 1: Write the failing test**

Create `backend/tests/integrity/plugins/doc_audit/test_index.py`:

```python
from pathlib import Path

from backend.app.integrity.plugins.doc_audit.index import MarkdownIndex


def _write(repo: Path, rel: str, content: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def test_builds_link_graph_and_indexes_anchors(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# Index\n\n- [Setup](docs/dev-setup.md)\n- [Test](docs/testing.md)\n")
    _write(tmp_path, "docs/dev-setup.md", "## Quick Start\n\nGo to [testing](testing.md#fast).\n")
    _write(tmp_path, "docs/testing.md", "## Fast\n\nSomething.\n")
    _write(tmp_path, "docs/orphan.md", "Not linked from anywhere.\n")

    cfg = {
        "doc_roots": ["*.md", "docs/**/*.md"],
        "excluded_paths": [],
        "claude_ignore_file": ".claude-ignore",
    }
    idx = MarkdownIndex.build(tmp_path, cfg)

    assert "CLAUDE.md" in idx.docs
    assert "docs/dev-setup.md" in idx.docs
    assert "docs/testing.md" in idx.docs
    assert "docs/orphan.md" in idx.docs
    assert idx.link_graph["CLAUDE.md"] >= {"docs/dev-setup.md", "docs/testing.md"}
    assert idx.link_graph["docs/dev-setup.md"] >= {"docs/testing.md"}
    assert "fast" in idx.anchors_by_path["docs/testing.md"]


def test_excluded_paths_drop_files(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# X\n")
    _write(tmp_path, "docs/health/latest.md", "# generated\n")
    _write(tmp_path, "docs/dev-setup.md", "# real\n")
    cfg = {
        "doc_roots": ["*.md", "docs/**/*.md"],
        "excluded_paths": ["docs/health/**"],
        "claude_ignore_file": ".claude-ignore",
    }
    idx = MarkdownIndex.build(tmp_path, cfg)
    assert "docs/dev-setup.md" in idx.docs
    assert "docs/health/latest.md" not in idx.docs
    assert "docs/health/latest.md" in idx.excluded


def test_ignored_paths_loaded_from_claude_ignore(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# X\n")
    _write(tmp_path, ".claude-ignore", "docs/draft/**\n")
    _write(tmp_path, "docs/draft/foo.md", "# draft\n")
    _write(tmp_path, "docs/published.md", "# published\n")
    cfg = {
        "doc_roots": ["*.md", "docs/**/*.md"],
        "excluded_paths": [],
        "claude_ignore_file": ".claude-ignore",
    }
    idx = MarkdownIndex.build(tmp_path, cfg)
    assert "docs/draft/foo.md" in idx.docs   # still parsed
    assert "docs/draft/foo.md" in idx.ignored
    assert "docs/published.md" not in idx.ignored
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/test_index.py -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement index.py**

Create `backend/app/integrity/plugins/doc_audit/index.py`:

```python
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any

from .parser.ignore import IgnoreMatcher
from .parser.markdown import ParsedDoc, parse_doc


@dataclass(frozen=True)
class MarkdownIndex:
    docs: dict[str, ParsedDoc]
    anchors_by_path: dict[str, set[str]]
    link_graph: dict[str, set[str]]
    excluded: frozenset[str]
    ignored: frozenset[str]
    repo_root: Path

    @classmethod
    def build(cls, repo_root: Path, plugin_cfg: dict[str, Any]) -> MarkdownIndex:
        roots: list[str] = list(plugin_cfg.get("doc_roots", []))
        excluded_globs: list[str] = list(plugin_cfg.get("excluded_paths", []))
        ignore_file = plugin_cfg.get("claude_ignore_file", ".claude-ignore")

        ignore_matcher = IgnoreMatcher.load(repo_root / ignore_file, repo_root=repo_root)
        candidates = _collect_candidates(repo_root, roots)
        excluded: set[str] = set()
        keep: list[Path] = []
        for path in candidates:
            rel = _rel(path, repo_root)
            if _matches_any(rel, excluded_globs):
                excluded.add(rel)
                continue
            keep.append(path)

        docs: dict[str, ParsedDoc] = {}
        ignored: set[str] = set()
        for path in keep:
            rel = _rel(path, repo_root)
            try:
                parsed = parse_doc(path, rel_path=rel)
            except Exception:
                continue
            docs[rel] = parsed
            if ignore_matcher.matches(rel):
                ignored.add(rel)

        anchors_by_path: dict[str, set[str]] = {
            rel: {h.slug for h in parsed.headings if h.slug}
            for rel, parsed in docs.items()
        }

        link_graph: dict[str, set[str]] = defaultdict(set)
        for rel, parsed in docs.items():
            base_dir = PurePosixPath(rel).parent
            for link in parsed.links:
                if not link.target:
                    continue
                target_lower = link.target.lower()
                if target_lower.startswith(("http://", "https://", "mailto:", "ftp://")):
                    continue
                if not link.target.endswith(".md"):
                    continue
                resolved = _resolve(base_dir, link.target)
                if resolved:
                    link_graph[rel].add(resolved)

        return cls(
            docs=docs,
            anchors_by_path=anchors_by_path,
            link_graph=dict(link_graph),
            excluded=frozenset(excluded),
            ignored=frozenset(ignored),
            repo_root=repo_root,
        )


def _rel(p: Path, repo_root: Path) -> str:
    return p.relative_to(repo_root).as_posix()


def _collect_candidates(repo_root: Path, roots: list[str]) -> list[Path]:
    seen: set[Path] = set()
    out: list[Path] = []
    for pattern in roots:
        for p in sorted(repo_root.glob(pattern)):
            if p.is_file() and p.suffix == ".md" and p not in seen:
                seen.add(p)
                out.append(p)
    return out


def _matches_any(rel: str, patterns: list[str]) -> bool:
    from .parser.ignore import _glob_match  # reuse the same matcher

    for pat in patterns:
        if _glob_match(rel, pat):
            return True
    return False


def _resolve(base_dir: PurePosixPath, target: str) -> str | None:
    try:
        joined = (base_dir / target).resolve()
        # PurePosixPath.resolve doesn't normalize `..` without filesystem;
        # use a manual normalization
        parts: list[str] = []
        for part in (base_dir / target).parts:
            if part == "..":
                if parts:
                    parts.pop()
                else:
                    return None
            elif part == ".":
                continue
            else:
                parts.append(part)
        return PurePosixPath(*parts).as_posix() if parts else None
    except Exception:
        return None
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/test_index.py -v
```

Expected: 3 PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/app/integrity/plugins/doc_audit/index.py \
  backend/tests/integrity/plugins/doc_audit/test_index.py && \
git commit -m "feat(integrity): doc_audit MarkdownIndex builder"
```

---

### Task 8: Plugin shell — DocAuditPlugin

**Files:**
- Create: `backend/app/integrity/plugins/doc_audit/plugin.py`
- Test: `backend/tests/integrity/plugins/doc_audit/test_plugin.py` (initial smoke; full integration test in Task 16)

- [ ] **Step 1: Write the failing test**

Create `backend/tests/integrity/plugins/doc_audit/test_plugin.py`:

```python
from datetime import date
from pathlib import Path

from backend.app.integrity.plugins.doc_audit.plugin import DocAuditPlugin
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


def _empty_graph(repo_root: Path) -> None:
    g = repo_root / "graphify"
    g.mkdir(parents=True, exist_ok=True)
    (g / "graph.json").write_text('{"nodes":[],"links":[]}', encoding="utf-8")


def test_plugin_runs_with_no_docs_and_no_rules_registered(tmp_path: Path):
    _empty_graph(tmp_path)
    cfg = {
        "doc_roots": ["docs/**/*.md"],
        "excluded_paths": [],
        "claude_ignore_file": ".claude-ignore",
        "seed_docs": ["CLAUDE.md"],
        "thresholds": {"stale_days": 90},
        "coverage_required": [],
        "rename_lookback": "30.days.ago",
        "disabled_rules": [],
    }
    plugin = DocAuditPlugin(config=cfg, today=date(2026, 4, 17), rules={})
    ctx = ScanContext(repo_root=tmp_path, graph=GraphSnapshot.load(tmp_path))
    result = plugin.scan(ctx)

    assert result.plugin_name == "doc_audit"
    assert result.plugin_version == "1.0.0"
    assert result.issues == []
    assert result.failures == []
    artifact = tmp_path / "integrity-out" / "2026-04-17" / "doc_audit.json"
    assert artifact.exists()
    assert artifact in result.artifacts


def test_plugin_catches_rule_exception(tmp_path: Path):
    _empty_graph(tmp_path)
    cfg = {
        "doc_roots": [],
        "excluded_paths": [],
        "claude_ignore_file": ".claude-ignore",
        "seed_docs": ["CLAUDE.md"],
        "thresholds": {"stale_days": 90},
        "coverage_required": [],
        "rename_lookback": "30.days.ago",
        "disabled_rules": [],
    }

    def boom(ctx, plugin_cfg, today):
        raise RuntimeError("boom")

    plugin = DocAuditPlugin(
        config=cfg, today=date(2026, 4, 17), rules={"doc.boom": boom}
    )
    ctx = ScanContext(repo_root=tmp_path, graph=GraphSnapshot.load(tmp_path))
    result = plugin.scan(ctx)

    assert any(i.severity == "ERROR" and i.rule == "doc.boom" for i in result.issues)
    assert any("doc.boom" in f and "RuntimeError" in f for f in result.failures)


def test_plugin_skips_disabled_rules(tmp_path: Path):
    _empty_graph(tmp_path)
    cfg = {
        "doc_roots": [],
        "excluded_paths": [],
        "claude_ignore_file": ".claude-ignore",
        "seed_docs": ["CLAUDE.md"],
        "thresholds": {"stale_days": 90},
        "coverage_required": [],
        "rename_lookback": "30.days.ago",
        "disabled_rules": ["doc.boom"],
    }
    called = {"count": 0}

    def boom(ctx, plugin_cfg, today):
        called["count"] += 1
        raise RuntimeError("boom")

    plugin = DocAuditPlugin(
        config=cfg, today=date(2026, 4, 17), rules={"doc.boom": boom}
    )
    plugin.scan(ScanContext(repo_root=tmp_path, graph=GraphSnapshot.load(tmp_path)))
    assert called["count"] == 0
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/test_plugin.py -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement plugin.py**

Create `backend/app/integrity/plugins/doc_audit/plugin.py`:

```python
from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import date
from typing import Any

from ...issue import IntegrityIssue
from ...protocol import ScanContext, ScanResult

Rule = Callable[[ScanContext, dict[str, Any], date], list[IntegrityIssue]]


def _default_rules() -> dict[str, Rule]:
    from .rules import (
        adr_status_drift,
        broken_link,
        coverage_gap,
        dead_code_ref,
        stale_candidate,
        unindexed,
    )

    return {
        "doc.coverage_gap": coverage_gap.run,
        "doc.unindexed": unindexed.run,
        "doc.broken_link": broken_link.run,
        "doc.dead_code_ref": dead_code_ref.run,
        "doc.stale_candidate": stale_candidate.run,
        "doc.adr_status_drift": adr_status_drift.run,
    }


@dataclass
class DocAuditPlugin:
    name: str = "doc_audit"
    version: str = "1.0.0"
    depends_on: tuple[str, ...] = ("graph_extension",)
    paths: tuple[str, ...] = (
        "docs/**/*.md",
        "knowledge/**/*.md",
        "CLAUDE.md",
        "*.md",
    )
    config: dict[str, Any] = field(default_factory=dict)
    today: date = field(default_factory=date.today)
    rules: dict[str, Rule] | None = None

    def scan(self, ctx: ScanContext) -> ScanResult:
        rules = self.rules if self.rules is not None else _default_rules()
        disabled = set(self.config.get("disabled_rules", []))

        all_issues: list[IntegrityIssue] = []
        rules_run: list[str] = []
        failures: list[str] = []

        for rule_id, fn in rules.items():
            if rule_id in disabled:
                continue
            try:
                issues = fn(ctx, self.config, self.today)
                all_issues.extend(issues)
                rules_run.append(rule_id)
            except Exception as exc:
                failures.append(f"{rule_id}: {type(exc).__name__}: {exc}")
                all_issues.append(
                    IntegrityIssue(
                        rule=rule_id,
                        severity="ERROR",
                        node_id="<rule-failure>",
                        location=f"doc_audit/{rule_id}",
                        message=f"{type(exc).__name__}: {exc}",
                    )
                )

        run_dir = ctx.repo_root / "integrity-out" / self.today.isoformat()
        run_dir.mkdir(parents=True, exist_ok=True)
        artifact = run_dir / "doc_audit.json"
        artifact.write_text(
            json.dumps(
                {
                    "date": self.today.isoformat(),
                    "rules_run": rules_run,
                    "failures": failures,
                    "issues": [i.to_dict() for i in all_issues],
                },
                indent=2,
                sort_keys=True,
            )
        )

        return ScanResult(
            plugin_name=self.name,
            plugin_version=self.version,
            issues=all_issues,
            artifacts=[artifact],
            failures=failures,
        )
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/test_plugin.py -v
```

Expected: 3 PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/app/integrity/plugins/doc_audit/plugin.py \
  backend/tests/integrity/plugins/doc_audit/test_plugin.py && \
git commit -m "feat(integrity): doc_audit plugin shell with per-rule try/except"
```

---

### Task 9: Rule — coverage_gap

**Files:**
- Create: `backend/app/integrity/plugins/doc_audit/rules/coverage_gap.py`
- Test: `backend/tests/integrity/plugins/doc_audit/rules/test_coverage_gap.py`

- [ ] **Step 1: Write the failing test**

Create `backend/tests/integrity/plugins/doc_audit/rules/test_coverage_gap.py`:

```python
from datetime import date
from pathlib import Path

from backend.app.integrity.plugins.doc_audit.rules.coverage_gap import run
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


def _ctx(tmp_path: Path) -> ScanContext:
    g = tmp_path / "graphify"
    g.mkdir(parents=True, exist_ok=True)
    (g / "graph.json").write_text('{"nodes":[],"links":[]}', encoding="utf-8")
    return ScanContext(repo_root=tmp_path, graph=GraphSnapshot.load(tmp_path))


def test_no_issues_when_all_required_present(tmp_path: Path):
    docs = tmp_path / "docs"
    docs.mkdir()
    for name in ("dev-setup.md", "testing.md", "gotchas.md", "skill-creation.md", "log.md"):
        (docs / name).write_text("# x\n")

    cfg = {
        "coverage_required": [
            "dev-setup.md",
            "testing.md",
            "gotchas.md",
            "skill-creation.md",
            "log.md",
        ],
    }
    issues = run(_ctx(tmp_path), cfg, date(2026, 4, 17))
    assert issues == []


def test_missing_files_emit_one_issue_each(tmp_path: Path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "dev-setup.md").write_text("# x\n")
    # testing.md and log.md missing

    cfg = {"coverage_required": ["dev-setup.md", "testing.md", "log.md"]}
    issues = run(_ctx(tmp_path), cfg, date(2026, 4, 17))
    assert len(issues) == 2
    rules = {i.rule for i in issues}
    assert rules == {"doc.coverage_gap"}
    locations = {i.location for i in issues}
    assert locations == {"docs/testing.md", "docs/log.md"}
    for i in issues:
        assert i.severity == "WARN"
        assert i.evidence["expected_path"].startswith("docs/")


def test_handles_missing_docs_directory(tmp_path: Path):
    cfg = {"coverage_required": ["dev-setup.md"]}
    issues = run(_ctx(tmp_path), cfg, date(2026, 4, 17))
    assert len(issues) == 1
    assert issues[0].location == "docs/dev-setup.md"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/rules/test_coverage_gap.py -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement rules/coverage_gap.py**

Create `backend/app/integrity/plugins/doc_audit/rules/coverage_gap.py`:

```python
from __future__ import annotations

from datetime import date
from typing import Any

from ....issue import IntegrityIssue
from ....protocol import ScanContext


def run(ctx: ScanContext, cfg: dict[str, Any], today: date) -> list[IntegrityIssue]:
    required: list[str] = list(cfg.get("coverage_required", []))
    issues: list[IntegrityIssue] = []
    for name in required:
        rel = f"docs/{name}"
        if not (ctx.repo_root / rel).is_file():
            issues.append(
                IntegrityIssue(
                    rule="doc.coverage_gap",
                    severity="WARN",
                    node_id=rel,
                    location=rel,
                    message=f"Required doc missing: {rel}",
                    evidence={"expected_path": rel},
                )
            )
    return issues
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/rules/test_coverage_gap.py -v
```

Expected: 3 PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/app/integrity/plugins/doc_audit/rules/coverage_gap.py \
  backend/tests/integrity/plugins/doc_audit/rules/test_coverage_gap.py && \
git commit -m "feat(integrity): doc.coverage_gap rule"
```

---

### Task 10: Rule — unindexed

**Files:**
- Create: `backend/app/integrity/plugins/doc_audit/rules/unindexed.py`
- Test: `backend/tests/integrity/plugins/doc_audit/rules/test_unindexed.py`

- [ ] **Step 1: Write the failing test**

Create `backend/tests/integrity/plugins/doc_audit/rules/test_unindexed.py`:

```python
from datetime import date
from pathlib import Path

from backend.app.integrity.plugins.doc_audit.rules.unindexed import run
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


def _write(repo: Path, rel: str, content: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _ctx(repo: Path) -> ScanContext:
    g = repo / "graphify"
    g.mkdir(parents=True, exist_ok=True)
    (g / "graph.json").write_text('{"nodes":[],"links":[]}', encoding="utf-8")
    return ScanContext(repo_root=repo, graph=GraphSnapshot.load(repo))


def test_orphan_doc_emits_issue(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# index\n\n- [Setup](docs/dev-setup.md)\n")
    _write(tmp_path, "docs/dev-setup.md", "# setup\n")
    _write(tmp_path, "docs/orphan.md", "no inbound links\n")

    cfg = {
        "doc_roots": ["*.md", "docs/**/*.md"],
        "excluded_paths": [],
        "seed_docs": ["CLAUDE.md"],
        "claude_ignore_file": ".claude-ignore",
    }
    issues = run(_ctx(tmp_path), cfg, date(2026, 4, 17))
    assert len(issues) == 1
    issue = issues[0]
    assert issue.rule == "doc.unindexed"
    assert issue.severity == "WARN"
    assert issue.node_id == "docs/orphan.md"
    assert issue.fix_class == "claude_md_link"
    assert "CLAUDE.md" in issue.evidence["seed_docs"]


def test_reachable_doc_not_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "- [Setup](docs/dev-setup.md)\n")
    _write(tmp_path, "docs/dev-setup.md", "- [Test](testing.md)\n")  # transitively reaches testing.md
    _write(tmp_path, "docs/testing.md", "# tests\n")

    cfg = {
        "doc_roots": ["*.md", "docs/**/*.md"],
        "excluded_paths": [],
        "seed_docs": ["CLAUDE.md"],
        "claude_ignore_file": ".claude-ignore",
    }
    issues = run(_ctx(tmp_path), cfg, date(2026, 4, 17))
    assert issues == []


def test_ignored_doc_not_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, ".claude-ignore", "docs/scratch/**\n")
    _write(tmp_path, "docs/scratch/notes.md", "# scratch\n")

    cfg = {
        "doc_roots": ["*.md", "docs/**/*.md"],
        "excluded_paths": [],
        "seed_docs": ["CLAUDE.md"],
        "claude_ignore_file": ".claude-ignore",
    }
    issues = run(_ctx(tmp_path), cfg, date(2026, 4, 17))
    assert all(i.node_id != "docs/scratch/notes.md" for i in issues)


def test_excluded_doc_not_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/health/latest.md", "# generated\n")

    cfg = {
        "doc_roots": ["*.md", "docs/**/*.md"],
        "excluded_paths": ["docs/health/**"],
        "seed_docs": ["CLAUDE.md"],
        "claude_ignore_file": ".claude-ignore",
    }
    issues = run(_ctx(tmp_path), cfg, date(2026, 4, 17))
    assert all(i.node_id != "docs/health/latest.md" for i in issues)


def test_seed_docs_themselves_never_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "README.md", "# x\n")

    cfg = {
        "doc_roots": ["*.md"],
        "excluded_paths": [],
        "seed_docs": ["CLAUDE.md"],
        "claude_ignore_file": ".claude-ignore",
    }
    issues = run(_ctx(tmp_path), cfg, date(2026, 4, 17))
    # CLAUDE.md is a seed; README.md is a top-level doc not reached → flagged
    flagged = {i.node_id for i in issues}
    assert "CLAUDE.md" not in flagged
    assert "README.md" in flagged
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/rules/test_unindexed.py -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement rules/unindexed.py**

Create `backend/app/integrity/plugins/doc_audit/rules/unindexed.py`:

```python
from __future__ import annotations

from collections import deque
from datetime import date
from typing import Any

from ....issue import IntegrityIssue
from ....protocol import ScanContext
from ..index import MarkdownIndex


def run(ctx: ScanContext, cfg: dict[str, Any], today: date) -> list[IntegrityIssue]:
    idx = MarkdownIndex.build(ctx.repo_root, cfg)
    seeds: list[str] = list(cfg.get("seed_docs", ["CLAUDE.md"]))
    visited: set[str] = set()
    queue: deque[str] = deque()
    for seed in seeds:
        if seed in idx.docs:
            visited.add(seed)
            queue.append(seed)

    while queue:
        cur = queue.popleft()
        for nxt in idx.link_graph.get(cur, set()):
            if nxt in visited:
                continue
            if nxt in idx.docs:
                visited.add(nxt)
                queue.append(nxt)

    issues: list[IntegrityIssue] = []
    for rel in sorted(idx.docs):
        if rel in visited:
            continue
        if rel in idx.ignored:
            continue
        if rel in seeds:
            continue
        issues.append(
            IntegrityIssue(
                rule="doc.unindexed",
                severity="WARN",
                node_id=rel,
                location=rel,
                message=f"Not reachable from {seeds}",
                evidence={"seed_docs": seeds},
                fix_class="claude_md_link",
            )
        )
    return issues
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/rules/test_unindexed.py -v
```

Expected: 5 PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/app/integrity/plugins/doc_audit/rules/unindexed.py \
  backend/tests/integrity/plugins/doc_audit/rules/test_unindexed.py && \
git commit -m "feat(integrity): doc.unindexed rule (BFS reachability)"
```

---

### Task 11: Rule — broken_link

**Files:**
- Create: `backend/app/integrity/plugins/doc_audit/rules/broken_link.py`
- Test: `backend/tests/integrity/plugins/doc_audit/rules/test_broken_link.py`

- [ ] **Step 1: Write the failing test**

Create `backend/tests/integrity/plugins/doc_audit/rules/test_broken_link.py`:

```python
from datetime import date
from pathlib import Path
from unittest.mock import patch

from backend.app.integrity.plugins.doc_audit.rules.broken_link import run
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


def _write(repo: Path, rel: str, content: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _ctx(repo: Path) -> ScanContext:
    g = repo / "graphify"
    g.mkdir(parents=True, exist_ok=True)
    (g / "graph.json").write_text('{"nodes":[],"links":[]}', encoding="utf-8")
    return ScanContext(repo_root=repo, graph=GraphSnapshot.load(repo))


_BASE_CFG = {
    "doc_roots": ["*.md", "docs/**/*.md", "knowledge/**/*.md"],
    "excluded_paths": [],
    "seed_docs": ["CLAUDE.md"],
    "claude_ignore_file": ".claude-ignore",
    "rename_lookback": "30.days.ago",
}


def test_broken_file_link_emits_issue(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/broken.md", "See [gone](gone.md) for details.\n")

    with patch(
        "backend.app.integrity.plugins.doc_audit.rules.broken_link.recent_renames",
        return_value={},
    ):
        issues = run(_ctx(tmp_path), _BASE_CFG, date(2026, 4, 17))
    matching = [i for i in issues if i.location.startswith("docs/broken.md")]
    assert len(matching) == 1
    issue = matching[0]
    assert issue.rule == "doc.broken_link"
    assert issue.severity == "WARN"
    assert issue.fix_class is None
    assert issue.evidence["target"] == "docs/gone.md"


def test_broken_anchor_emits_issue(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/target.md", "## Real Section\n")
    _write(tmp_path, "docs/anchor.md", "Link [there](target.md#nonexistent).\n")

    with patch(
        "backend.app.integrity.plugins.doc_audit.rules.broken_link.recent_renames",
        return_value={},
    ):
        issues = run(_ctx(tmp_path), _BASE_CFG, date(2026, 4, 17))
    matching = [i for i in issues if "anchor.md" in i.location]
    assert len(matching) == 1
    assert matching[0].evidence["anchor"] == "nonexistent"


def test_recent_rename_downgrades_to_doc_link_renamed(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/source.md", "See [old](old-name.md).\n")

    with patch(
        "backend.app.integrity.plugins.doc_audit.rules.broken_link.recent_renames",
        return_value={"docs/old-name.md": "docs/new-name.md"},
    ):
        issues = run(_ctx(tmp_path), _BASE_CFG, date(2026, 4, 17))
    matching = [i for i in issues if "source.md" in i.location]
    assert len(matching) == 1
    issue = matching[0]
    assert issue.fix_class == "doc_link_renamed"
    assert issue.evidence["rename_to"] == "docs/new-name.md"


def test_absolute_url_not_checked(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "[ext](https://example.com/whatever).\n")

    with patch(
        "backend.app.integrity.plugins.doc_audit.rules.broken_link.recent_renames",
        return_value={},
    ):
        issues = run(_ctx(tmp_path), _BASE_CFG, date(2026, 4, 17))
    assert issues == []


def test_valid_link_not_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/a.md", "See [b](b.md#sec).\n")
    _write(tmp_path, "docs/b.md", "## Sec\n")

    with patch(
        "backend.app.integrity.plugins.doc_audit.rules.broken_link.recent_renames",
        return_value={},
    ):
        issues = run(_ctx(tmp_path), _BASE_CFG, date(2026, 4, 17))
    assert issues == []


def test_in_page_anchor_validated(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/inpage.md", "## Top\n\nGo [here](#nope) and [there](#top).\n")

    with patch(
        "backend.app.integrity.plugins.doc_audit.rules.broken_link.recent_renames",
        return_value={},
    ):
        issues = run(_ctx(tmp_path), _BASE_CFG, date(2026, 4, 17))
    matching = [i for i in issues if "inpage.md" in i.location]
    assert len(matching) == 1
    assert matching[0].evidence["anchor"] == "nope"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/rules/test_broken_link.py -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement rules/broken_link.py**

Create `backend/app/integrity/plugins/doc_audit/rules/broken_link.py`:

```python
from __future__ import annotations

from datetime import date
from pathlib import PurePosixPath
from typing import Any

from ....issue import IntegrityIssue
from ....protocol import ScanContext
from ...graph_lint.git_renames import recent_renames
from ..index import MarkdownIndex


_ABSOLUTE_PREFIXES = ("http://", "https://", "mailto:", "ftp://", "tel:")


def _resolve_target(base_dir: PurePosixPath, target: str) -> str | None:
    parts: list[str] = []
    for part in (base_dir / target).parts:
        if part == "..":
            if parts:
                parts.pop()
            else:
                return None
        elif part == ".":
            continue
        else:
            parts.append(part)
    return PurePosixPath(*parts).as_posix() if parts else None


def run(ctx: ScanContext, cfg: dict[str, Any], today: date) -> list[IntegrityIssue]:
    idx = MarkdownIndex.build(ctx.repo_root, cfg)
    rename_lookback = cfg.get("rename_lookback", "30.days.ago")
    renames = recent_renames(ctx.repo_root, since=rename_lookback)

    issues: list[IntegrityIssue] = []
    for rel in sorted(idx.docs):
        parsed = idx.docs[rel]
        base_dir = PurePosixPath(rel).parent
        for link in parsed.links:
            target_lower = (link.target or "").lower()
            if target_lower.startswith(_ABSOLUTE_PREFIXES):
                continue

            # In-page anchor: target empty, anchor present → validate against this doc's anchors
            if not link.target and link.anchor:
                if link.anchor not in idx.anchors_by_path.get(rel, set()):
                    issues.append(
                        IntegrityIssue(
                            rule="doc.broken_link",
                            severity="WARN",
                            node_id=f"{rel}#{link.anchor}",
                            location=f"{rel}:{link.line}",
                            message=f"Anchor #{link.anchor} not found in {rel}",
                            evidence={
                                "target": rel,
                                "anchor": link.anchor,
                                "in_page": True,
                            },
                            fix_class=None,
                        )
                    )
                continue

            if not link.target:
                continue
            # Skip non-markdown intra-repo links (images, code files, etc.) — out of scope
            if not link.target.endswith(".md"):
                continue

            resolved = _resolve_target(base_dir, link.target)
            if resolved is None:
                continue

            target_path = ctx.repo_root / resolved
            if not target_path.is_file():
                fix_class = None
                evidence: dict[str, Any] = {"target": resolved}
                if resolved in renames:
                    fix_class = "doc_link_renamed"
                    evidence["rename_to"] = renames[resolved]
                issues.append(
                    IntegrityIssue(
                        rule="doc.broken_link",
                        severity="WARN",
                        node_id=f"{rel}->{resolved}",
                        location=f"{rel}:{link.line}",
                        message=f"Broken link: {resolved}",
                        evidence=evidence,
                        fix_class=fix_class,
                    )
                )
                continue

            if link.anchor:
                if link.anchor not in idx.anchors_by_path.get(resolved, set()):
                    issues.append(
                        IntegrityIssue(
                            rule="doc.broken_link",
                            severity="WARN",
                            node_id=f"{rel}->{resolved}#{link.anchor}",
                            location=f"{rel}:{link.line}",
                            message=f"Anchor #{link.anchor} not found in {resolved}",
                            evidence={
                                "target": resolved,
                                "anchor": link.anchor,
                            },
                            fix_class=None,
                        )
                    )
    return issues
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/rules/test_broken_link.py -v
```

Expected: 6 PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/app/integrity/plugins/doc_audit/rules/broken_link.py \
  backend/tests/integrity/plugins/doc_audit/rules/test_broken_link.py && \
git commit -m "feat(integrity): doc.broken_link rule with git-rename downgrade"
```

---

### Task 12: Rule — dead_code_ref

**Files:**
- Create: `backend/app/integrity/plugins/doc_audit/rules/dead_code_ref.py`
- Test: `backend/tests/integrity/plugins/doc_audit/rules/test_dead_code_ref.py`

- [ ] **Step 1: Write the failing test**

Create `backend/tests/integrity/plugins/doc_audit/rules/test_dead_code_ref.py`:

```python
import json
from datetime import date
from pathlib import Path

from backend.app.integrity.plugins.doc_audit.rules.dead_code_ref import run
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


def _write(repo: Path, rel: str, content: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _ctx_with_graph(repo: Path, nodes: list[dict]) -> ScanContext:
    g = repo / "graphify"
    g.mkdir(parents=True, exist_ok=True)
    (g / "graph.json").write_text(json.dumps({"nodes": nodes, "links": []}), encoding="utf-8")
    return ScanContext(repo_root=repo, graph=GraphSnapshot.load(repo))


_CFG = {
    "doc_roots": ["*.md", "docs/**/*.md", "knowledge/**/*.md"],
    "excluded_paths": [],
    "seed_docs": ["CLAUDE.md"],
    "claude_ignore_file": ".claude-ignore",
}


def test_missing_path_ref_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/dead.md", "See `backend/app/missing.py:42` for details.\n")
    nodes = [{"id": "foo.do_thing", "label": "do_thing", "source_file": "backend/app/foo.py"}]
    issues = run(_ctx_with_graph(tmp_path, nodes), _CFG, date(2026, 4, 17))
    matching = [i for i in issues if "dead.md" in i.location]
    assert len(matching) >= 1
    assert any(i.evidence["code_ref"].startswith("`backend/app/missing.py:42`") for i in matching)


def test_missing_qualified_symbol_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/sym.md", "Calls `Module.gone_func` somewhere.\n")
    nodes = [{"id": "module.live_func", "label": "live_func", "source_file": "backend/app/module.py"}]
    issues = run(_ctx_with_graph(tmp_path, nodes), _CFG, date(2026, 4, 17))
    matching = [i for i in issues if "sym.md" in i.location]
    assert len(matching) == 1
    assert "Module.gone_func" in matching[0].evidence["code_ref"]


def test_live_path_ref_not_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/live.md", "See `backend/app/foo.py:42`.\n")
    _write(tmp_path, "backend/app/foo.py", "# real file\n")
    nodes = [{"id": "foo.do_thing", "label": "do_thing", "source_file": "backend/app/foo.py"}]
    issues = run(_ctx_with_graph(tmp_path, nodes), _CFG, date(2026, 4, 17))
    matching = [i for i in issues if "live.md" in i.location]
    assert matching == []


def test_unqualified_symbol_not_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/prose.md", "The variable `config` is widely used.\n")
    issues = run(_ctx_with_graph(tmp_path, []), _CFG, date(2026, 4, 17))
    matching = [i for i in issues if "prose.md" in i.location]
    assert matching == []


def test_adr_paths_excluded_from_dead_code_ref(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "knowledge/adr/001-foo.md", "References `backend/app/missing.py`.\n")
    issues = run(_ctx_with_graph(tmp_path, []), _CFG, date(2026, 4, 17))
    assert all("knowledge/adr/" not in i.location for i in issues)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/rules/test_dead_code_ref.py -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement rules/dead_code_ref.py**

Create `backend/app/integrity/plugins/doc_audit/rules/dead_code_ref.py`:

```python
from __future__ import annotations

from datetime import date
from typing import Any

from ....issue import IntegrityIssue
from ....protocol import ScanContext
from ..index import MarkdownIndex
from ..parser.code_refs import extract_code_refs


def _graph_indices(ctx: ScanContext) -> tuple[set[str], set[str]]:
    paths: set[str] = set()
    symbols: set[str] = set()
    for node in ctx.graph.nodes:
        sf = node.get("source_file")
        if isinstance(sf, str) and sf:
            paths.add(sf)
        nid = node.get("id")
        if isinstance(nid, str):
            symbols.add(nid.lower())
        label = node.get("label")
        if isinstance(label, str):
            symbols.add(label.lower())
    return paths, symbols


def _is_adr(rel: str) -> bool:
    return rel.startswith("knowledge/adr/")


def run(ctx: ScanContext, cfg: dict[str, Any], today: date) -> list[IntegrityIssue]:
    idx = MarkdownIndex.build(ctx.repo_root, cfg)
    graph_paths, graph_symbols = _graph_indices(ctx)
    issues: list[IntegrityIssue] = []
    for rel in sorted(idx.docs):
        if _is_adr(rel):
            continue  # handled by adr_status_drift
        parsed = idx.docs[rel]
        refs = extract_code_refs(parsed.raw_text)
        for ref in refs:
            if ref.kind in ("path", "path_line"):
                target = ref.path or ""
                if not target:
                    continue
                if target in graph_paths:
                    continue
                if (ctx.repo_root / target).exists():
                    continue
                issues.append(
                    IntegrityIssue(
                        rule="doc.dead_code_ref",
                        severity="WARN",
                        node_id=f"{rel}->{target}",
                        location=f"{rel}:{ref.source_line}",
                        message=f"Dead code reference: {target}",
                        evidence={
                            "code_ref": ref.text,
                            "kind": ref.kind,
                            "source_line": ref.source_line,
                        },
                    )
                )
            elif ref.kind == "symbol":
                if not ref.symbol or "." not in ref.symbol:
                    continue
                if ref.symbol.lower() in graph_symbols:
                    continue
                issues.append(
                    IntegrityIssue(
                        rule="doc.dead_code_ref",
                        severity="WARN",
                        node_id=f"{rel}->{ref.symbol}",
                        location=f"{rel}:{ref.source_line}",
                        message=f"Dead symbol reference: {ref.symbol}",
                        evidence={
                            "code_ref": ref.text,
                            "kind": ref.kind,
                            "source_line": ref.source_line,
                        },
                    )
                )
    return issues
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/rules/test_dead_code_ref.py -v
```

Expected: 5 PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/app/integrity/plugins/doc_audit/rules/dead_code_ref.py \
  backend/tests/integrity/plugins/doc_audit/rules/test_dead_code_ref.py && \
git commit -m "feat(integrity): doc.dead_code_ref rule"
```

---

### Task 13: Rule — stale_candidate

**Files:**
- Create: `backend/app/integrity/plugins/doc_audit/rules/stale_candidate.py`
- Test: `backend/tests/integrity/plugins/doc_audit/rules/test_stale_candidate.py`

- [ ] **Step 1: Write the failing test**

Create `backend/tests/integrity/plugins/doc_audit/rules/test_stale_candidate.py`:

```python
from datetime import date
from pathlib import Path
from unittest.mock import patch

from backend.app.integrity.plugins.doc_audit.rules.stale_candidate import run
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


def _write(repo: Path, rel: str, content: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _ctx(repo: Path) -> ScanContext:
    g = repo / "graphify"
    g.mkdir(parents=True, exist_ok=True)
    (g / "graph.json").write_text('{"nodes":[],"links":[]}', encoding="utf-8")
    return ScanContext(repo_root=repo, graph=GraphSnapshot.load(repo))


_CFG = {
    "doc_roots": ["*.md", "docs/**/*.md"],
    "excluded_paths": [],
    "seed_docs": ["CLAUDE.md"],
    "claude_ignore_file": ".claude-ignore",
    "thresholds": {"stale_days": 90},
}


def _patched_git_log(*, doc_iso: str | None, src_iso: str | None):
    """Return a context manager that patches GitLog.last_commit_iso."""
    def fake_last_commit_iso(self, rel_path: str) -> str | None:
        if rel_path.endswith(".md"):
            return doc_iso
        return src_iso

    return patch(
        "backend.app.integrity.plugins.doc_audit.rules.stale_candidate.GitLog.last_commit_iso",
        fake_last_commit_iso,
    )


def test_stale_doc_with_changed_ref_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/old.md", "See `backend/app/foo.py`.\n")
    _write(tmp_path, "backend/app/foo.py", "# changed\n")

    with _patched_git_log(doc_iso="2025-01-01T00:00:00+00:00", src_iso="2026-04-17T00:00:00+00:00"):
        issues = run(_ctx(tmp_path), _CFG, date(2026, 4, 17))

    matching = [i for i in issues if "old.md" in i.location]
    assert len(matching) == 1
    issue = matching[0]
    assert issue.rule == "doc.stale_candidate"
    assert issue.severity == "INFO"
    assert "backend/app/foo.py" in issue.evidence["changed_refs"]


def test_recent_doc_not_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/fresh.md", "See `backend/app/foo.py`.\n")
    _write(tmp_path, "backend/app/foo.py", "# changed\n")

    with _patched_git_log(doc_iso="2026-04-15T00:00:00+00:00", src_iso="2026-04-17T00:00:00+00:00"):
        issues = run(_ctx(tmp_path), _CFG, date(2026, 4, 17))

    assert all("fresh.md" not in i.location for i in issues)


def test_old_doc_with_no_changed_ref_not_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/old-stable.md", "See `backend/app/foo.py`.\n")
    _write(tmp_path, "backend/app/foo.py", "# unchanged\n")

    # src_iso older than doc_iso → ref didn't change after doc
    with _patched_git_log(doc_iso="2025-12-01T00:00:00+00:00", src_iso="2025-01-01T00:00:00+00:00"):
        issues = run(_ctx(tmp_path), _CFG, date(2026, 4, 17))

    assert all("old-stable.md" not in i.location for i in issues)


def test_uncommitted_doc_skipped(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(tmp_path, "docs/new.md", "See `backend/app/foo.py`.\n")
    _write(tmp_path, "backend/app/foo.py", "# anything\n")

    with _patched_git_log(doc_iso=None, src_iso="2026-04-17T00:00:00+00:00"):
        issues = run(_ctx(tmp_path), _CFG, date(2026, 4, 17))

    assert all("new.md" not in i.location for i in issues)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/rules/test_stale_candidate.py -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement rules/stale_candidate.py**

Create `backend/app/integrity/plugins/doc_audit/rules/stale_candidate.py`:

```python
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any

from ....issue import IntegrityIssue
from ....protocol import ScanContext
from ..index import MarkdownIndex
from ..parser.code_refs import extract_code_refs
from ..parser.git_log import GitLog


def _parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def run(ctx: ScanContext, cfg: dict[str, Any], today: date) -> list[IntegrityIssue]:
    idx = MarkdownIndex.build(ctx.repo_root, cfg)
    stale_days = int(cfg.get("thresholds", {}).get("stale_days", 90))
    threshold = datetime.combine(today, datetime.min.time(), tzinfo=timezone.utc) - timedelta(
        days=stale_days
    )
    gl = GitLog(ctx.repo_root)

    issues: list[IntegrityIssue] = []
    for rel in sorted(idx.docs):
        doc_iso = gl.last_commit_iso(rel)
        doc_dt = _parse_iso(doc_iso)
        if doc_dt is None:
            continue
        if doc_dt > threshold:
            continue

        parsed = idx.docs[rel]
        changed_refs: list[str] = []
        for ref in extract_code_refs(parsed.raw_text):
            if ref.kind not in ("path", "path_line") or not ref.path:
                continue
            src_iso = gl.last_commit_iso(ref.path)
            src_dt = _parse_iso(src_iso)
            if src_dt is None:
                continue
            if src_dt > doc_dt:
                changed_refs.append(ref.path)

        if not changed_refs:
            continue

        issues.append(
            IntegrityIssue(
                rule="doc.stale_candidate",
                severity="INFO",
                node_id=rel,
                location=rel,
                message=f"Doc {rel} unchanged >{stale_days}d while {len(changed_refs)} ref(s) moved",
                evidence={
                    "doc_last_commit": doc_iso,
                    "stale_days": stale_days,
                    "changed_refs": changed_refs,
                },
            )
        )
    return issues
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/rules/test_stale_candidate.py -v
```

Expected: 4 PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/app/integrity/plugins/doc_audit/rules/stale_candidate.py \
  backend/tests/integrity/plugins/doc_audit/rules/test_stale_candidate.py && \
git commit -m "feat(integrity): doc.stale_candidate rule (INFO)"
```

---

### Task 14: Rule — adr_status_drift

**Files:**
- Create: `backend/app/integrity/plugins/doc_audit/rules/adr_status_drift.py`
- Test: `backend/tests/integrity/plugins/doc_audit/rules/test_adr_status_drift.py`

- [ ] **Step 1: Write the failing test**

Create `backend/tests/integrity/plugins/doc_audit/rules/test_adr_status_drift.py`:

```python
import json
from datetime import date
from pathlib import Path

from backend.app.integrity.plugins.doc_audit.rules.adr_status_drift import (
    is_accepted,
    run,
)
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


def _write(repo: Path, rel: str, content: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def _ctx(repo: Path, nodes: list[dict] | None = None) -> ScanContext:
    g = repo / "graphify"
    g.mkdir(parents=True, exist_ok=True)
    (g / "graph.json").write_text(
        json.dumps({"nodes": nodes or [], "links": []}), encoding="utf-8"
    )
    return ScanContext(repo_root=repo, graph=GraphSnapshot.load(repo))


_CFG = {
    "doc_roots": ["*.md", "knowledge/**/*.md"],
    "excluded_paths": [],
    "seed_docs": ["CLAUDE.md"],
    "claude_ignore_file": ".claude-ignore",
}


def test_is_accepted_recognizes_bold_line():
    text = "# ADR\n\n**Status:** Accepted\n\nBody.\n"
    assert is_accepted({}, text) is True


def test_is_accepted_recognizes_yaml_frontmatter():
    text = "Body.\n"
    assert is_accepted({"status": "accepted"}, text) is True
    assert is_accepted({"status": "Accepted"}, text) is True


def test_is_accepted_rejects_other_statuses():
    text = "**Status:** Proposed\n"
    assert is_accepted({}, text) is False
    assert is_accepted({"status": "deprecated"}, text) is False


def test_accepted_adr_with_dead_ref_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(
        tmp_path,
        "knowledge/adr/002-drift.md",
        "# ADR 002\n\n**Status:** Accepted\n\nReferences `backend/app/gone.py:10`.\n",
    )
    issues = run(_ctx(tmp_path), _CFG, date(2026, 4, 17))
    matching = [i for i in issues if "002-drift.md" in i.location]
    assert len(matching) == 1
    assert matching[0].rule == "doc.adr_status_drift"
    assert matching[0].severity == "WARN"


def test_accepted_adr_with_live_ref_not_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(
        tmp_path,
        "knowledge/adr/001-real.md",
        "# ADR 001\n\n**Status:** Accepted\n\nUses `backend/app/foo.py`.\n",
    )
    _write(tmp_path, "backend/app/foo.py", "# real\n")
    issues = run(
        _ctx(tmp_path, [{"id": "x", "label": "x", "source_file": "backend/app/foo.py"}]),
        _CFG,
        date(2026, 4, 17),
    )
    assert all("001-real.md" not in i.location for i in issues)


def test_proposed_adr_skipped(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(
        tmp_path,
        "knowledge/adr/003-prop.md",
        "# ADR 003\n\n**Status:** Proposed\n\nReferences `backend/app/gone.py`.\n",
    )
    issues = run(_ctx(tmp_path), _CFG, date(2026, 4, 17))
    assert all("003-prop.md" not in i.location for i in issues)


def test_template_excluded(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(
        tmp_path,
        "knowledge/adr/template.md",
        "# Template\n\n**Status:** Accepted\n\n`backend/app/missing.py`\n",
    )
    issues = run(_ctx(tmp_path), _CFG, date(2026, 4, 17))
    assert all("template.md" not in i.location for i in issues)


def test_yaml_frontmatter_accepted_flagged(tmp_path: Path):
    _write(tmp_path, "CLAUDE.md", "# x\n")
    _write(
        tmp_path,
        "knowledge/adr/004-yaml.md",
        "---\nstatus: accepted\n---\n\n# ADR 004\n\nUses `backend/app/gone.py`.\n",
    )
    issues = run(_ctx(tmp_path), _CFG, date(2026, 4, 17))
    matching = [i for i in issues if "004-yaml.md" in i.location]
    assert len(matching) == 1
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/rules/test_adr_status_drift.py -v
```

Expected: FAIL with `ModuleNotFoundError`.

- [ ] **Step 3: Implement rules/adr_status_drift.py**

Create `backend/app/integrity/plugins/doc_audit/rules/adr_status_drift.py`:

```python
from __future__ import annotations

import re
from datetime import date
from typing import Any

from ....issue import IntegrityIssue
from ....protocol import ScanContext
from ..index import MarkdownIndex
from ..parser.code_refs import extract_code_refs


_BOLD_STATUS_RE = re.compile(
    r"^\s*\*\*Status:\*\*\s*Accepted\b", re.IGNORECASE | re.MULTILINE
)


def is_accepted(front_matter: dict[str, Any], raw_text: str) -> bool:
    fm_status = front_matter.get("status")
    if isinstance(fm_status, str) and fm_status.strip().lower() == "accepted":
        return True
    return bool(_BOLD_STATUS_RE.search(raw_text))


def _is_adr_doc(rel: str) -> bool:
    return rel.startswith("knowledge/adr/") and not rel.endswith("/template.md")


def _graph_indices(ctx: ScanContext) -> tuple[set[str], set[str]]:
    paths: set[str] = set()
    symbols: set[str] = set()
    for node in ctx.graph.nodes:
        sf = node.get("source_file")
        if isinstance(sf, str) and sf:
            paths.add(sf)
        nid = node.get("id")
        if isinstance(nid, str):
            symbols.add(nid.lower())
        label = node.get("label")
        if isinstance(label, str):
            symbols.add(label.lower())
    return paths, symbols


def run(ctx: ScanContext, cfg: dict[str, Any], today: date) -> list[IntegrityIssue]:
    idx = MarkdownIndex.build(ctx.repo_root, cfg)
    graph_paths, graph_symbols = _graph_indices(ctx)
    issues: list[IntegrityIssue] = []
    for rel in sorted(idx.docs):
        if not _is_adr_doc(rel):
            continue
        parsed = idx.docs[rel]
        if not is_accepted(parsed.front_matter, parsed.raw_text):
            continue
        for ref in extract_code_refs(parsed.raw_text):
            if ref.kind in ("path", "path_line") and ref.path:
                if ref.path in graph_paths:
                    continue
                if (ctx.repo_root / ref.path).exists():
                    continue
                issues.append(
                    IntegrityIssue(
                        rule="doc.adr_status_drift",
                        severity="WARN",
                        node_id=f"{rel}->{ref.path}",
                        location=f"{rel}:{ref.source_line}",
                        message=f"Accepted ADR references missing path: {ref.path}",
                        evidence={
                            "code_ref": ref.text,
                            "kind": ref.kind,
                            "source_line": ref.source_line,
                        },
                    )
                )
            elif ref.kind == "symbol" and ref.symbol and "." in ref.symbol:
                if ref.symbol.lower() in graph_symbols:
                    continue
                issues.append(
                    IntegrityIssue(
                        rule="doc.adr_status_drift",
                        severity="WARN",
                        node_id=f"{rel}->{ref.symbol}",
                        location=f"{rel}:{ref.source_line}",
                        message=f"Accepted ADR references missing symbol: {ref.symbol}",
                        evidence={
                            "code_ref": ref.text,
                            "kind": ref.kind,
                            "source_line": ref.source_line,
                        },
                    )
                )
    return issues
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/rules/test_adr_status_drift.py -v
```

Expected: 7 PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/app/integrity/plugins/doc_audit/rules/adr_status_drift.py \
  backend/tests/integrity/plugins/doc_audit/rules/test_adr_status_drift.py && \
git commit -m "feat(integrity): doc.adr_status_drift rule"
```

---

### Task 15: Engine wiring — register DocAuditPlugin in CLI

**Files:**
- Modify: `backend/app/integrity/__main__.py`
- Test: `backend/tests/integrity/test_main_cli.py` (existing — add a doc_audit-specific test)

- [ ] **Step 1: Write the failing test**

Append to `backend/tests/integrity/test_main_cli.py`:

```python
def test_main_runs_only_doc_audit(tmp_path, monkeypatch):
    # Arrange: empty repo with just a CLAUDE.md and graphify stub
    (tmp_path / "CLAUDE.md").write_text("# x\n", encoding="utf-8")
    g = tmp_path / "graphify"
    g.mkdir()
    (g / "graph.json").write_text('{"nodes":[],"links":[]}', encoding="utf-8")

    from backend.app.integrity.__main__ import main

    rc = main(["--plugin", "doc_audit", "--repo-root", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / "integrity-out" / __import__("datetime").date.today().isoformat() / "doc_audit.json").exists()


def test_main_rejects_unknown_plugin(tmp_path):
    g = tmp_path / "graphify"
    g.mkdir()
    (g / "graph.json").write_text('{"nodes":[],"links":[]}', encoding="utf-8")

    from backend.app.integrity.__main__ import main

    import pytest

    with pytest.raises(SystemExit):
        main(["--plugin", "nonexistent", "--repo-root", str(tmp_path)])
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/test_main_cli.py::test_main_runs_only_doc_audit -v
```

Expected: FAIL with `unknown plugin: 'doc_audit'` (the existing CLI rejects unknown plugin names).

- [ ] **Step 3: Wire DocAuditPlugin into __main__.py**

Edit `backend/app/integrity/__main__.py`:

1. Update the `KNOWN_PLUGINS` constant near the top:

```python
KNOWN_PLUGINS = ("graph_extension", "graph_lint", "doc_audit")
```

2. Inside `_build_engine`, after the `want_lint` block, add:

```python
    audit_cfg_enabled = enabled.get("doc_audit", {}).get("enabled", True)
    want_audit = (only is None or only == "doc_audit") and audit_cfg_enabled
    if want_audit:
        from .plugins.doc_audit.plugin import DocAuditPlugin

        audit_plugin = DocAuditPlugin(config=enabled.get("doc_audit", {}))
        # Drop depends_on when graph_extension isn't registered so the
        # engine topo-sort doesn't require an unloaded plugin.
        if not want_extension:
            from dataclasses import replace

            audit_plugin = replace(audit_plugin, depends_on=())
        engine.register(audit_plugin)
```

- [ ] **Step 4: Run test to verify it passes**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/test_main_cli.py -v
```

Expected: existing tests + 2 new tests all PASS.

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/app/integrity/__main__.py backend/tests/integrity/test_main_cli.py && \
git commit -m "feat(integrity): register doc_audit plugin in CLI"
```

---

### Task 16: Plugin integration test (tiny_repo fixture)

**Files:**
- Create: `backend/tests/integrity/plugins/doc_audit/conftest.py`
- Modify: `backend/tests/integrity/plugins/doc_audit/test_plugin.py` — add integration test

This task validates all rules wired together against a single synthetic repo.

- [ ] **Step 1: Build the tiny_repo fixture**

Create `backend/tests/integrity/plugins/doc_audit/conftest.py`:

```python
from __future__ import annotations

import json
import subprocess
from datetime import date
from pathlib import Path

import pytest


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=str(cwd), check=True, capture_output=True)


@pytest.fixture
def tiny_repo(tmp_path: Path) -> Path:
    """Synthetic mini-repo exercising every doc_audit rule.

    Layout (relative to returned path):
      CLAUDE.md                # links to all "good" docs
      docs/dev-setup.md        # required (coverage)
      docs/testing.md          # required
      docs/gotchas.md          # required
      docs/skill-creation.md   # required
      docs/log.md              # required
      docs/orphan.md           # NOT linked → unindexed
      docs/broken.md           # links to gone.md → broken_link
      docs/anchor-broken.md    # links to dev-setup.md#nope → broken_link (anchor)
      docs/dead-ref.md         # `backend/app/missing.py` + `Module.gone` → dead_code_ref
      knowledge/adr/001-real.md    # Accepted, refs live foo.py → no issue
      knowledge/adr/002-drift.md   # Accepted, refs missing.py → adr_status_drift
      knowledge/adr/template.md    # Accepted but excluded
      backend/app/foo.py
      graphify/graph.json
    """
    repo = tmp_path / "tiny"
    repo.mkdir()

    (repo / "CLAUDE.md").write_text(
        "# Index\n\n"
        "- [Dev setup](docs/dev-setup.md)\n"
        "- [Testing](docs/testing.md)\n"
        "- [Gotchas](docs/gotchas.md)\n"
        "- [Skill creation](docs/skill-creation.md)\n"
        "- [Changelog](docs/log.md)\n"
        "- [Broken](docs/broken.md)\n"
        "- [Anchor broken](docs/anchor-broken.md)\n"
        "- [Dead ref](docs/dead-ref.md)\n",
        encoding="utf-8",
    )
    docs = repo / "docs"
    docs.mkdir()
    for name in ("dev-setup.md", "testing.md", "gotchas.md", "skill-creation.md", "log.md"):
        (docs / name).write_text(f"# {name}\n", encoding="utf-8")
    (docs / "orphan.md").write_text("# Not linked from index\n", encoding="utf-8")
    (docs / "broken.md").write_text("See [gone](gone.md).\n", encoding="utf-8")
    (docs / "anchor-broken.md").write_text(
        "See [setup](dev-setup.md#nope).\n", encoding="utf-8"
    )
    (docs / "dead-ref.md").write_text(
        "Refs `backend/app/missing.py:7` and `Module.gone_func`.\n",
        encoding="utf-8",
    )

    adr = repo / "knowledge" / "adr"
    adr.mkdir(parents=True)
    (adr / "001-real.md").write_text(
        "# ADR 001\n\n**Status:** Accepted\n\nUses `backend/app/foo.py`.\n",
        encoding="utf-8",
    )
    (adr / "002-drift.md").write_text(
        "# ADR 002\n\n**Status:** Accepted\n\nReferences `backend/app/missing.py:1`.\n",
        encoding="utf-8",
    )
    (adr / "template.md").write_text(
        "# Template\n\n**Status:** Accepted\n\nReferences `backend/app/missing.py`.\n",
        encoding="utf-8",
    )

    (repo / "backend" / "app").mkdir(parents=True)
    (repo / "backend" / "app" / "foo.py").write_text("# real file\n", encoding="utf-8")

    g = repo / "graphify"
    g.mkdir()
    (g / "graph.json").write_text(
        json.dumps(
            {
                "nodes": [
                    {
                        "id": "foo.do_thing",
                        "label": "do_thing",
                        "source_file": "backend/app/foo.py",
                    }
                ],
                "links": [],
            }
        ),
        encoding="utf-8",
    )

    # Initialize git so stale_candidate has commit timestamps to read
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "test")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "initial")

    return repo


@pytest.fixture
def today_fixed() -> date:
    return date(2026, 4, 17)
```

- [ ] **Step 2: Write the integration test**

Append to `backend/tests/integrity/plugins/doc_audit/test_plugin.py`:

```python
from collections import Counter

from backend.app.integrity.plugins.doc_audit.plugin import DocAuditPlugin
from backend.app.integrity.protocol import ScanContext
from backend.app.integrity.schema import GraphSnapshot


def test_full_plugin_against_tiny_repo(tiny_repo, today_fixed):
    cfg = {
        "doc_roots": ["*.md", "docs/**/*.md", "knowledge/**/*.md"],
        "excluded_paths": [],
        "claude_ignore_file": ".claude-ignore",
        "seed_docs": ["CLAUDE.md"],
        "thresholds": {"stale_days": 90},
        "coverage_required": [
            "dev-setup.md",
            "testing.md",
            "gotchas.md",
            "skill-creation.md",
            "log.md",
        ],
        "rename_lookback": "30.days.ago",
        "disabled_rules": [],
    }
    plugin = DocAuditPlugin(config=cfg, today=today_fixed)
    ctx = ScanContext(repo_root=tiny_repo, graph=GraphSnapshot.load(tiny_repo))
    result = plugin.scan(ctx)

    counts = Counter(i.rule for i in result.issues)
    # coverage_gap: all 5 required files present → 0
    assert counts["doc.coverage_gap"] == 0
    # unindexed: docs/orphan.md not linked from CLAUDE.md → 1
    assert counts["doc.unindexed"] == 1
    # broken_link: docs/broken.md → docs/gone.md (1) + anchor-broken → 1 = 2
    assert counts["doc.broken_link"] == 2
    # dead_code_ref: dead-ref.md has 2 refs (path + symbol)
    assert counts["doc.dead_code_ref"] == 2
    # adr_status_drift: 002-drift.md (1 path ref); 001-real and template excluded
    assert counts["doc.adr_status_drift"] == 1
    # stale_candidate: tiny_repo just got committed → no docs older than 90d
    assert counts["doc.stale_candidate"] == 0

    assert result.failures == []
    artifact = tiny_repo / "integrity-out" / today_fixed.isoformat() / "doc_audit.json"
    assert artifact.exists()
    payload = __import__("json").loads(artifact.read_text())
    assert set(payload["rules_run"]) == {
        "doc.coverage_gap",
        "doc.unindexed",
        "doc.broken_link",
        "doc.dead_code_ref",
        "doc.stale_candidate",
        "doc.adr_status_drift",
    }
```

- [ ] **Step 3: Run integration test**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/test_plugin.py::test_full_plugin_against_tiny_repo -v
```

Expected: PASS.

- [ ] **Step 4: Run the full doc_audit test suite to confirm nothing regressed**

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/ -v
```

Expected: all PASS (≈ 35-40 tests across rules + parser + plugin + index).

- [ ] **Step 5: Commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add backend/tests/integrity/plugins/doc_audit/conftest.py \
  backend/tests/integrity/plugins/doc_audit/test_plugin.py && \
git commit -m "test(integrity): doc_audit plugin integration test against tiny_repo fixture"
```

---

### Task 17: Make target + acceptance gate verification

**Files:**
- Modify: `Makefile`
- Possibly modify: `CLAUDE.md` (add links to clear `doc.unindexed` on the real repo)
- Possibly create: `.claude-ignore` (opt-out for unreachable-by-design docs)

- [ ] **Step 1: Add make target**

Edit `Makefile`. Find the `.PHONY: integrity integrity-lint integrity-snapshot-prune` block and:

1. Update help text on existing `integrity` line from `(A→B)` to `(A→B→C)`:

```make
integrity: ## Run the full integrity pipeline (A→B→C); writes integrity-out/ + docs/health/
	uv run python -m backend.app.integrity
```

2. Append to the `.PHONY` declaration: ` integrity-doc`. The full block becomes:

```make
.PHONY: integrity integrity-lint integrity-doc integrity-snapshot-prune
```

3. Add a new target after `integrity-lint`:

```make
integrity-doc: ## Run only Plugin C (doc_audit) — assumes A has run
	uv run python -m backend.app.integrity --plugin doc_audit --no-augment
```

- [ ] **Step 2: Verify make target invokes correctly (dry run)**

```bash
cd /Users/jay/Developer/claude-code-agent && make -n integrity-doc
```

Expected: prints `uv run python -m backend.app.integrity --plugin doc_audit --no-augment`.

- [ ] **Step 3: Run plugin against real repo (first observation)**

```bash
cd /Users/jay/Developer/claude-code-agent && make integrity-doc
```

Expected: exit 0. Inspect output:

```bash
cd /Users/jay/Developer/claude-code-agent && \
DATE=$(date +%F) && \
jq '.rules_run, (.issues | group_by(.rule) | map({rule: .[0].rule, count: length}))' \
  integrity-out/$DATE/doc_audit.json
```

Expected: `rules_run` lists all 6 rules; counts will reveal real-repo state.

- [ ] **Step 4: Drive `doc.unindexed` and `doc.broken_link` to 0 (acceptance gate)**

Inspect issues:

```bash
cd /Users/jay/Developer/claude-code-agent && \
DATE=$(date +%F) && \
jq '.issues[] | select(.rule == "doc.unindexed") | .location' \
  integrity-out/$DATE/doc_audit.json && \
jq '.issues[] | select(.rule == "doc.broken_link") | {loc: .location, msg: .message}' \
  integrity-out/$DATE/doc_audit.json
```

For each `doc.unindexed`:
- If the doc should be reachable: add a link to it from `CLAUDE.md` (preferred) or from a doc already reachable from CLAUDE.md.
- If the doc is intentionally unreachable: create/update `.claude-ignore` (one path-glob per line) to opt out.

For each `doc.broken_link`: fix the link target in the source markdown file.

Re-run after each batch of edits:

```bash
cd /Users/jay/Developer/claude-code-agent && make integrity-doc
```

Repeat until both rule counts are 0.

- [ ] **Step 5: Verify acceptance gate**

```bash
cd /Users/jay/Developer/claude-code-agent && \
DATE=$(date +%F) && \
echo "rules_run:" && \
jq -r '.rules_run | join(", ")' integrity-out/$DATE/doc_audit.json && \
echo "" && \
echo "issue counts by rule:" && \
jq -r '.issues | group_by(.rule) | map("\(.[0].rule): \(length)") | join("\n")' \
  integrity-out/$DATE/doc_audit.json && \
echo "" && \
echo "WARN/ERROR count (gate-blocking):" && \
jq -r '[.issues[] | select(.severity == "WARN" or .severity == "ERROR")] | length' \
  integrity-out/$DATE/doc_audit.json
```

Acceptance gate γ requires:
1. ✅ `make integrity-doc` exit 0 — confirmed by Step 3.
2. ✅ `doc.unindexed` count == 0 — confirmed by Step 4.
3. ✅ `doc.broken_link` count == 0 — confirmed by Step 4.
4. ✅ `doc.adr_status_drift` listed in `rules_run` — confirmed by `rules_run` above.
5. ✅ All doc_audit unit + integration tests pass — re-confirm:

```bash
cd /Users/jay/Developer/claude-code-agent/backend && \
uv run pytest tests/integrity/plugins/doc_audit/ -v
```

Expected: all PASS.

6. ✅ Plugin C results visible in `docs/health/latest.md` — verify by running full pipeline:

```bash
cd /Users/jay/Developer/claude-code-agent && make integrity && \
grep -E "^## doc_audit" docs/health/latest.md
```

Expected: `## doc_audit (v1.0.0)` heading present in the markdown.

INFO-severity (`doc.stale_candidate`) does NOT block the gate.

- [ ] **Step 6: Verify nothing else regressed**

```bash
cd /Users/jay/Developer/claude-code-agent && make lint && make typecheck && make test-backend
```

Expected: all green.

- [ ] **Step 7: Update changelog**

Append an entry to `docs/log.md` under `[Unreleased]`:

```markdown
- **integrity**: Plugin C (`doc_audit`) ships gate γ — six markdown-drift rules
  (`doc.unindexed`, `doc.broken_link`, `doc.dead_code_ref`, `doc.stale_candidate`,
  `doc.adr_status_drift`, `doc.coverage_gap`). New `make integrity-doc` target.
  Adds `markdown-it-py` runtime dep. `.claude-ignore` opt-out supported.
  Spec: `docs/superpowers/specs/2026-04-17-integrity-plugin-c-design.md`.
```

- [ ] **Step 8: Final commit**

```bash
cd /Users/jay/Developer/claude-code-agent && \
git add Makefile docs/log.md && \
git diff --cached --name-only | grep -v '^Makefile$\|^docs/log.md$' >/dev/null 2>&1 && \
  git add CLAUDE.md .claude-ignore 2>/dev/null || true && \
git commit -m "feat(integrity): wire Plugin C (doc_audit) into Make + close gate γ"
```

If `CLAUDE.md` and/or `.claude-ignore` were also modified to clear `doc.unindexed`, include them in the commit. Otherwise this commit only touches `Makefile` and `docs/log.md`.

---

## Self-Review Notes

**Spec coverage** (each spec section → task that implements it):
- §3 decisions (markdown-it-py, configurable seed_docs/coverage list, both ADR status formats, GitHub slug, conservative regex, 30-day rename lookback, doc_audit.json artifact, .claude-ignore) → Tasks 1–4, 6, 7, 8, 11, 12, 14
- §4.1 file layout → Task 1 (skeleton), Tasks 3–14 (content)
- §4.2 plugin shape → Task 8
- §4.3 rule signature → Task 8 (Rule type alias)
- §4.4 parser layer (ParsedDoc, MarkdownIndex, code_refs, git_log, ignore) → Tasks 3–7
- §4.5 each rule in detail → Tasks 9–14
- §4.6 reuse from existing engine (no copies) → Verified in Tasks 11 (recent_renames import), 12+14 (graph indices), 9 (no copies)
- §5 config additions → Task 2
- §6 data flow → handled by aggregator (already shipped at gate β); Task 17 verifies via `make integrity`
- §7 CLI / Make targets → Tasks 15 + 17
- §8 error handling (per-rule try/except, plugin-wide failure caught by engine, missing graph degrades gracefully, missing git degrades gracefully) → Task 8 (per-rule try/except), Tasks 5/13 (None on missing git), Tasks 12/14 (empty graph indices)
- §9 testing (≥1 positive + 1 negative per rule, parser tests, integration test, smoke against real repo) → Tasks 3–7 (parser tests), Tasks 9–14 (per-rule), Task 16 (integration), Task 17 (smoke)
- §10 acceptance gate γ → Task 17 explicitly walks through all six gate criteria
- §13 dependencies (markdown-it-py >=3.0) → Task 1
- §14 rollout (configure, observe, fix CLAUDE.md / .claude-ignore, achieve 0 unindexed + 0 broken) → Task 17 Step 4

**Placeholder scan**: No "TBD", "implement later", or vague-handler steps. Every step has either an exact code block or an exact command.

**Type consistency**:
- `Rule = Callable[[ScanContext, dict[str, Any], date], list[IntegrityIssue]]` defined in Task 8, used by all rules in Tasks 9–14.
- `ParsedDoc.raw_text` (Task 3) consumed by Tasks 12, 13, 14 (`raw_text` field present).
- `CodeRef.kind` literal `"path" | "path_line" | "symbol"` (Task 4) matched in Tasks 12, 13, 14.
- `IgnoreMatcher.matches(rel)` returns `bool` (Task 6); `MarkdownIndex.build` consumes `claude_ignore_file` (Task 7); rules consume `idx.ignored` (Tasks 10).
- `GitLog.last_commit_iso(rel_path)` returns `str | None` (Task 5); `stale_candidate` (Task 13) handles `None` correctly.
- `MarkdownIndex.docs[rel]` (Task 7) accessed in Tasks 10, 11, 12, 13, 14.
- `is_accepted(front_matter, raw_text)` (Task 14) uses `dict[str, Any]` matching `ParsedDoc.front_matter` shape.
- `recent_renames` import path (`...graph_lint.git_renames`) verified against existing module (Task 11).
- `KNOWN_PLUGINS` extension (Task 15) matches existing tuple shape.

All cross-task names match. Plan is internally consistent.

---

## Execution

Plan complete and saved to `docs/superpowers/plans/2026-04-17-integrity-plugin-c.md`. User pre-approved subagent-driven execution with comprehensive choices — proceeding via `superpowers:subagent-driven-development` starting at Task 1.
