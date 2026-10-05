from typing import Optional
import httpx

class HttpClientFactory:
    """Creates pooled, robust async HTTP clients for infrastructure communication."""
    
    @staticmethod
    def create_async_client(
        timeout: float = 60.0,
        max_connections: int = 20,
        max_keepalive_connections: int = 10,
    ) -> httpx.AsyncClient:
        limits = httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
            keepalive_expiry=30.0
        )
        return httpx.AsyncClient(
            timeout=httpx.Timeout(timeout, connect=10.0),
            limits=limits,
            follow_redirects=True
        )
