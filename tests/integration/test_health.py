import pytest
from starlette.testclient import TestClient

def test_health_endpoint(fake_app):
    with TestClient(fake_app) as client:
        res = client.get("/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "ok"
        assert data["provider"] == "fake"
        assert data["model"] == "test-model-fake"
        assert data["auth_enabled"] is True

def test_readiness_endpoint(fake_app):
    with TestClient(fake_app) as client:
        res = client.get("/ready")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "ready"
        assert data["provider_reachable"] is True

def test_root_endpoint(fake_app):
    with TestClient(fake_app) as client:
        res = client.get("/")
        assert res.status_code == 200
        assert "Gemini-Local-LLM-Bridge" in res.json()["service"]
