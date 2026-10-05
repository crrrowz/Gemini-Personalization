import time
from typing import Optional
from src.app.domain.models import LLMRequest, LLMResponse
from src.app.domain.errors import (
    BridgeError,
    ProviderConnectionError,
    ProviderTimeoutError,
    ProviderAuthenticationError,
    ProviderRateLimitError,
    InvalidRequestError,
)
from src.app.providers.base import LLMProvider
from src.app.infrastructure.logging import get_logger

logger = get_logger("service.llm")

class LLMService:
    """Core application service coordinating LLM generation requests and domain policies."""

    def __init__(self, provider: LLMProvider):
        self._provider = provider

    @property
    def provider_name(self) -> str:
        return self._provider.name

    @property
    def model_name(self) -> str:
        return self._provider.model

    async def check_readiness(self) -> bool:
        """Check if the underlying provider is ready."""
        return await self._provider.check_health()

    async def ask(self, question: str, context: Optional[str] = None) -> str:
        """
        Processes a question and context from Gemini, queries the LLM provider,
        and returns a resilient response string.
        """
        # 1. Validation
        if not question or not question.strip():
            logger.warning("Empty question received from Gemini")
            return "Please provide a valid, non-empty question."

        request = LLMRequest(
            question=question.strip(),
            context=context.strip() if context else None
        )

        logger.info(f"[LLMService] Processing question (length: {len(request.question)} chars, context: {bool(request.context)})")
        start_time = time.perf_counter()

        # 2. Execution with comprehensive error handling
        try:
            response: LLMResponse = await self._provider.generate(request)
            elapsed = time.perf_counter() - start_time
            logger.info(f"[LLMService] Response generated successfully in {elapsed:.2f}s (model: {response.model})")
            return response.content

        except ProviderConnectionError as e:
            elapsed = time.perf_counter() - start_time
            logger.error(f"[LLMService] Connection error after {elapsed:.2f}s: {e.message}")
            return f"Local LLM is currently unavailable. Could not connect to the model server. ({e.message})"

        except ProviderTimeoutError as e:
            elapsed = time.perf_counter() - start_time
            logger.error(f"[LLMService] Timeout error after {elapsed:.2f}s: {e.message}")
            return "Local LLM request timed out. The model took too long to respond."

        except ProviderAuthenticationError as e:
            elapsed = time.perf_counter() - start_time
            logger.error(f"[LLMService] Authentication error after {elapsed:.2f}s: {e.message}")
            return "Authentication failed with the local LLM backend. Please verify your LLM_API_KEY."

        except ProviderRateLimitError as e:
            elapsed = time.perf_counter() - start_time
            logger.warning(f"[LLMService] Rate limit error after {elapsed:.2f}s: {e.message}")
            return "Local LLM rate limit exceeded. Please wait a moment before trying again."

        except BridgeError as e:
            elapsed = time.perf_counter() - start_time
            logger.error(f"[LLMService] Bridge error after {elapsed:.2f}s: {e.message}")
            return f"Error from Local LLM Bridge: {e.message}"

        except Exception as e:
            elapsed = time.perf_counter() - start_time
            logger.exception(f"[LLMService] Unexpected error after {elapsed:.2f}s: {str(e)}")
            return "An unexpected error occurred while communicating with the local LLM."
