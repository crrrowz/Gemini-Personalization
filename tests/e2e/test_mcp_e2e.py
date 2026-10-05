import pytest
from starlette.testclient import TestClient

def test_mcp_ask_local_llm_e2e(fake_app):
    with TestClient(fake_app) as client:
        # 1. Initialize
        init_res = client.post("/mcp", json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "gemini-e2e-client", "version": "1.0"}
            }
        }, headers={
            "Authorization": "Bearer test-secret-token",
            "accept": "application/json, text/event-stream"
        })
        assert init_res.status_code == 200

        # 2. List tools
        tools_res = client.post("/mcp", json={
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }, headers={
            "Authorization": "Bearer test-secret-token",
            "accept": "application/json, text/event-stream"
        })
        assert tools_res.status_code == 200
        assert "ask_local_llm" in tools_res.text

        # 3. Call tool
        call_res = client.post("/mcp", json={
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "ask_local_llm",
                "arguments": {
                    "question": "What is the capital of France?",
                    "context": "Geography exam"
                }
            }
        }, headers={
            "Authorization": "Bearer test-secret-token",
            "accept": "application/json, text/event-stream"
        })
        assert call_res.status_code == 200
        assert "FakeLLMProvider" in call_res.text
