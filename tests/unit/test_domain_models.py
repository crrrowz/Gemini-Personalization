import pytest
from src.app.domain.models import LLMRequest, LLMResponse
from src.app.domain.errors import (
    BridgeError,
    ProviderConnectionError,
    ProviderTimeoutError,
    ProviderAuthenticationError,
)

def test_llm_request_immutability():
    req = LLMRequest(question="Test question?", context="Context info")
    assert req.question == "Test question?"
    assert req.context == "Context info"
    assert req.temperature == 0.3
    
    with pytest.raises(Exception):
        req.question = "New question"  # dataclass is frozen

def test_llm_response_creation():
    resp = LLMResponse(
        content="Hello world",
        model="test-model",
        usage={"total_tokens": 15}
    )
    assert resp.content == "Hello world"
    assert resp.model == "test-model"
    assert resp.usage["total_tokens"] == 15

def test_error_hierarchy():
    err = ProviderConnectionError("Failed to reach LLM", details="Refused")
    assert isinstance(err, BridgeError)
    assert err.message == "Failed to reach LLM"
    assert err.details == "Refused"
