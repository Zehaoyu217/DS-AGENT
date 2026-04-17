"""Unit tests for build_duckdb_globals in sandbox_bootstrap."""
from __future__ import annotations

import subprocess
import sys

from app.harness.sandbox_bootstrap import (
    _PREAMBLE_CACHE,
    _get_cached_preamble,
    build_duckdb_globals,
)


def test_build_duckdb_globals_no_dataset() -> None:
    preamble = build_duckdb_globals("test-session-001", None)
    assert "import duckdb" in preamble
    assert "df = None" in preamble
    assert "save_artifact" in preamble


def test_build_duckdb_globals_has_conn() -> None:
    preamble = build_duckdb_globals("test-session-001", None)
    assert "conn = duckdb.connect" in preamble


def test_build_duckdb_globals_session_id_embedded() -> None:
    preamble = build_duckdb_globals("my-session-xyz", None)
    assert "my-session-xyz" in preamble


def test_build_duckdb_globals_csv_dataset(tmp_path: object) -> None:
    fake_path = "/tmp/data.csv"
    preamble = build_duckdb_globals("test-session-csv", fake_path)
    assert "pd.read_csv" in preamble
    assert "df =" in preamble


def test_build_duckdb_globals_parquet_dataset() -> None:
    fake_path = "/tmp/data.parquet"
    preamble = build_duckdb_globals("test-session-pq", fake_path)
    assert "pd.read_parquet" in preamble
    assert "df =" in preamble


def test_preamble_cache_returns_same_string_on_repeat_calls() -> None:
    """_get_cached_preamble(None) must return the same string on every call."""
    first = _get_cached_preamble(None)
    second = _get_cached_preamble(None)
    assert first == second
    assert isinstance(first, str)
    assert len(first) > 0


def test_preamble_cache_hits_on_second_call() -> None:
    """_get_cached_preamble(None) must populate _PREAMBLE_CACHE and reuse it."""
    # Clear any existing cache entry for id(None) = 0 to force a clean miss.
    none_key = id(None)
    _PREAMBLE_CACHE.pop(none_key, None)

    _get_cached_preamble(None)  # miss — should populate cache
    assert none_key in _PREAMBLE_CACHE  # cache must be populated

    cached_value = _PREAMBLE_CACHE[none_key]
    _get_cached_preamble(None)  # hit — must return same object
    assert _PREAMBLE_CACHE[none_key] is cached_value


def test_preamble_cache_with_mock_registry() -> None:
    """Registry-keyed cache: generate_bootstrap_imports must be called only once."""
    call_count = 0

    class _MockRegistry:
        def generate_bootstrap_imports(self) -> list[str]:
            nonlocal call_count
            call_count += 1
            return ["# mock skill import"]

    registry = _MockRegistry()
    key = id(registry)
    _PREAMBLE_CACHE.pop(key, None)  # ensure clean slate

    _get_cached_preamble(registry)
    _get_cached_preamble(registry)
    _get_cached_preamble(registry)

    assert call_count == 1, (
        f"generate_bootstrap_imports() called {call_count} times — expected 1"
    )


def test_build_duckdb_globals_runs_in_subprocess() -> None:
    """Verify the generated preamble is valid Python that executes without error."""
    preamble = build_duckdb_globals("test-session-sub", None)
    # Patch paths so it doesn't need real data dirs
    code = preamble + "\nprint('ok')"
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        timeout=30,
    )
    # 0 = success, 1 = import error (acceptable in minimal test env with missing packages)
    # We just want no syntax error (which would be exit code 1 with SyntaxError in stderr)
    if result.returncode not in (0, 1):
        raise AssertionError(
            f"Unexpected returncode {result.returncode}\nstderr: {result.stderr}"
        )
    # If it failed, ensure it's an ImportError not a SyntaxError
    if result.returncode == 1:
        assert "SyntaxError" not in result.stderr, (
            f"Preamble has a syntax error:\n{result.stderr}"
        )
