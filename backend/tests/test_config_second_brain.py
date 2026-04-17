"""Tests for Second Brain integration configuration flags."""
from __future__ import annotations

import importlib


def test_second_brain_disabled_when_home_missing(monkeypatch, tmp_path):
    monkeypatch.setenv("SECOND_BRAIN_HOME", str(tmp_path / "nonexistent"))
    from app import config
    importlib.reload(config)
    assert config.SECOND_BRAIN_ENABLED is False


def test_second_brain_enabled_when_sb_dir_present(monkeypatch, tmp_path):
    home = tmp_path / "sb"
    (home / ".sb").mkdir(parents=True)
    monkeypatch.setenv("SECOND_BRAIN_HOME", str(home))
    from app import config
    importlib.reload(config)
    assert home == config.SECOND_BRAIN_HOME
    assert config.SECOND_BRAIN_ENABLED is True
