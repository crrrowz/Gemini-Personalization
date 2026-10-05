import pytest
from starlette.testclient import TestClient

def test_unauthorized_access(fake_app):
    with TestClient(fake_app) as client:
        # Request /mcp without Authorization header
        res = client.post("/mcp", json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        })
        assert res.status_code == 401
        assert "Unauthorized" in res.json()["error"]["message"]

def test_authorized_access(fake_app):
    with TestClient(fake_app) as client:
        # Request /mcp with correct Bearer token
        res = client.post("/mcp", json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list",
            "params": {}
        }, headers={
            "Authorization": "Bearer test-secret-token",
            "accept": "application/json, text/event-stream"
        })
        assert res.status_code == 200
        assert "ask_local_llm" in res.text
