from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.deps import get_readiness_service
from app.services.readiness_service import ReadinessService

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}  # no Depends, no I/O. Liveness = "the event loop answers"


@router.get("/ready")
async def ready(svc: ReadinessService = Depends(get_readiness_service)) -> JSONResponse:
    r = await svc.check()
    if r.ok:
        return JSONResponse({"status": "ready", "checks": r.checks})
    return JSONResponse({"status": "unavailable", "checks": r.checks, "failed": r.failed}, status_code=503)
