---
name: report_builder
description: Composes research_memo (default), analysis_brief, or full_report from promoted findings. Renders Markdown + HTML (editorial theme) + PDF. Blocks on stat_validate FAIL.
version: 0.1.0
---

# report_builder

Turn promoted findings into a publishable report.

## Templates

| Template | Use | Length |
|---|---|---|
| `research_memo` | GIR-style default. 3 key points + one section per finding + methodology + caveats | ~3-5 pages |
| `analysis_brief` | One-pager. One chart, three bullets. | 1 page |
| `full_report` | TOC + intro + themed finding groups + discussion + extended appendix | 10+ pages |

## Entry point

```python
build(spec: ReportSpec, template: Literal["research_memo","analysis_brief","full_report"] = "research_memo",
      formats: tuple[str, ...] = ("md", "html")) -> ReportResult
```

`ReportSpec` is defined in `pkg/build.py`. All findings must have passed `stat_validate` with PASS or WARN; FAIL blocks the build.

## Rules (enforced)

- **Key Points = exactly 3** (not 5, not 7).
- Every claim cites an artifact ID.
- Methodology section is required.
- Caveats are first-class; no empty caveat sections.
- Default theme: editorial.
- PDF via weasyprint; requires system libcairo + pango.
