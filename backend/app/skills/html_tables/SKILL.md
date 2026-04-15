---
name: html_tables
description: Render a DataFrame as themed HTML with numeric right-align, semantic cell classes, and caption.
level: 1
version: '0.1'
---
# html_tables

Renders a DataFrame into HTML, pulling CSS from the active theme (cell-positive, cell-negative, cell-muted). Headers come from DataFrame columns; numeric columns automatically get `cell-num` for right-align.

## When to use

When an analytical result is best shown as a table, not a chart (e.g. exact per-row counts, categorical comparisons, ≤20 rows).

## Contract

- `render(df, title=None, caption=None, variant="light", max_rows=200, cell_classes=None) -> str`
- Returns a string containing `<style>` + `<table class="ga-table">`.
- `cell_classes` maps `(row_index, column_name) -> list[str]`; lets callers mark positive/negative cells.

## Rules

- No color hex hardcoded in renderer — comes from the active variant.
- Rows beyond `max_rows` are truncated with a visible marker row.
- Numeric columns right-aligned via the `cell-num` class.
