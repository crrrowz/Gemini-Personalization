#!/usr/bin/env python3
"""
Verification & Diagnostics script for Gemini Local LLM Bridge.
Tests Health, Readiness, and MCP Tool Discovery.
"""

import sys
import httpx

def run_diagnostics(base_url: str, auth_token: str = "") -> bool:
    base_url = base_url.rstrip("/")
    headers = {"accept": "application/json, text/event-stream"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    print("=" * 60)
    print(f" Gemini Local LLM Bridge - Verification Tool")
    print(f" Target Endpoint: {base_url}")
    print("=" * 60 + "\n")

    # 1. Health Probe
    health_url = f"{base_url}/health"
    try:
        print(f"[1/4] Probing Health Check: GET {health_url} ...")
        res = httpx.get(health_url, timeout=10.0)
        print(f"      HTTP Status: {res.status_code}")
        print(f"      Payload:     {res.text}")
        if res.status_code != 200:
            print("      Health check returned non-200 status code.")
            return False
    except Exception as e:
        print(f"      Connection failed: {e}")
        return False

    # 2. Readiness Probe
    ready_url = f"{base_url}/ready"
    try:
        print(f"\n[2/4] Probing Provider Readiness: GET {ready_url} ...")
        res = httpx.get(ready_url, timeout=10.0)
        print(f"      HTTP Status: {res.status_code}")
        print(f"      Payload:     {res.text}")
    except Exception as e:
        print(f"      Readiness probe warning: {e}")

    # 3. MCP Handshake (Initialize)
    mcp_url = f"{base_url}/mcp"
    try:
        print(f"\n[3/4] Testing MCP Protocol Initialize: POST {mcp_url} ...")
        init_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "mcp-verifier", "version": "1.0.0"}
            }
        }
        res = httpx.post(mcp_url, json=init_payload, headers=headers, timeout=10.0)
        print(f"      HTTP Status: {res.status_code}")
        print(f"      Payload:     {res.text[:180]}...")
        if res.status_code != 200:
            print("      MCP initialization failed.")
            return False
    except Exception as e:
        print(f"      MCP initialize request failed: {e}")
        return False

    # 4. MCP Tool Discovery (tools/list)
    try:
        print(f"\n[4/4] Testing MCP Tool Discovery: POST {mcp_url} (tools/list) ...")
        list_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        res = httpx.post(mcp_url, json=list_payload, headers=headers, timeout=10.0)
        print(f"      HTTP Status: {res.status_code}")
        print(f"      Payload:     {res.text}")
        if "ask_local_llm" in res.text:
            print("\n" + "=" * 60)
            print(" SUCCESS: Server is fully operational & 'ask_local_llm' is ready!")
            print("=" * 60)
            return True
        else:
            print("\n WARNING: 'ask_local_llm' not detected in tool manifest.")
            return False
    except Exception as e:
        print(f"      MCP tools/list failed: {e}")
        return False

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    token = sys.argv[2] if len(sys.argv) > 2 else ""
    success = run_diagnostics(target, token)
    sys.exit(0 if success else 1)
