"""Tests for the sb_digest pre-turn hook."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from app import config as app_config


@pytest.fixture
def hook_env(tmp_path, monkeypatch):
    home = tmp_path / "sb"
    (home / "digests").mkdir(parents=True)
    (home / "claims").mkdir()
    (home / "sources").mkdir()
    (home / ".sb").mkdir()
    monkeypatch.setenv("SECOND_BRAIN_HOME", str(home))
    monkeypatch.setattr(app_config, "SECOND_BRAIN_ENABLED", True, raising=False)
    monkeypatch.delenv("SB_DIGEST_HOOK_ENABLED", raising=False)
    return home


def _write(home: Path, today: date, entries: list[dict]) -> None:
    dig = home / "digests"
    (dig / f"{today.isoformat()}.md").write_text("# Digest")
    with (dig / f"{today.isoformat()}.actions.jsonl").open("w") as f:
        for e in entries:
            f.write(json.dumps(e) + "\n")


def test_hook_disabled_flag(monkeypatch):
    monkeypatch.setattr(app_config, "SECOND_BRAIN_ENABLED", False, raising=False)
    from app.hooks.sb_digest_hook import build_digest_summary

    assert build_digest_summary() is None


def test_hook_explicit_env_disable(hook_env, monkeypatch):
    monkeypatch.setenv("SB_DIGEST_HOOK_ENABLED", "false")
    from app.hooks.sb_digest_hook import build_digest_summary

    assert build_digest_summary() is None


def test_hook_missing_digest(hook_env):
    from app.hooks.sb_digest_hook import build_digest_summary

    assert build_digest_summary() is None


def test_hook_all_applied_returns_none(hook_env):
    today = date.today()
    _write(
        hook_env,
        today,
        [{"id": "r01", "section": "Reconciliation", "action": {"action": "keep"}}],
    )
    (hook_env / "digests" / f"{today.isoformat()}.applied.jsonl").write_text(
        json.dumps({"id": "r01", "action": {}}) + "\n"
    )
    from app.hooks.sb_digest_hook import build_digest_summary

    assert build_digest_summary() is None


def test_hook_returns_summary_with_unread(hook_env):
    today = date.today()
    _write(
        hook_env,
        today,
        [
            {"id": "r01", "section": "Reconciliation", "action": {"action": "keep"}},
            {"id": "r02", "section": "Reconciliation", "action": {"action": "keep"}},
            {"id": "t01", "section": "Taxonomy", "action": {"action": "keep"}},
        ],
    )
    from app.hooks.sb_digest_hook import build_digest_summary

    s = build_digest_summary()
    assert s is not None
    assert "2 pending KB decisions" not in s  # 3 unread, not 2
    assert "3 pending KB decisions" in s
    assert today.isoformat() in s


def test_hook_never_raises(hook_env, monkeypatch):
    from app.hooks import sb_digest_hook

    def boom():
        raise RuntimeError("x")

    monkeypatch.setattr(sb_digest_hook, "_load_config", boom)
    assert sb_digest_hook.build_digest_summary() is None
