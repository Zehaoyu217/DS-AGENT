from fastapi.testclient import TestClient

from app.main import create_app


def test_health_returns_ok() -> None:
    app = create_app()
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"


def test_health_includes_version() -> None:
    app = create_app()
    client = TestClient(app)
    response = client.get("/api/health")
    body = response.json()
    assert "version" in body
