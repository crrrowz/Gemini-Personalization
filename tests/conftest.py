import pytest
from src.app.config.settings import Settings
from src.app.mcp.server import create_mcp_app

@pytest.fixture
def fake_settings():
    return Settings(
        LLM_PROVIDER="fake",
        LLM_MODEL="test-model-fake",
        AUTH_TOKEN="test-secret-token",
        LOG_LEVEL="DEBUG"
    )

@pytest.fixture
def fake_app(fake_settings):
    return create_mcp_app(fake_settings)
