import os
from typing import Optional, Literal
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Central application settings validated via Pydantic."""
    
    # MCP Server Settings
    mcp_host: str = Field(default="0.0.0.0", validation_alias="MCP_HOST")
    mcp_port: int = Field(default=8000, validation_alias="MCP_PORT")
    mcp_path: str = Field(default="/mcp", validation_alias="MCP_PATH")
    mcp_server_name: str = Field(default="Gemini-Local-LLM-Bridge", validation_alias="MCP_SERVER_NAME")
    
    # Gemini Auth Settings
    auth_token: Optional[str] = Field(default=None, validation_alias="AUTH_TOKEN")
    
    # LLM Provider Configuration
    llm_provider: Literal["openai_compatible", "fake"] = Field(default="openai_compatible", validation_alias="LLM_PROVIDER")
    llm_base_url: str = Field(default="http://127.0.0.1:11434/v1", validation_alias="LLM_BASE_URL")
    llm_api_key: Optional[str] = Field(default=None, validation_alias="LLM_API_KEY")
    llm_model: str = Field(default="llama3.2", validation_alias="LLM_MODEL")
    llm_timeout: float = Field(default=60.0, ge=1.0, le=600.0, validation_alias="LLM_TIMEOUT")
    llm_max_retries: int = Field(default=2, ge=0, le=5, validation_alias="LLM_MAX_RETRIES")
    llm_system_prompt: Optional[str] = Field(
        default="You are a helpful AI assistant serving as a specialized local intelligence node. Analyze the provided context and question carefully, and provide clear, accurate, and concise answers.",
        validation_alias="LLM_SYSTEM_PROMPT"
    )

    # Logging Settings
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(default="INFO", validation_alias="LOG_LEVEL")

    # Compatibility backward fallback aliases
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @field_validator("mcp_path")
    @classmethod
    def normalize_path(cls, v: str) -> str:
        if not v.startswith("/"):
            return f"/{v}"
        return v

    @field_validator("llm_base_url")
    @classmethod
    def normalize_url(cls, v: str) -> str:
        return v.rstrip("/")

# Global cached settings instance
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Retrieve or initialize application settings."""
    global _settings
    if _settings is None:
        # Check backward-compatible variable names if new ones aren't set
        if "LOCAL_LLM_BASE_URL" in os.environ and "LLM_BASE_URL" not in os.environ:
            os.environ["LLM_BASE_URL"] = os.environ["LOCAL_LLM_BASE_URL"]
        if "LOCAL_LLM_API_KEY" in os.environ and "LLM_API_KEY" not in os.environ:
            os.environ["LLM_API_KEY"] = os.environ["LOCAL_LLM_API_KEY"]
        if "LOCAL_LLM_MODEL" in os.environ and "LLM_MODEL" not in os.environ:
            os.environ["LLM_MODEL"] = os.environ["LOCAL_LLM_MODEL"]
        if "LOCAL_LLM_TIMEOUT" in os.environ and "LLM_TIMEOUT" not in os.environ:
            os.environ["LLM_TIMEOUT"] = os.environ["LOCAL_LLM_TIMEOUT"]
        if "HOST" in os.environ and "MCP_HOST" not in os.environ:
            os.environ["MCP_HOST"] = os.environ["HOST"]
        if "PORT" in os.environ and "MCP_PORT" not in os.environ:
            os.environ["MCP_PORT"] = os.environ["PORT"]
            
        _settings = Settings()
    return _settings
