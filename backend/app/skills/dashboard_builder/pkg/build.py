# backend/app/skills/dashboard_builder/pkg/build.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

Layout = Literal["bento", "grid", "single_column"]
Mode = Literal["standalone_html", "a2ui"]
Direction = Literal["up_is_good", "down_is_good"]
SectionKind = Literal["kpi", "chart", "table"]


@dataclass(frozen=True)
class KPICard:
    label: str
    value: float | int | str
    delta: float | None
    comparison_period: str
    direction: Direction
    sparkline_artifact_id: str | None = None
    unit: str | None = None


@dataclass(frozen=True)
class SectionSpec:
    kind: SectionKind
    span: int                        # 1-12 grid columns; bento spans up to 12
    payload: Any                     # KPICard | chart artifact id (str) | table artifact id (str)
    title: str | None = None


@dataclass(frozen=True)
class DashboardSpec:
    title: str
    author: str
    layout: Layout
    sections: tuple[SectionSpec, ...]
    theme_variant: str = "light"
    subtitle: str | None = None


@dataclass(frozen=True)
class DashboardResult:
    mode: Mode
    path: Path | None                # None for a2ui in-memory result
    a2ui_payload: dict[str, Any] | None
    artifact_id: str


_MAX_SECTIONS = 12
_VALID_LAYOUTS = {"bento", "grid", "single_column"}
_VALID_MODES = {"standalone_html", "a2ui"}
_VALID_DIRECTIONS = {"up_is_good", "down_is_good"}


def validate_spec(spec: DashboardSpec) -> None:
    if not spec.sections:
        raise ValueError("EMPTY_DASHBOARD: Dashboard has no sections.")
    if len(spec.sections) > _MAX_SECTIONS:
        raise ValueError(
            f"TOO_MANY_SECTIONS: Dashboard has {len(spec.sections)} sections; maximum is {_MAX_SECTIONS}."
        )
    if spec.layout not in _VALID_LAYOUTS:
        raise ValueError(
            f"UNKNOWN_LAYOUT: Unknown layout '{spec.layout}'. Use bento | grid | single_column."
        )
    for section in spec.sections:
        if section.kind == "kpi":
            kpi: KPICard = section.payload
            if kpi.delta is None:
                raise ValueError(
                    f"KPI_NO_DELTA: KPI '{kpi.label}' has no delta; cards must show delta or be dropped."
                )
            if kpi.direction not in _VALID_DIRECTIONS:
                raise ValueError(
                    f"UNKNOWN_DIRECTION: KPI '{kpi.label}' has direction='{kpi.direction}'. "
                    "Use up_is_good | down_is_good."
                )
