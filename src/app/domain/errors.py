class BridgeError(Exception):
    """Base exception for all domain and application errors."""
    def __init__(self, message: str, details: str = ""):
        super().__init__(message)
        self.message = message
        self.details = details

class ConfigurationError(BridgeError):
    """Raised when application configuration is invalid or missing."""
    pass

class ProviderError(BridgeError):
    """Base exception for LLM provider errors."""
    pass

class ProviderConnectionError(ProviderError):
    """Raised when the LLM provider cannot be reached (e.g. host down or network failure)."""
    pass

class ProviderTimeoutError(ProviderError):
    """Raised when the LLM provider takes longer than the configured timeout."""
    pass

class ProviderAuthenticationError(ProviderError):
    """Raised when the LLM provider rejects authentication (HTTP 401/403)."""
    pass

class ProviderRateLimitError(ProviderError):
    """Raised when the LLM provider rejects request due to rate limiting (HTTP 429)."""
    pass

class InvalidRequestError(BridgeError):
    """Raised when the request parameters are invalid."""
    pass
