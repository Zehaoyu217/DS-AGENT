"""Minimal stub for table CSS theme."""
from __future__ import annotations


def render_table_css(variant: str = "default") -> str:  # noqa: D401
    """Return basic table CSS."""
    return (
        "table { border-collapse: collapse; font-family: monospace; font-size: 13px; }"
        " th, td { border: 1px solid #444; padding: 4px 8px; text-align: left; }"
        " th { background: #222; color: #ccc; }"
        " tr:nth-child(even) { background: #111; }"
    )
