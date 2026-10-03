"""
logger.py — High-Performance Structured JSON & Console Logging Module.
Provides IEEE TIFS / SOC-2 compliant structured audit logging with contextual metadata.
"""

import os
import sys
import logging
import structlog
from typing import Any, Dict


def setup_structured_logging(log_level: str = "INFO"):
    """Configures structlog with standard library logging integration."""
    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )

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


def get_logger(name: str = "intelligent_aml") -> structlog.stdlib.BoundLogger:
    """Returns a structured logger with component binding."""
    return structlog.get_logger(name)
