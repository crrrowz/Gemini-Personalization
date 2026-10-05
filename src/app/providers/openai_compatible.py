import asyncio
from typing import Optional, Dict, Any
import httpx

from src.app.domain.models import LLMRequest, LLMResponse
from src.app.domain.errors import (
    ProviderError,
    ProviderConnectionError,
    ProviderTimeoutError,
    ProviderAuthenticationError,
    ProviderRateLimitError,
)
from src.app.providers.base import LLMProvider
from src.app.infrastructure.http_client import HttpClientFactory
from src.app.infrastructure.logging import get_logger

logger = get_logger("provider.openai")

class OpenAICompatibleProvider(LLMProvider):
    """Production provider for OpenAI-compatible REST endpoints (Ollama, LM Studio, vLLM, etc.)."""

    def __init__(
        self,
        base_url: str,
        model: str,
        api_key: Optional[str] = None,
        timeout: float = 60.0,
        max_retries: int = 2,
        default_system_prompt: Optional[str] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ):
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._api_key = api_key
        self._timeout = timeout
        self._max_retries = max_retries
        self._default_system_prompt = default_system_prompt or "You are a helpful AI assistant."
        self._client = http_client or HttpClientFactory.create_async_client(timeout=timeout)

    @property
    def name(self) -> str:
        return "openai_compatible"

    @property
    def model(self) -> str:
        return self._model

    @property
    def base_url(self) -> str:
        return self._base_url

    async def generate(self, request: LLMRequest) -> LLMResponse:
        endpoint = f"{self._base_url}/chat/completions"
        
        system_content = request.system_prompt or self._default_system_prompt
        messages = [{"role": "system", "content": system_content}]
        
        if request.context:
            user_content = f"Context:\n\"\"\"\n{request.context}\n\"\"\"\n\nQuestion:\n{request.question}"
        else:
            user_content = request.question

        messages.append({"role": "user", "content": user_content})

        payload: Dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            "temperature": request.temperature,
        }
        if request.max_tokens:
            payload["max_tokens"] = request.max_tokens

        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        attempt = 0
        while True:
            attempt += 1
            try:
                logger.debug(f"Sending request to {endpoint} (attempt {attempt}/{self._max_retries + 1})")
                response = await self._client.post(endpoint, json=payload, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    choices = data.get("choices", [])
                    if not choices:
                        raise ProviderError("LLM API returned an empty choices list.")
                    
                    content = choices[0].get("message", {}).get("content", "")
                    usage = data.get("usage")
                    
                    return LLMResponse(
                        content=content.strip(),
                        model=self._model,
                        usage=usage,
                        raw_response=data
                    )
                
                elif response.status_code in (401, 403):
                    error_msg = f"Authentication failed with LLM API (HTTP {response.status_code}): {response.text}"
                    logger.error(error_msg)
                    raise ProviderAuthenticationError(error_msg)
                    
                elif response.status_code == 429:
                    error_msg = f"Rate limit exceeded on LLM API (HTTP 429): {response.text}"
                    logger.warning(error_msg)
                    if attempt > self._max_retries:
                        raise ProviderRateLimitError(error_msg)
                    await asyncio.sleep(2.0 * attempt)
                    continue
                    
                else:
                    error_msg = f"LLM API returned error (HTTP {response.status_code}): {response.text}"
                    if attempt > self._max_retries or response.status_code < 500:
                        raise ProviderError(error_msg)
                    logger.warning(f"Server error HTTP {response.status_code}, retrying... ({attempt}/{self._max_retries})")
                    await asyncio.sleep(1.0 * attempt)
                    continue

            except (httpx.ConnectError, httpx.NetworkError) as e:
                if attempt > self._max_retries:
                    raise ProviderConnectionError(
                        f"Could not connect to LLM backend at {self._base_url}. Please ensure the model server is running.",
                        details=str(e)
                    )
                logger.warning(f"Connection error to LLM backend: {e}. Retrying ({attempt}/{self._max_retries})...")
                await asyncio.sleep(1.0 * attempt)

            except httpx.TimeoutException as e:
                if attempt > self._max_retries:
                    raise ProviderTimeoutError(
                        f"LLM request timed out after {self._timeout}s.",
                        details=str(e)
                    )
                logger.warning(f"LLM request timeout. Retrying ({attempt}/{self._max_retries})...")
                await asyncio.sleep(1.0 * attempt)

    async def check_health(self) -> bool:
        """Performs a lightweight probe to verify connectivity."""
        try:
            # Try /models or base URL
            models_endpoint = f"{self._base_url}/models"
            headers = {}
            if self._api_key:
                headers["Authorization"] = f"Bearer {self._api_key}"
            res = await self._client.get(models_endpoint, headers=headers, timeout=5.0)
            return res.status_code in (200, 401)  # Reachable even if auth needed
        except Exception:
            return False

    async def close(self) -> None:
        """Closes the underlying HTTP client."""
        await self._client.aclose()
