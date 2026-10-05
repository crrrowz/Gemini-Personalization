from typing import Optional
from fastmcp import FastMCP
from src.app.application.services.llm_service import LLMService
from src.app.infrastructure.logging import get_logger

logger = get_logger("mcp.tool.ask_llm")

def register_ask_llm_tool(mcp: FastMCP, llm_service: LLMService) -> None:
    """
    Registers the 'ask_local_llm' tool onto the FastMCP server instance.
    This acts as a thin adapter between MCP protocol and LLMService.
    """
    @mcp.tool(
        name="ask_local_llm",
        description="Consult the local LLM model for specialized analysis, reasoning, second opinion, or domain-specific queries."
    )
    async def ask_local_llm(question: str, context: Optional[str] = None) -> str:
        """
        Send a question and optional context to the local LLM model and return its answer.
        
        Args:
            question: The question, query, or task to send to the local LLM.
            context: Optional background information, screen observation, code snippet, or conversation context.
        """
        logger.info("[Gemini/MCP] Tool called: ask_local_llm")
        return await llm_service.ask(question=question, context=context)
