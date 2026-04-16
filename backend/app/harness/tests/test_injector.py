from __future__ import annotations

from unittest.mock import MagicMock

from app.harness.injector import InjectorInputs, PreTurnInjector, _has_content_beyond_headers
from app.skills.base import SkillMetadata, SkillNode


def _make_node(name: str, desc: str, children: list[SkillNode] | None = None) -> SkillNode:
    meta = SkillMetadata(name=name, version="1.0", description=desc)
    node = SkillNode(metadata=meta, instructions="", package_path=None, depth=1, parent=None)
    if children:
        node.children.extend(children)
    return node


def _skill_registry_stub():
    class _Stub:
        def list_top_level(self) -> list[SkillNode]:
            return [
                _make_node("correlation", "Multi-method corr with CI."),
                _make_node("group_compare", "Effect-size-first comparison."),
            ]
    return _Stub()


def _make_injector(tmp_path, working: str = "WORKING DIGEST", index: str = "INDEX DIGEST"):
    prompt_path = tmp_path / "data_scientist.md"
    prompt_path.write_text("STATIC PROMPT BODY", encoding="utf-8")
    wiki = MagicMock()
    wiki.working_digest.return_value = working
    wiki.index_digest.return_value = index
    wiki.latest_session_notes.return_value = ""
    return PreTurnInjector(
        prompt_path=prompt_path,
        wiki=wiki,
        skill_registry=_skill_registry_stub(),
    )


# ── Content-beyond-headers helper ────────────────────────────────────────────


def test_has_content_beyond_headers_true_for_real_content() -> None:
    assert _has_content_beyond_headers("# Heading\n\nSome actual content here.") is True


def test_has_content_beyond_headers_false_for_header_only() -> None:
    assert _has_content_beyond_headers("# Working\n\n") is False


def test_has_content_beyond_headers_false_for_index_placeholders() -> None:
    index_only = (
        "# Wiki Index\n\n"
        "## Findings\n\n_(no pages yet)_\n\n"
        "## Entities\n\n_(no pages yet)_\n\n"
    )
    assert _has_content_beyond_headers(index_only) is False


def test_has_content_beyond_headers_true_when_index_has_entries() -> None:
    index_with_entry = (
        "# Wiki Index\n\n"
        "## Findings\n\n"
        "- [F-001](F-001.md) — Revenue grew 12%\n\n"
        "## Entities\n\n_(no pages yet)_\n\n"
    )
    assert _has_content_beyond_headers(index_with_entry) is True


# ── Injector assembly ─────────────────────────────────────────────────────────


def test_injector_assembles_all_sections(tmp_path) -> None:
    injector = _make_injector(tmp_path)
    inputs = InjectorInputs(active_profile_summary="PROFILE SUMMARY")
    system = injector.build(inputs)

    assert "STATIC PROMPT BODY" in system
    assert "WORKING DIGEST" in system
    assert "INDEX DIGEST" in system
    assert "correlation" in system
    assert "Multi-method corr with CI." in system
    assert "PROFILE SUMMARY" in system


def test_injector_omits_profile_when_absent(tmp_path) -> None:
    injector = _make_injector(tmp_path, working="", index="")
    system = injector.build(InjectorInputs())
    assert "## Active Dataset Profile" not in system


def test_injector_omits_operational_state_when_only_headers(tmp_path) -> None:
    """Empty header-skeleton wiki files must not produce an Operational State section."""
    injector = _make_injector(tmp_path, working="# Working\n\n", index="# Index\n\n")
    system = injector.build(InjectorInputs())
    assert "## Operational State" not in system


def test_injector_omits_operational_state_when_index_all_placeholders(tmp_path) -> None:
    placeholder_index = (
        "# Wiki Index\n\n"
        "## Findings\n\n_(no pages yet)_\n\n"
        "## Hypotheses\n\n_(no pages yet)_\n\n"
    )
    injector = _make_injector(tmp_path, working="# Working\n\n", index=placeholder_index)
    system = injector.build(InjectorInputs())
    assert "## Operational State" not in system


def test_injector_includes_operational_state_with_real_content(tmp_path) -> None:
    injector = _make_injector(
        tmp_path,
        working="## TODO\n\n- profile loans table\n",
        index="# Wiki Index\n\n## Findings\n\n- [F-001](F-001.md) — Revenue up\n\n",
    )
    system = injector.build(InjectorInputs())
    assert "## Operational State" in system


def test_injector_enforces_section_order(tmp_path) -> None:
    injector = _make_injector(tmp_path)
    out = injector.build(InjectorInputs(active_profile_summary="PROF"))
    positions = {
        "STATIC": out.index("STATIC"),
        "## Operational State": out.index("## Operational State"),
        "## Skills": out.index("## Skills"),
        "## Active Dataset Profile": out.index("## Active Dataset Profile"),
    }
    assert (
        positions["STATIC"]
        < positions["## Operational State"]
        < positions["## Skills"]
        < positions["## Active Dataset Profile"]
    )


def test_injector_gotchas_no_longer_in_system_prompt(tmp_path) -> None:
    """Statistical Gotchas moved to a skill — must NOT appear in the base system prompt."""
    injector = _make_injector(tmp_path)
    system = injector.build(InjectorInputs())
    assert "## Statistical Gotchas" not in system
    assert "simpsons_paradox" not in system


def test_injector_static_is_cached(tmp_path) -> None:
    """_static() should read the file only once, not on every build() call."""
    injector = _make_injector(tmp_path)
    # Prime the cache.
    injector.build(InjectorInputs())
    cache_after_first = injector._static_cache
    assert cache_after_first is not None
    # Mutate the underlying file — the cached value must not change.
    (tmp_path / "data_scientist.md").write_text("CHANGED", encoding="utf-8")
    injector.build(InjectorInputs())
    assert injector._static_cache == cache_after_first
    assert "CHANGED" not in injector._static_cache


def test_skill_menu_is_cached_after_first_build(tmp_path) -> None:
    """_skill_menu() must call list_top_level() only once across multiple build() calls."""
    call_count = 0
    original_nodes = [
        _make_node("correlation", "Multi-method corr."),
    ]

    class _CountingStub:
        def list_top_level(self) -> list[SkillNode]:
            nonlocal call_count
            call_count += 1
            return original_nodes

    prompt_path = tmp_path / "prompt.md"
    prompt_path.write_text("BASE", encoding="utf-8")
    wiki = MagicMock()
    wiki.working_digest.return_value = ""
    wiki.index_digest.return_value = ""
    wiki.latest_session_notes.return_value = ""
    injector = PreTurnInjector(
        prompt_path=prompt_path,
        wiki=wiki,
        skill_registry=_CountingStub(),
    )

    injector.build(InjectorInputs())
    injector.build(InjectorInputs())
    injector.build(InjectorInputs())

    assert call_count == 1, (
        f"list_top_level() called {call_count} times — expected 1 (cache miss only on first call)"
    )


def test_skill_menu_cache_contains_correct_content(tmp_path) -> None:
    """Cached skill menu must render the same content as a freshly built one."""
    injector = _make_injector(tmp_path)
    first = injector.build(InjectorInputs())
    # Cache is now warm — second call must return identical output.
    second = injector.build(InjectorInputs())
    assert first == second
