from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_job(monkeypatch):
    # Fake task object
    class FakeTask:
        id = "fake-job-id-123"

    # Fake function instead of real Celery call
    def fake_compute_sum_parallel(number):
        return FakeTask()

    # Override real function
    monkeypatch.setattr("app.main.compute_sum_parallel", fake_compute_sum_parallel)

    response = client.post("/jobs", json={"number": 5})

    assert response.status_code == 200
    data = response.json()

    assert data["job_id"] == "fake-job-id-123"
    assert data["status"] == "PENDING"


def test_invalid_input():
    response = client.post("/jobs", json={"number": -1})
    assert response.status_code == 422