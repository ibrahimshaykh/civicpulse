import re
from time import perf_counter
from typing import Any
from uuid import uuid4

import structlog
from starlette.datastructures import Headers, MutableHeaders
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.core.logging import request_id_var
from app.core.metrics import HTTP_LATENCY, HTTP_REQUESTS

log = structlog.get_logger()

# Max 128 chars, [A-Za-z0-9-_.]: never echo attacker-supplied junk into logs or headers.
_RID_RE = re.compile(r"[A-Za-z0-9\-_.]{1,128}")


def _route_template(scope: Scope) -> str:
    """The path *template* ("/api/complaints/{complaint_id}"), not the raw path --
    using the raw path would let a scanner hitting random URLs create unbounded
    Prometheus label cardinality."""
    route = scope.get("route")
    path = getattr(route, "path", None)
    return path if isinstance(path, str) else "unmatched"


class RequestContextMiddleware:
    """Pure ASGI (not BaseHTTPMiddleware), so contextvars and streaming responses
    behave correctly -- BaseHTTPMiddleware runs the downstream app in a separate
    task, which breaks contextvar propagation back to the middleware."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = Headers(scope=scope)
        rid = headers.get("x-request-id") or str(uuid4())
        if not _RID_RE.fullmatch(rid):
            rid = str(uuid4())
        token = request_id_var.set(rid)
        structlog.contextvars.bind_contextvars(request_id=rid)
        start = perf_counter()
        status_holder: dict[str, Any] = {"code": 500}

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":
                status_holder["code"] = message["status"]
                MutableHeaders(scope=message).append("X-Request-ID", rid)
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            route = _route_template(scope)
            dur = perf_counter() - start
            HTTP_REQUESTS.labels(scope["method"], route, str(status_holder["code"])).inc()
            HTTP_LATENCY.labels(scope["method"], route).observe(dur)
            if route not in ("/health", "/ready", "/metrics"):
                log.info(
                    "request_completed",
                    method=scope["method"],
                    route=route,
                    status=status_holder["code"],
                    duration_ms=round(dur * 1000, 1),
                )
            structlog.contextvars.clear_contextvars()
            request_id_var.reset(token)
