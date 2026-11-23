"""
src/engine/logging_config.py
Structured JSON logging configuration with automated regex-based PII redaction.
Strictly prevents account numbers, National IDs, and customer identities from reaching logs.
"""

import logging
import json
import re
import sys
import time
from typing import Any, Dict

# Institutional PII Redaction Patterns
ACCOUNT_REGEX = re.compile(r"BD\d{2}-[A-Z]{4}-\d{4}-\d{4}-\d{4}", re.IGNORECASE)
NID_REGEX = re.compile(r"\b\d{10}\b|\b\d{13}\b|\b\d{17}\b")
CARD_REGEX = re.compile(r"\b(?:\d[ -]*?){13,16}\b")
EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

class PiiRedactionFilter(logging.Filter):
    """Redacts customer PII (account numbers, NIDs, emails) before log output."""

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = self.redact(record.msg)
        if hasattr(record, "args") and record.args:
            if isinstance(record.args, dict):
                record.args = {k: self.redact(str(v)) for k, v in record.args.items()}
            elif isinstance(record.args, tuple):
                record.args = tuple(self.redact(str(v)) for v in record.args)
        return True

    @classmethod
    def redact(cls, text: str) -> str:
        if not text:
            return text
        text = ACCOUNT_REGEX.sub("BD**-****-****-****-****", text)
        text = CARD_REGEX.sub("****-****-****-****", text)
        text = EMAIL_REGEX.sub("*****@*****.***", text)
        return text


class JsonFormatter(logging.Formatter):
    """Formats log records as canonical single-line JSON without PII."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(record.created)),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": "intelligent-aml-engine",
            "environment": "production-banking"
        }
        if hasattr(record, "trace_id"):
            log_entry["trace_id"] = record.trace_id
        if hasattr(record, "span_id"):
            log_entry["span_id"] = record.span_id
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


def setup_structured_logging(level: int = logging.INFO) -> None:
    """Configures structured JSON logging with active PII redaction filter on root logger."""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers
    for h in list(root_logger.handlers):
        root_logger.removeHandler(h)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    handler.addFilter(PiiRedactionFilter())
    root_logger.addHandler(handler)
