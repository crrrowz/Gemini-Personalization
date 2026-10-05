from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass(frozen=True)
class LLMRequest:
    """Standardized internal representation of an LLM generation request."""
    question: str
    context: Optional[str] = None
    system_prompt: Optional[str] = None
    temperature: float = 0.3
    max_tokens: Optional[int] = None

@dataclass(frozen=True)
class LLMResponse:
    """Standardized internal representation of an LLM generation response."""
    content: str
    model: str
    usage: Optional[Dict[str, int]] = None
    raw_response: Optional[Dict[str, Any]] = None
