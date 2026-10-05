from typing import Optional, Dict, Any
from src.app.domain.models import LLMRequest, LLMResponse
from src.app.domain.errors import (
    ProviderConnectionError,
    ProviderTimeoutError,
    ProviderAuthenticationError,
)
from src.app.providers.base import LLMProvider

class FakeLLMProvider(LLMProvider):
    """Deterministic, zero-dependency LLM provider for unit tests and local simulations."""
    
    def __init__(
        self,
        canned_response: str = "This is a deterministic response from FakeLLMProvider.",
        model_name: str = "fake-model-v1",
        simulate_error: Optional[str] = None,
    ):
        self._canned_response = canned_response
        self._model_name = model_name
        self._simulate_error = simulate_error
        self.call_history: list[LLMRequest] = []

    @property
    def name(self) -> str:
        return "fake"

    @property
    def model(self) -> str:
        return self._model_name

    def set_canned_response(self, response: str) -> None:
        self._canned_response = response

    def set_simulate_error(self, error_type: Optional[str]) -> None:
        self._simulate_error = error_type

    async def generate(self, request: LLMRequest) -> LLMResponse:
        self.call_history.append(request)

        if self._simulate_error == "connection":
            raise ProviderConnectionError("Simulated connection failure to local LLM.")
        elif self._simulate_error == "timeout":
            raise ProviderTimeoutError("Simulated timeout waiting for local LLM.")
        elif self._simulate_error == "auth":
            raise ProviderAuthenticationError("Simulated authentication error 401.")

        content = self._canned_response
        if "{question}" in content:
            content = content.replace("{question}", request.question)

        return LLMResponse(
            content=content,
            model=self._model_name,
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
            raw_response={"id": "fake-resp-1"}
        )

    async def check_health(self) -> bool:
        return self._simulate_error is None
