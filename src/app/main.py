import sys
import uvicorn
from dotenv import load_dotenv

# Preload .env if available
load_dotenv()

from src.app.config.settings import get_settings
from src.app.infrastructure.logging import setup_logging
from src.app.mcp.server import create_mcp_app

settings = get_settings()
logger = setup_logging(settings.log_level)

# ASGI application instance for uvicorn
app = create_mcp_app(settings)

def run():
    """Main execution function for starting the MCP server."""
    display_host = "localhost" if settings.mcp_host == "0.0.0.0" else settings.mcp_host
    logger.info(f"Starting {settings.mcp_server_name} on http://{display_host}:{settings.mcp_port}{settings.mcp_path}")
    logger.info(f"Health check: http://{display_host}:{settings.mcp_port}/health")
    logger.info(f"Readiness check: http://{display_host}:{settings.mcp_port}/ready")
    logger.info(f"Active Provider: {settings.llm_provider} (Model: {settings.llm_model})")
    
    uvicorn.run(
        "src.app.main:app",
        host=settings.mcp_host,
        port=settings.mcp_port,
        log_level=settings.log_level.lower(),
        reload=False
    )

if __name__ == "__main__":
    run()
