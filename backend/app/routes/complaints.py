from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Query, Response

from app.domain.enums import Category, Priority, Status
from app.routes import _stubs
from app.schemas import ComplaintCreate, ComplaintOut, ComplaintPage, ErrorBody, StatusUpdate

router = APIRouter(prefix="/api/complaints", tags=["complaints"])

ERR: dict[int | str, dict[str, Any]] = {
    400: {"model": ErrorBody, "description": "Validation error"},
    404: {"model": ErrorBody, "description": "Complaint not found"},
    409: {"model": ErrorBody, "description": "Invalid status transition"},
    429: {"model": ErrorBody, "description": "Rate limited; see Retry-After"},
}


def _err(*codes: int) -> dict[int | str, dict[str, Any]]:
    return {code: ERR[code] for code in codes}


# Stub bodies (C0-05): signatures and response models are the contract; BE-03/BE-04
# replace each body with a call into ComplaintService.


@router.post("", status_code=201, response_model=ComplaintOut, responses=_err(400, 429))
async def create_complaint(body: ComplaintCreate, response: Response) -> ComplaintOut:
    out = _stubs.complaint().model_copy(
        update={"text": body.text, "location": body.location, "reporter_contact": body.reporter_contact}
    )
    response.headers["Location"] = f"/api/complaints/{out.id}"
    return out


@router.get("/{complaint_id}", response_model=ComplaintOut, responses=_err(400, 404))
async def get_complaint(complaint_id: UUID) -> ComplaintOut:
    return _stubs.complaint().model_copy(update={"id": complaint_id})


@router.get("", response_model=ComplaintPage, responses=_err(400))
async def list_complaints(
    category: Category | None = None,
    priority: Priority | None = None,
    status: Status | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> ComplaintPage:
    return ComplaintPage(items=[_stubs.complaint()], total=1, page=page, page_size=page_size, pages=1)


@router.patch("/{complaint_id}/status", response_model=ComplaintOut, responses=_err(400, 404, 409))
async def change_status(complaint_id: UUID, body: StatusUpdate) -> ComplaintOut:
    return _stubs.complaint().model_copy(
        update={"id": complaint_id, "status": body.status, "allowed_transitions": []}
    )
