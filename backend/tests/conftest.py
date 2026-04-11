import pytest


@pytest.fixture(autouse=True)
def _test_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set minimal env vars for all tests."""
    monkeypatch.setenv("ENVIRONMENT", "test")


@pytest.fixture(autouse=True)
def _clear_config_cache() -> None:
    from app.config import get_config

    get_config.cache_clear()
