import pytest
import asyncio
from src.app.application.services.llm_service import LLMService
from src.app.providers.fake import FakeLLMProvider

def test_llm_service_success():
    provider = FakeLLMProvider(canned_response="Success: {question}")
    service = LLMService(provider=provider)
    
    result = asyncio.run(service.ask(question="Test Q", context="Context info"))
    assert result == "Success: Test Q"

def test_llm_service_empty_input():
    provider = FakeLLMProvider()
    service = LLMService(provider=provider)
    
    result = asyncio.run(service.ask(question="   "))
    assert "Please provide a valid" in result
    assert len(provider.call_history) == 0

def test_llm_service_connection_error_handling():
    provider = FakeLLMProvider()
    provider.set_simulate_error("connection")
    service = LLMService(provider=provider)
    
    result = asyncio.run(service.ask(question="Test Q"))
    assert "Local LLM is currently unavailable" in result

def test_llm_service_timeout_error_handling():
    provider = FakeLLMProvider()
    provider.set_simulate_error("timeout")
    service = LLMService(provider=provider)
    
    result = asyncio.run(service.ask(question="Test Q"))
    assert "Local LLM request timed out" in result

def test_llm_service_auth_error_handling():
    provider = FakeLLMProvider()
    provider.set_simulate_error("auth")
    service = LLMService(provider=provider)
    
    result = asyncio.run(service.ask(question="Test Q"))
    assert "Authentication failed" in result
