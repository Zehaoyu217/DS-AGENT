from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class SeriesStroke:
    width: float
    dash: list[int] | None


@dataclass(frozen=True)
class VariantTokens:
    """A single variant's resolved tokens."""

    name: str
    raw: dict[str, Any]
    series_strokes: dict[str, SeriesStroke]
    typography: dict[str, Any]

    def surface(self, key: str) -> str:
        return str(self.raw["surface"][key])

    def series_color(self, role: str) -> str:
        return str(self.raw["series_blues"][role])

    def series_stroke(self, role: str) -> SeriesStroke:
        return self.series_strokes[role]

    def semantic(self, role: str) -> str:
        return str(self.raw["semantic"][role])

    def categorical(self) -> list[str]:
        return list(self.raw["categorical"])

    def diverging(self) -> dict[str, str]:
        return dict(self.raw["diverging"])

    def chart(self, key: str) -> Any:
        return self.raw["chart"][key]

    def typography_override(self) -> dict[str, Any]:
        return dict(self.typography)


@dataclass(frozen=True)
class ThemeTokens:
    variants: dict[str, dict[str, Any]]
    typography: dict[str, Any]
    series_strokes: dict[str, SeriesStroke]
    default_variant: str

    @classmethod
    def load(cls, path: Path) -> ThemeTokens:
        data = yaml.safe_load(path.read_text())
        _validate_tokens_shape(data, path)
        strokes = {
            role: SeriesStroke(width=float(s["width"]), dash=s.get("dash"))
            for role, s in data["series_strokes"].items()
        }
        return cls(
            variants=data["variants"],
            typography=data["typography"],
            series_strokes=strokes,
            default_variant=data["default_variant"],
        )

    def for_variant(self, name: str) -> VariantTokens:
        if name not in self.variants:
            raise KeyError(name)
        return VariantTokens(
            name=name,
            raw=self.variants[name],
            series_strokes=self.series_strokes,
            typography=dict(self.variants[name].get("typography_override", {})),
        )

    def default(self) -> VariantTokens:
        return self.for_variant(self.default_variant)


_REQUIRED_VARIANT_KEYS = (
    "surface",
    "series_blues",
    "semantic",
    "categorical",
    "diverging",
    "chart",
)


def _validate_tokens_shape(data: Any, path: Path) -> None:
    """Shallow shape check for tokens.yaml. Raises ValueError with a clear message."""
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level must be a mapping, got {type(data).__name__}")
    variants = data.get("variants")
    if not isinstance(variants, dict) or not variants:
        raise ValueError(
            f"{path}: 'variants' must be a non-empty mapping of variant name to tokens"
        )
    default_variant = data.get("default_variant")
    if not isinstance(default_variant, str):
        raise ValueError(f"{path}: 'default_variant' must be a string")
    if default_variant not in variants:
        raise ValueError(
            f"{path}: 'default_variant' {default_variant!r} is not present in 'variants' "
            f"(available: {sorted(variants)})"
        )
    if not isinstance(data.get("typography"), dict):
        raise ValueError(f"{path}: top-level 'typography' must be a mapping")
    if not isinstance(data.get("series_strokes"), dict):
        raise ValueError(f"{path}: top-level 'series_strokes' must be a mapping")
    for variant_name, variant in variants.items():
        if not isinstance(variant, dict):
            raise ValueError(
                f"{path}: variant {variant_name!r} must be a mapping, got {type(variant).__name__}"
            )
        for key in _REQUIRED_VARIANT_KEYS:
            if key not in variant:
                raise ValueError(
                    f"{path}: variant {variant_name!r} is missing required key {key!r}"
                )
