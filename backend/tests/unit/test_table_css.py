"""Table CSS stub contract tests.

The full theme system (tokens.yaml / ThemeTokens / variant-aware CSS) was
never implemented. ``render_table_css`` is a deliberate stub that returns
a single monospace, dark, border-collapsed table style for every variant.
These tests pin the stub contract so we notice if the stub drifts or the
full theme system is wired in (at which point these tests should be
replaced with variant-aware assertions).
"""
from __future__ import annotations

from config.themes.table_css import render_table_css


def test_returns_nonempty_css() -> None:
    css = render_table_css()
    assert css
    assert "border-collapse: collapse" in css


def test_contains_table_and_cell_selectors() -> None:
    css = render_table_css()
    assert "table {" in css
    assert "th, td {" in css


def test_variant_arg_accepted_but_ignored() -> None:
    """Stub accepts any variant name without raising; output is identical."""
    default = render_table_css()
    editorial = render_table_css(variant="editorial")
    print_variant = render_table_css(variant="print")
    assert default == editorial == print_variant


def test_uses_monospace_family_for_data_density() -> None:
    """Swiss/terminal aesthetic — monospace is non-negotiable for tables."""
    assert "monospace" in render_table_css()
