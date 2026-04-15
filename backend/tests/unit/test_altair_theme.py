"""Altair theme stub contract tests.

The full variant-aware Altair theme (gir_light / gir_editorial / ...) was
never implemented. The module exports no-op ``register_all`` / ``use_variant``
and an ``active_tokens`` that returns an empty dict. These tests pin the
stub contract so skill imports keep working even when Altair is not
configured; replace them once a real theme ships.
"""
from __future__ import annotations

from config.themes.altair_theme import active_tokens, register_all, use_variant


def test_register_all_is_callable_and_returns_none() -> None:
    assert register_all() is None


def test_use_variant_accepts_any_name() -> None:
    # No variants are registered — the stub must not raise for any input.
    assert use_variant("light") is None
    assert use_variant("editorial") is None
    assert use_variant("nonexistent") is None


def test_active_tokens_returns_empty_dict_when_unconfigured() -> None:
    tokens = active_tokens()
    assert tokens == {}
