from pathlib import Path

from backend.app.integrity.config import load_config


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def test_load_returns_defaults_when_no_file(tmp_path: Path):
    cfg = load_config(tmp_path)
    assert cfg.plugins["graph_extension"]["enabled"] is True
    assert cfg.plugins["graph_lint"]["thresholds"]["vulture_min_confidence"] == 80


def test_load_merges_user_overrides(tmp_path: Path):
    write(
        tmp_path / "config" / "integrity.yaml",
        """
plugins:
  graph_lint:
    thresholds:
      vulture_min_confidence: 60
""",
    )
    cfg = load_config(tmp_path)
    assert cfg.plugins["graph_lint"]["thresholds"]["vulture_min_confidence"] == 60
    assert cfg.plugins["graph_lint"]["thresholds"]["density_drop_pct"] == 25  # default kept


def test_env_override_int_threshold(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("INTEGRITY_VULTURE_MIN_CONFIDENCE", "70")
    cfg = load_config(tmp_path)
    assert cfg.plugins["graph_lint"]["thresholds"]["vulture_min_confidence"] == 70


def test_env_override_float_threshold(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("INTEGRITY_DENSITY_DROP_PCT", "33.5")
    cfg = load_config(tmp_path)
    assert cfg.plugins["graph_lint"]["thresholds"]["density_drop_pct"] == 33.5


def test_excluded_paths_default(tmp_path: Path):
    cfg = load_config(tmp_path)
    paths = cfg.plugins["graph_lint"]["excluded_paths"]
    assert "tests/**" in paths
