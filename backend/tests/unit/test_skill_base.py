from app.skills.base import SkillError, SkillResult


def test_skill_error_formats_message() -> None:
    error_templates = {
        "COLUMN_NOT_FOUND": {
            "message": "Column '{column}' not found in table '{table}'",
            "guidance": "Available columns: {available_columns}. Did you mean: {suggestions}?",
            "recovery": "Fix the column name and retry",
        }
    }
    err = SkillError(
        code="COLUMN_NOT_FOUND",
        context={
            "column": "price",
            "table": "sales",
            "available_columns": ["date", "revenue"],
            "suggestions": ["price_usd"],
        },
        templates=error_templates,
    )
    formatted = err.format()
    assert "Column 'price' not found in table 'sales'" in formatted
    assert "Available columns: ['date', 'revenue']" in formatted
    assert "Did you mean: ['price_usd']" in formatted
    assert "Fix the column name and retry" in formatted


def test_skill_error_without_template_falls_back() -> None:
    err = SkillError(
        code="UNKNOWN_ERROR",
        context={"detail": "something broke"},
        templates={},
    )
    formatted = err.format()
    assert "UNKNOWN_ERROR" in formatted
    assert "something broke" in formatted


def test_skill_result_with_data() -> None:
    result = SkillResult(data={"rows": 10, "columns": ["a", "b"]})
    assert result.data["rows"] == 10
    assert result.artifacts == []
    assert result.events == []


def test_skill_result_with_artifacts() -> None:
    result = SkillResult(
        data=None,
        artifacts=[{"type": "chart", "title": "My Chart", "spec": {}}],
    )
    assert len(result.artifacts) == 1
    assert result.artifacts[0]["type"] == "chart"
