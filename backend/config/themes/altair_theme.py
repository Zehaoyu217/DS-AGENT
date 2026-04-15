"""Minimal stub for Altair theme registration.

The full theme implementation is not required — this stub allows
skill imports to resolve without error.  Charts render using the
default Altair theme.
"""
from __future__ import annotations


def register_all() -> None:  # noqa: D401
    """No-op: theme registration not configured."""


def use_variant(name: str) -> None:  # noqa: D401
    """No-op: theme variants not configured."""


def active_tokens() -> dict:
    return {}
