from functools import lru_cache

from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    """Application configuration loaded from environment variables.

    Runtime data paths are controlled by ``CCAGENT_HOME`` (default ``~/.ccagent``).
    See ``app.core.home`` for the full path-helper API. The fields below that
    reference paths (sandbox_state_root, duckdb_path, wiki_root) are convenience
    overrides; in production prefer setting ``CCAGENT_HOME`` and relying on the
    derived defaults in ``wiring.py``.
    """

    environment: str = "development"
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = False

    # Model
    default_model: str = "qwen3.5:9b"
    ollama_base_url: str = "http://localhost:11434"
    litellm_base_url: str = "http://localhost:4000"
    openrouter_api_key: str = ""

    # Sandbox
    sandbox_timeout_seconds: int = 30
    sandbox_max_memory_mb: int = 2048
    sandbox_state_root: str = "./data/sandbox_sessions"

    # DuckDB
    duckdb_path: str = "./data/duckdb/eval.db"

    # Wiki
    wiki_root: str = "../knowledge/wiki"
    wiki_auto_write: bool = True

    # Context window
    context_max_tokens: int = 32768
    context_compaction_threshold: float = 0.80

    model_config = {"env_prefix": "", "env_file": "../.env", "extra": "ignore"}


@lru_cache
def get_config() -> AppConfig:
    return AppConfig()
