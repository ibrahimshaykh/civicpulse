from collections.abc import Sequence

import structlog
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import request_id_var
from app.domain.enums import Status
from app.schemas import ErrorBody, ErrorDetail, FieldError

log = structlog.get_logger()


class DomainError(Exception):
    status_code = 500
    code = "internal_error"


class NotFound(DomainError):
    status_code = 404
    code = "not_found"


class InvalidTransition(DomainError):
    status_code = 409
    code = "invalid_transition"

    def __init__(self, current: Status, target: Status, allowed: list[Status]) -> None:
        self.current = current
        self.target = target
        self.allowed = allowed
        reason = (
            f"'{current.value}' is terminal."
            if not allowed
            else f"Allowed from '{current.value}': {', '.join(s.value for s in allowed)}."
        )
        super().__init__(f"Invalid status transition: {current.value} → {target.value}. {reason}")


class RateLimited(DomainError):
    status_code = 429
    code = "rate_limited"

    def __init__(self, retry_after_s: int) -> None:
        self.retry_after_s = retry_after_s
        super().__init__(f"Too many complaints from this address. Try again in {retry_after_s} seconds.")


def _field_name(loc: Sequence[int | str]) -> str:
    """ "body"/"query"/"path" is where pydantic/FastAPI say the value came from,
    not part of the field's name -- plan §10.5: a query param becomes
    "page_size"; a body field becomes "text", not "body.text"."""
    parts = [str(p) for p in loc if p not in ("body", "query", "path")]
    return ".".join(parts) if parts else "__root__"


async def _validation_error_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    fields = [FieldError(field=_field_name(e["loc"]), message=e["msg"], type=e["type"]) for e in exc.errors()]
    body = ErrorBody(
        error=ErrorDetail(
            code="validation_error",
            message="Request validation failed",
            request_id=request_id_var.get(),
            fields=fields,
        )
    )
    return JSONResponse(status_code=400, content=body.model_dump(mode="json", exclude_none=True))


async def _domain_error_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, DomainError)
    request_id = request_id_var.get()
    headers: dict[str, str] = {}
    detail: ErrorDetail
    if isinstance(exc, InvalidTransition):
        detail = ErrorDetail(
            code=exc.code,
            message=str(exc),
            request_id=request_id,
            from_status=exc.current,
            to_status=exc.target,
            allowed=exc.allowed,
        )
    elif isinstance(exc, RateLimited):
        detail = ErrorDetail(
            code=exc.code, message=str(exc), request_id=request_id, retry_after_s=exc.retry_after_s
        )
        headers["Retry-After"] = str(exc.retry_after_s)
    else:
        detail = ErrorDetail(code=exc.code, message=str(exc), request_id=request_id)
    body = ErrorBody(error=detail)
    return JSONResponse(
        status_code=exc.status_code, content=body.model_dump(mode="json", exclude_none=True), headers=headers
    )


async def _http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StarletteHTTPException)
    code = {404: "not_found", 405: "method_not_allowed"}.get(exc.status_code, "http_error")
    body = ErrorBody(error=ErrorDetail(code=code, message=str(exc.detail), request_id=request_id_var.get()))
    return JSONResponse(status_code=exc.status_code, content=body.model_dump(mode="json", exclude_none=True))


async def _unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = request_id_var.get()
    log.exception("unhandled_error", request_id=request_id)
    body = ErrorBody(
        error=ErrorDetail(code="internal_error", message="Unexpected error", request_id=request_id)
    )
    return JSONResponse(status_code=500, content=body.model_dump(mode="json", exclude_none=True))


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, _validation_error_handler)
    app.add_exception_handler(DomainError, _domain_error_handler)
    app.add_exception_handler(StarletteHTTPException, _http_exception_handler)
    app.add_exception_handler(Exception, _unhandled_exception_handler)
