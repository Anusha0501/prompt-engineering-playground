from fastapi.testclient import TestClient

from backend.main import app


def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_compare_mock_zero_shot():
    client = TestClient(app)
    response = client.post(
        "/compare",
        json={
            "task": "Explain tokens to a beginner",
            "provider": "mock",
            "model": "demo-model",
            "strategies": ["zero_shot"],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["title"] == "Zero Shot"
    assert "Mock response" in data["results"][0]["output"]
