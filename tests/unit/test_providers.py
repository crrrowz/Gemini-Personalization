import pytest
import asyncio
from src.app.domain.models import LLMRequest
from src.app.domain.errors import (
    ProviderConnectionError,
    ProviderTimeoutError,
    ProviderAuthenticationError,
)
from src.app.providers.fake import FakeLLMProvider
from src.app.providers.openai_compatible import OpenAICompatibleProvider
from src.app.providers.factory import ProviderFactory
from src.app.config.settings import Settings

def test_fake_provider_generation():
    provider = FakeLLMProvider(canned_response="Answer to: {question}")
    req = LLMRequest(question="What is Redis?")
    
    resp = asyncio.run(provider.generate(req))
    assert resp.content == "Answer to: What is Redis?"
    assert resp.model == "fake-model-v1"
    assert len(provider.call_history) == 1

def test_fake_provider_error_simulation():
    provider = FakeLLMProvider()
    provider.set_simulate_error("connection")
    
    with pytest.raises(ProviderConnectionError):
        asyncio.run(provider.generate(LLMRequest(question="Hi")))

def test_provider_factory():
    fake_settings = Settings(LLM_PROVIDER="fake", LLM_MODEL="mock-ai")
    p1 = ProviderFactory.create_provider(fake_settings)
    assert isinstance(p1, FakeLLMProvider)
    assert p1.model == "mock-ai"

    openai_settings = Settings(LLM_PROVIDER="openai_compatible", LLM_MODEL="llama-3")
    p2 = ProviderFactory.create_provider(openai_settings)
    assert isinstance(p2, OpenAICompatibleProvider)
    assert p2.model == "llama-3"
