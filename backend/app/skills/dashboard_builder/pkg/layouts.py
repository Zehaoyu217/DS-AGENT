# backend/app/skills/dashboard_builder/pkg/layouts.py
from __future__ import annotations

from typing import Literal

Layout = Literal["bento", "grid", "single_column"]


def resolve_spans(requested: list[int], layout: Layout) -> list[int]:
    if layout == "single_column":
        return [12 for _ in requested]
    if layout == "grid":
        return [4 for _ in requested]
    # bento: honour user spans, clamp to 1..12
    return [max(1, min(12, s)) for s in requested]
