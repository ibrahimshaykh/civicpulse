"""JSON logging to stdout only -- no FileHandler anywhere (grep-checked in BE-08)."""

import logging
import sys
from collections.abc import Mapping, MutableMapping
from contextvars import ContextVar
from typing import Any

import structlog
from structlog.types import Processor

request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


def add_request_id(_: Any, __: str, event_dict: MutableMapping[str, Any]) -> Mapping[str, Any]:
    event_dict.setdefault("request_id", request_id_var.get())
    return event_dict


def configure_logging(level: str) -> None:
    shared: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        add_request_id,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]
    structlog.configure(
        processors=[*shared, structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=shared,
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.processors.JSONRenderer(),
            ],
        )
    )
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)
    for name in ("uvicorn", "uvicorn.error", "sqlalchemy.engine", "httpx"):
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
    logging.getLogger("uvicorn.access").disabled = True  # our middleware writes the access line
    logging.getLogger("httpx").setLevel("WARNING")  # httpx logs full URLs at INFO
