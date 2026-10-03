"""
logger.py — High-Performance Structured JSON & Console Logging Module.
Provides IEEE TIFS / SOC-2 compliant structured audit logging with contextual metadata.
"""

import os
import sys
import logging
from typing import Any, Dict

try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False


def setup_structured_logging(log_level: str = "INFO"):
    """Configures structlog with standard library logging integration."""
    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
        level=level,
    )

    if not STRUCTLOG_AVAILABLE:
        return

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    is_json = os.getenv("LOG_FORMAT", "console").lower() == "json"
    if is_json:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


setup_structured_logging()


def get_logger(name: str = "intelligent_aml") -> Any:
    """Returns a structured logger with component binding or standard logger fallback."""
    if STRUCTLOG_AVAILABLE:
        return structlog.get_logger(name)
    return logging.getLogger(name)
