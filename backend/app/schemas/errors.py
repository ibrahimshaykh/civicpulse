from pydantic import BaseModel

from app.domain.enums import Status


class FieldError(BaseModel):
    field: str  # "text", "location", "page_size"
    message: str  # human-readable, from Pydantic
    type: str  # "string_too_short", "enum", ...


class ErrorDetail(BaseModel):
    code: str  # "validation_error" | "not_found" | "invalid_transition" | "rate_limited" | "internal_error"
    message: str  # rendered verbatim by the frontend
    request_id: str
    fields: list[FieldError] | None = None
    from_status: Status | None = None
    to_status: Status | None = None
    allowed: list[Status] | None = None
    retry_after_s: int | None = None


class ErrorBody(BaseModel):
    """The one envelope every 4xx/5xx response uses (plan D6)."""

    error: ErrorDetail
