from src.app.config.settings import Settings
from src.app.domain.errors import ConfigurationError
from src.app.providers.base import LLMProvider
from src.app.providers.openai_compatible import OpenAICompatibleProvider
from src.app.providers.fake import FakeLLMProvider

class ProviderFactory:
    """Factory responsible for instantiating the appropriate LLMProvider from settings."""

    @staticmethod
    def create_provider(settings: Settings) -> LLMProvider:
        if settings.llm_provider == "openai_compatible":
            return OpenAICompatibleProvider(
                base_url=settings.llm_base_url,
                model=settings.llm_model,
                api_key=settings.llm_api_key,
                timeout=settings.llm_timeout,
                max_retries=settings.llm_max_retries,
                default_system_prompt=settings.llm_system_prompt
            )
        elif settings.llm_provider == "fake":
            return FakeLLMProvider(
                model_name=settings.llm_model
            )
        else:
            raise ConfigurationError(f"Unsupported LLM provider: {settings.llm_provider}")
