from __future__ import annotations

import pytest

from app.harness.config import HarnessConfig, ModelProfile, load_config


def test_load_config_parses_models_yaml(tmp_path) -> None:
    config_path = tmp_path / "models.yaml"
    config_path.write_text(
        """
mode: config
models:
  gpt_oss_120b:
    provider: openrouter
    model_id: openai/gpt-oss-120b:free
    tier: observatory
  gemma_mlx:
    provider: mlx
    model_id: mlx/mlx-community/gemma-4-e4b-it-OptiQ-4bit
    tier: strict
roles:
  think: gpt_oss_120b
  evaluate: gemma_mlx
warmup: [gemma_mlx]
guardrails:
  mode: per_tier
  retry_on_gate_block: null
""",
        encoding="utf-8",
    )
    cfg = load_config(config_path)
    assert isinstance(cfg, HarnessConfig)
    assert cfg.mode == "config"
    assert cfg.roles["think"] == "gpt_oss_120b"
    profile = cfg.models["gemma_mlx"]
    assert isinstance(profile, ModelProfile)
    assert profile.provider == "mlx"
    assert profile.tier == "strict"
    assert "gemma_mlx" in cfg.warmup


def test_load_config_rejects_unknown_role_target(tmp_path) -> None:
    config_path = tmp_path / "bad.yaml"
    config_path.write_text(
        """
mode: config
models: {}
roles: {think: doesnt_exist}
warmup: []
guardrails: {mode: per_tier, retry_on_gate_block: null}
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="role 'think'"):
        load_config(config_path)


def test_load_config_rejects_unknown_tier(tmp_path) -> None:
    path = tmp_path / "bad.yaml"
    path.write_text(
        """
mode: config
models:
  x: {provider: openrouter, model_id: x, tier: mystery}
roles: {think: x}
warmup: []
guardrails: {mode: per_tier, retry_on_gate_block: null}
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="tier"):
        load_config(path)


def test_load_config_rejects_removed_providers(tmp_path) -> None:
    """anthropic and ollama are no longer valid providers."""
    for bad_provider in ("anthropic", "ollama"):
        path = tmp_path / f"{bad_provider}.yaml"
        path.write_text(
            f"""
mode: config
models:
  x: {{provider: {bad_provider}, model_id: x, tier: advisory}}
roles: {{think: x}}
warmup: []
guardrails: {{mode: per_tier, retry_on_gate_block: null}}
""",
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="provider"):
            load_config(path)


def test_load_config_accepts_mlx_provider(tmp_path) -> None:
    path = tmp_path / "mlx.yaml"
    path.write_text(
        """
mode: config
models:
  local_mlx:
    provider: mlx
    model_id: mlx/mlx-community/gemma-4-e2b-it-OptiQ-4bit
    tier: strict
roles: {think: local_mlx}
warmup: [local_mlx]
guardrails: {mode: per_tier, retry_on_gate_block: null}
""",
        encoding="utf-8",
    )

    cfg = load_config(path)
    assert cfg.models["local_mlx"].provider == "mlx"
    assert cfg.warmup == ("local_mlx",)
