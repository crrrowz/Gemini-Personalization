from abc import ABC, abstractmethod
from src.app.domain.models import LLMRequest, LLMResponse

class LLMProvider(ABC):
    """Abstract interface for all LLM backend providers."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Provider identifier."""
        pass

    @property
    @abstractmethod
    def model(self) -> str:
        """Active model identifier."""
        pass

    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generates text completion from the LLM provider.
        
        Args:
            request: Standardized LLMRequest domain object.
            
        Returns:
            LLMResponse containing generated content and metadata.
            
        Raises:
            ProviderConnectionError: Connection to LLM backend failed.
            ProviderTimeoutError: LLM backend timed out.
            ProviderAuthenticationError: Invalid API credentials.
            ProviderRateLimitError: Backend rate limit reached.
            ProviderError: Other backend errors.
        """
        pass

    @abstractmethod
    async def check_health(self) -> bool:
        """Quick health check to test provider reachability."""
        pass
