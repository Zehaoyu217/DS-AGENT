from __future__ import annotations

import time
import uuid
from typing import Any, Literal

from pydantic import BaseModel, Field

ArtifactType = Literal[
    "table", "chart", "diagram", "dashboard_component", "profile", "analysis", "file",
]


class Artifact(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    type: ArtifactType = "table"
    name: str = ""
    title: str = ""
    description: str = ""
    content: str = ""
    format: str = "html"
    session_id: str = ""
    created_at: float = Field(default_factory=time.time)
    metadata: dict[str, Any] = Field(default_factory=dict)
    chart_data: dict[str, Any] | None = None
    total_rows: int | None = None
    displayed_rows: int | None = None
    profile_summary: str | None = None


class ProgressStep(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    label: str
    status: Literal["pending", "running", "done", "error"] = "pending"
    detail: str = ""
    started_at: float | None = None
    finished_at: float | None = None
