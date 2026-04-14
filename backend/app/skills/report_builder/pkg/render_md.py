# backend/app/skills/report_builder/pkg/render_md.py
from __future__ import annotations

from datetime import date as _date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.skills.report_builder.pkg.build import ReportSpec, Template, validate_spec

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_DIR)),
    autoescape=select_autoescape(enabled_extensions=("html",), default_for_string=False),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_md(spec: ReportSpec, template: Template = "research_memo", today: _date | None = None) -> str:
    validate_spec(spec, template)
    tpl = _env.get_template(f"{template}.md.j2")
    return tpl.render(spec=spec, today=(today or _date.today()).isoformat())
