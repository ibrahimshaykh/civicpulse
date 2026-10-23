from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, Response

from app.api.deps import enforce_rate_limit, get_complaint_service
from app.domain.enums import Category, Priority, Status
from app.schemas import ComplaintCreate, ComplaintOut, ComplaintPage, ErrorBody, StatusUpdate
from app.services.complaint_service import ComplaintQuery, ComplaintService

router = APIRouter(prefix="/api/complaints", tags=["complaints"])

ERR: dict[int | str, dict[str, Any]] = {
    400: {"model": ErrorBody, "description": "Validation error"},
    404: {"model": ErrorBody, "description": "Complaint not found"},
    409: {"model": ErrorBody, "description": "Invalid status transition"},
    429: {"model": ErrorBody, "description": "Rate limited; see Retry-After"},
}


def _err(*codes: int) -> dict[int | str, dict[str, Any]]:
    return {code: ERR[code] for code in codes}


def _set_rate_limit_headers(request: Request, response: Response) -> None:
    # Headers on every response, including success -- a client should always
    # be able to see how much budget is left, not just when it runs out.
    decision = getattr(request.state, "rate_limit", None)
    if decision is not None:
        response.headers["X-RateLimit-Limit"] = str(decision.limit)
        response.headers["X-RateLimit-Remaining"] = str(decision.remaining)


@router.post(
    "",
    status_code=201,
    response_model=ComplaintOut,
    responses=_err(400, 429),
    dependencies=[Depends(enforce_rate_limit)],
)
async def create_complaint(
    body: ComplaintCreate,
    request: Request,
    response: Response,
    svc: ComplaintService = Depends(get_complaint_service),
) -> ComplaintOut:
    out = await svc.create(body)
    response.headers["Location"] = f"/api/complaints/{out.id}"
    _set_rate_limit_headers(request, response)
    return out


@router.get("/{complaint_id}", response_model=ComplaintOut, responses=_err(400, 404))
async def get_complaint(
    complaint_id: UUID, svc: ComplaintService = Depends(get_complaint_service)
) -> ComplaintOut:
    return await svc.get(complaint_id)


@router.get("", response_model=ComplaintPage, responses=_err(400))
async def list_complaints(
    category: Category | None = None,
    priority: Priority | None = None,
    status: Status | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    svc: ComplaintService = Depends(get_complaint_service),
) -> ComplaintPage:
    q = ComplaintQuery(category=category, priority=priority, status=status, page=page, page_size=page_size)
    return await svc.list(q)


@router.patch("/{complaint_id}/status", response_model=ComplaintOut, responses=_err(400, 404, 409))
async def change_status(
    complaint_id: UUID, body: StatusUpdate, svc: ComplaintService = Depends(get_complaint_service)
) -> ComplaintOut:
    return await svc.change_status(complaint_id, body.status)
