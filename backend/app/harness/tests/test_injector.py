from __future__ import annotations

from unittest.mock import MagicMock

from app.harness.injector import InjectorInputs, PreTurnInjector


def _skill_registry_stub() -> MagicMock:
    reg = MagicMock()
    reg.list_skills.return_value = [
        {"name": "correlation", "description": "Multi-method corr with CI."},
        {"name": "group_compare", "description": "Effect-size-first comparison."},
    ]
    return reg


def _gotcha_index_stub(text: str = "- **simpsons_paradox** — pooled vs stratified") -> MagicMock:
    idx = MagicMock()
    idx.as_injection.return_value = text
    return idx


def test_injector_assembles_all_sections(tmp_path) -> None:
    prompt_path = tmp_path / "data_scientist.md"
    prompt_path.write_text("STATIC PROMPT BODY", encoding="utf-8")

    wiki = MagicMock()
    wiki.working_digest.return_value = "WORKING DIGEST"
    wiki.index_digest.return_value = "INDEX DIGEST"

    injector = PreTurnInjector(
        prompt_path=prompt_path,
        wiki=wiki,
        skill_registry=_skill_registry_stub(),
        gotcha_index=_gotcha_index_stub(),
    )
    inputs = InjectorInputs(active_profile_summary="PROFILE SUMMARY")
    system = injector.build(inputs)

    assert "STATIC PROMPT BODY" in system
    assert "WORKING DIGEST" in system
    assert "INDEX DIGEST" in system
    assert "correlation" in system
    assert "Multi-method corr with CI." in system
    assert "simpsons_paradox" in system
    assert "PROFILE SUMMARY" in system


def test_injector_omits_profile_when_absent(tmp_path) -> None:
    prompt_path = tmp_path / "p.md"
    prompt_path.write_text("BODY", encoding="utf-8")
    wiki = MagicMock()
    wiki.working_digest.return_value = ""
    wiki.index_digest.return_value = ""
    injector = PreTurnInjector(
        prompt_path=prompt_path,
        wiki=wiki,
        skill_registry=_skill_registry_stub(),
        gotcha_index=_gotcha_index_stub(""),
    )
    system = injector.build(InjectorInputs())
    assert "## Active Dataset Profile" not in system


def test_injector_enforces_section_order(tmp_path) -> None:
    prompt_path = tmp_path / "p.md"
    prompt_path.write_text("STATIC", encoding="utf-8")
    wiki = MagicMock()
    wiki.working_digest.return_value = "WORK"
    wiki.index_digest.return_value = "IDX"
    injector = PreTurnInjector(
        prompt_path=prompt_path,
        wiki=wiki,
        skill_registry=_skill_registry_stub(),
        gotcha_index=_gotcha_index_stub("GOTCHA"),
    )
    out = injector.build(InjectorInputs(active_profile_summary="PROF"))
    positions = {
        "STATIC": out.index("STATIC"),
        "## Operational State": out.index("## Operational State"),
        "## Skill Menu": out.index("## Skill Menu"),
        "## Statistical Gotchas": out.index("## Statistical Gotchas"),
        "## Active Dataset Profile": out.index("## Active Dataset Profile"),
    }
    assert (
        positions["STATIC"]
        < positions["## Operational State"]
        < positions["## Skill Menu"]
        < positions["## Statistical Gotchas"]
        < positions["## Active Dataset Profile"]
    )
