from starlette.requests import Request
from starlette.responses import JSONResponse
from fastmcp import FastMCP

from src.app.config.settings import Settings
from src.app.application.services.llm_service import LLMService
from src.app.providers.factory import ProviderFactory
from src.app.mcp.auth import MCPAuthMiddleware
from src.app.mcp.tools.ask_llm import register_ask_llm_tool
from src.app.infrastructure.logging import get_logger

logger = get_logger("mcp.server")

def create_mcp_app(settings: Settings):
    """
    Builds, configures, and returns the ASGI application hosting the FastMCP server.
    """
    # 1. Instantiate provider & application service via DI
    provider = ProviderFactory.create_provider(settings)
    llm_service = LLMService(provider=provider)

    # 2. Instantiate FastMCP
    mcp = FastMCP(
        name=settings.mcp_server_name,
        instructions="MCP Server bridging Google Gemini to a private local LLM for specialized analysis."
    )

    # 3. Register MCP Tools
    register_ask_llm_tool(mcp, llm_service)

    # 4. Define Health & Diagnostics Routes
    @mcp.custom_route("/", methods=["GET"])
    async def root_endpoint(request: Request):
        return JSONResponse({
            "service": settings.mcp_server_name,
            "status": "online",
            "endpoints": {
                "health": "/health",
                "ready": "/ready",
                "mcp": settings.mcp_path
            }
        })

    @mcp.custom_route("/health", methods=["GET"])
    async def health_endpoint(request: Request):
        return JSONResponse({
            "status": "ok",
            "service": settings.mcp_server_name,
            "provider": settings.llm_provider,
            "model": settings.llm_model,
            "auth_enabled": bool(settings.auth_token)
        })

    @mcp.custom_route("/ready", methods=["GET"])
    async def readiness_endpoint(request: Request):
        is_ready = await llm_service.check_readiness()
        status_code = 200 if is_ready else 503
        return JSONResponse({
            "status": "ready" if is_ready else "degraded",
            "provider_reachable": is_ready,
            "model": settings.llm_model
        }, status_code=status_code)

    @mcp.custom_route(settings.mcp_path, methods=["GET"])
    async def mcp_browser_info(request: Request):
        accept = request.headers.get("accept", "")
        if "text/event-stream" in accept:
            return JSONResponse({"status": "ready", "protocol": "mcp-http"})
            
        return JSONResponse({
            "status": "ready",
            "description": "Model Context Protocol (MCP) HTTP endpoint. Use POST for JSON-RPC 2.0 requests (initialize, tools/list, tools/call).",
            "tool": "ask_local_llm"
        })

    # 5. Build Starlette ASGI app with Stateless HTTP for Gemini
    app = mcp.http_app(transport="http", stateless_http=True, path=settings.mcp_path)

    # 6. Add Authentication Middleware
    app.add_middleware(
        MCPAuthMiddleware,
        auth_token=settings.auth_token,
        exempt_paths={"/", "/health", "/ready"}
    )

    return app
