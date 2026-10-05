import logging
import sys
import re
from typing import Optional

class SecretFilter(logging.Filter):
    """Filter that obfuscates sensitive API keys and tokens from logs."""
    
    TOKEN_PATTERNS = [
        (re.compile(r"Bearer\s+([a-zA-Z0-9_\-\.]{8,})", re.IGNORECASE), r"Bearer [REDACTED]"),
        (re.compile(r"api[-_]?key['\":\s=]+([a-zA-Z0-9_\-\.]{8,})", re.IGNORECASE), r"api_key=[REDACTED]"),
        (re.compile(r"token['\":\s=]+([a-zA-Z0-9_\-\.]{8,})", re.IGNORECASE), r"token=[REDACTED]"),
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            for pattern, replacement in self.TOKEN_PATTERNS:
                record.msg = pattern.sub(replacement, record.msg)
        return True

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Configures root and application loggers with secret sanitization."""
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Root handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(numeric_level)
    handler.addFilter(SecretFilter())
    
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    
    # Configure app logger
    logger = logging.getLogger("gemini_bridge")
    logger.setLevel(numeric_level)
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False
    
    return logger

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a named logger with proper hierarchy."""
    if name:
        return logging.getLogger(f"gemini_bridge.{name}")
    return logging.getLogger("gemini_bridge")
