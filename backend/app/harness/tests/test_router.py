from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from app.harness.config import GuardrailConfig, HarnessConfig, ModelProfile
from app.harness.router import ModelRouter


def _cfg() -> HarnessConfig:
    return HarnessConfig(
        mode="config",
        models={
            "claude": ModelProfile(name="claude", provider="anthropic",
                                   model_id="claude-sonnet-4-6", tier="observatory"),
            "gemma": ModelProfile(name="gemma", provider="ollama",
                                  model_id="gemma4:26b", tier="strict",
                                  host="http://localhost:11434"),
        },
        roles={"think": "gemma", "evaluate": "claude"},
        warmup=("gemma",),
        guardrails=GuardrailConfig(mode="per_tier", retry_on_gate_block=None),
    )


def test_router_resolves_role_to_client() -> None:
    client_factory = MagicMock()
    fake_client = MagicMock()
    client_factory.side_effect = lambda profile: fake_client
    router = ModelRouter(config=_cfg(), client_factory=client_factory)
    client = router.for_role("think")
    assert client is fake_client


def test_router_unknown_role_raises() -> None:
    router = ModelRouter(config=_cfg(), client_factory=lambda p: MagicMock())
    with pytest.raises(KeyError, match="role"):
        router.for_role("nope")


def test_router_caches_clients_per_model() -> None:
    factory_calls: list[str] = []

    def factory(profile):
        factory_calls.append(profile.name)
        return MagicMock()

    router = ModelRouter(config=_cfg(), client_factory=factory)
    c1 = router.for_role("think")
    c2 = router.for_role("think")
    assert c1 is c2
    assert factory_calls == ["gemma"]


def test_router_warms_up_configured_models() -> None:
    client = MagicMock()
    router = ModelRouter(config=_cfg(), client_factory=lambda p: client)
    router.warm_up()
    client.warmup.assert_called_once()


def test_router_escalate_on_gate_block_swaps_to_configured_model() -> None:
    cfg = _cfg()
    cfg = HarnessConfig(
        mode=cfg.mode, models=cfg.models, roles=cfg.roles, warmup=cfg.warmup,
        guardrails=GuardrailConfig(mode="per_tier", retry_on_gate_block="claude"),
    )

    def _factory(profile: ModelProfile) -> MagicMock:
        m = MagicMock()
        m.name = profile.name
        return m

    router = ModelRouter(config=cfg, client_factory=_factory)
    retry = router.retry_client()
    assert retry is not None
    assert retry.name == "claude"
