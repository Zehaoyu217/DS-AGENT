# backend/app/skills/dashboard_builder/pkg/__init__.py
from app.skills.reporting.dashboard_builder.pkg import build
from app.skills.reporting.dashboard_builder.pkg.build import (
    DashboardResult,
    DashboardSpec,
    KPICard,
    SectionSpec,
)

__all__ = [
    "DashboardResult",
    "DashboardSpec",
    "KPICard",
    "SectionSpec",
    "build",
]
