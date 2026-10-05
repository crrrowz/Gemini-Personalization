from typing import Optional, Set
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.app.infrastructure.logging import get_logger

logger = get_logger("mcp.auth")

class MCPAuthMiddleware(BaseHTTPMiddleware):
    """Bearer Token / API Key authentication middleware for public MCP endpoints."""

    def __init__(self, app, auth_token: Optional[str] = None, exempt_paths: Optional[Set[str]] = None):
        super().__init__(app)
        self.auth_token = auth_token.strip() if auth_token else None
        self.exempt_paths = exempt_paths or {"/health", "/ready"}

    async def dispatch(self, request: Request, call_next):
        # Allow exempt paths (health checks)
        if request.url.path in self.exempt_paths:
            return await call_next(request)

        # Allow browser GET info if applicable
        if request.method == "GET" and request.url.path in ["/", "/mcp"]:
            # Check if requesting SSE or just visiting via browser
            accept = request.headers.get("accept", "")
            if "text/event-stream" not in accept:
                return await call_next(request)

        # If authentication token is configured, enforce Bearer verification
        if self.auth_token:
            auth_header = request.headers.get("Authorization", "").strip()
            expected_header = f"Bearer {self.auth_token}"
            
            if auth_header != expected_header:
                logger.warning(f"Unauthorized request to {request.url.path} from {request.client.host if request.client else 'unknown'}")
                return JSONResponse(
                    {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32000,
                            "message": "Unauthorized: Invalid or missing Authorization Bearer token."
                        }
                    },
                    status_code=401,
                    headers={"WWW-Authenticate": "Bearer"}
                )

        return await call_next(request)
