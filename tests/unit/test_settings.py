import pytest
from src.app.config.settings import Settings

def test_settings_defaults():
    s = Settings()
    assert s.mcp_host == "0.0.0.0"
    assert s.mcp_port == 8000
    assert s.mcp_path == "/mcp"
    assert s.llm_provider in ("openai_compatible", "fake")
    assert s.llm_timeout == 60.0

def test_settings_path_normalization():
    s = Settings(mcp_path="mcp/v1", llm_base_url="http://localhost:11434/v1/")
    assert s.mcp_path == "/mcp/v1"
    assert s.llm_base_url == "http://localhost:11434/v1"

def test_settings_custom_values():
    s = Settings(
        MCP_PORT="9000",
        LLM_PROVIDER="fake",
        LLM_MODEL="mistral-7b",
        AUTH_TOKEN="secret-123"
    )
    assert s.mcp_port == 9000
    assert s.llm_provider == "fake"
    assert s.llm_model == "mistral-7b"
    assert s.auth_token == "secret-123"
