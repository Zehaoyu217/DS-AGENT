# backend/app/skills/dashboard_builder/pkg/a2ui.py
from __future__ import annotations

from typing import Any

from app.skills.reporting.dashboard_builder.pkg.build import DashboardSpec, KPICard
from app.skills.reporting.dashboard_builder.pkg.kpi import render_kpi_tile
from app.skills.reporting.dashboard_builder.pkg.layouts import resolve_spans


def to_a2ui(spec: DashboardSpec) -> dict[str, Any]:
    spans = resolve_spans([s.span for s in spec.sections], layout=spec.layout)
    tiles: list[dict[str, Any]] = []
    for section, span in zip(spec.sections, spans, strict=True):
        if section.kind == "kpi":
            kpi: KPICard = section.payload
            rendered = render_kpi_tile(kpi, span=span)
            tiles.append(
                {
                    "kind": "kpi",
                    "span": span,
                    "label": rendered.label,
                    "value": rendered.value,
                    "delta": rendered.delta_str,
                    "delta_class": rendered.delta_class,
                    "comparison_period": rendered.comparison_period,
                    "sparkline_artifact_id": kpi.sparkline_artifact_id,
                }
            )
        elif section.kind == "chart":
            tiles.append(
                {
                    "kind": "chart",
                    "span": span,
                    "title": section.title,
                    "artifact_id": str(section.payload),
                }
            )
        elif section.kind == "table":
            tiles.append(
                {
                    "kind": "table",
                    "span": span,
                    "title": section.title,
                    "artifact_id": str(section.payload),
                }
            )
        else:
            raise ValueError(f"Unknown section kind '{section.kind}'")

    return {
        "a2ui_version": "1",
        "kind": "dashboard",
        "title": spec.title,
        "subtitle": spec.subtitle,
        "author": spec.author,
        "layout": spec.layout,
        "theme_variant": spec.theme_variant,
        "tiles": tiles,
    }
