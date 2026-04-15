from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

GOTCHA_SLUGS: tuple[str, ...] = (
    "base_rate_neglect",
    "berksons_paradox",
    "confounding",
    "ecological_fallacy",
    "immortal_time_bias",
    "look_ahead_bias",
    "multicollinearity",
    "multiple_comparisons",
    "non_stationarity",
    "regression_to_mean",
    "selection_bias",
    "simpsons_paradox",
    "spurious_correlation",
    "survivorship_bias",
)

_REPO_ROOT = Path(__file__).resolve().parents[3]
_GOTCHA_DIR = _REPO_ROOT / "knowledge" / "gotchas"
_INDEX_FILE = _GOTCHA_DIR / "INDEX.md"


@dataclass(frozen=True)
class GotchaIndex:
    entries: dict[str, str]

    def as_injection(self) -> str:
        return "\n".join(
            f"- **{slug}** — {text}" for slug, text in self.entries.items()
        )


def load_index() -> GotchaIndex:
    raw = _INDEX_FILE.read_text(encoding="utf-8")
    entries: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.startswith("- "):
            continue
        body = line[2:].strip()
        if " — " not in body and " -- " not in body:
            continue
        sep = " — " if " — " in body else " -- "
        slug_part, desc = body.split(sep, 1)
        slug = slug_part.strip().strip("*`_ ")
        entries[slug] = desc.strip()
    missing = set(GOTCHA_SLUGS) - set(entries)
    if missing:
        raise RuntimeError(f"INDEX.md missing gotchas: {sorted(missing)}")
    return GotchaIndex(entries={slug: entries[slug] for slug in GOTCHA_SLUGS})


def load_gotcha(slug: str) -> str:
    if slug not in GOTCHA_SLUGS:
        raise KeyError(f"unknown gotcha: {slug}")
    path = _GOTCHA_DIR / f"{slug}.md"
    return path.read_text(encoding="utf-8")
