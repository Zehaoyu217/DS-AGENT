# Testing Guide

## Backend (pytest)

```bash
cd backend
pytest                           # all tests
pytest tests/unit/               # unit only
pytest tests/integration/        # integration only
pytest -v -k "test_config"      # specific test
pytest --cov=app --cov-report=term-missing  # coverage
```

Target: 80% coverage minimum.

## Frontend (vitest)

```bash
cd frontend
npm test                         # all tests
npm run test:watch               # watch mode
```

## Skill Evals

```bash
make skill-eval                  # all skills
make skill-eval skill=timeseries # specific skill
```

Skill evals test agent behavior against sealed assertions — see `docs/skill-creation.md`.

## Writing Tests

Follow the AAA pattern (Arrange-Act-Assert):

```python
def test_config_loads_defaults() -> None:
    # Arrange
    # (config auto-loads from env)

    # Act
    config = get_config()

    # Assert
    assert config.environment == "test"
```
