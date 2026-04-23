from __future__ import annotations

from app.api import models_api


def test_models_api_includes_mlx_group(monkeypatch) -> None:
    monkeypatch.setattr(models_api, "_mlx_runtime_available", lambda: True)
    monkeypatch.setattr(
        models_api,
        "_fetch_mlx_models",
        lambda: [
            models_api.ModelEntry(
                id="mlx/mlx-community/gemma-4-e2b-it-OptiQ-4bit",
                label="Gemma 4 E2B",
                description="MLX local · cached",
            )
        ],
    )

    response = models_api.list_models()
    groups = {group.provider: group for group in response.groups}

    assert groups["mlx"].available is True
    assert groups["mlx"].models[0].id == "mlx/mlx-community/gemma-4-e2b-it-OptiQ-4bit"


def test_models_api_marks_mlx_unavailable_when_runtime_missing(monkeypatch) -> None:
    monkeypatch.setattr(models_api, "_mlx_runtime_available", lambda: False)

    response = models_api.list_models()
    groups = {group.provider: group for group in response.groups}

    assert groups["mlx"].available is False
    assert groups["mlx"].models == []
    assert "backend[mlx]" in groups["mlx"].note


def test_models_api_has_no_ollama_group() -> None:
    """Ollama was removed — the response must not advertise it."""
    response = models_api.list_models()
    providers = {group.provider for group in response.groups}
    assert "ollama" not in providers
    assert "anthropic" not in providers
