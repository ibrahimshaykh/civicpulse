from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}  # no Depends, no I/O. Liveness = "the event loop answers"


@router.get("/ready")
async def ready() -> dict[str, object]:
    # Stub (C0-05). BE-05 checks Postgres and Redis and returns 503 when either fails.
    return {"status": "ready", "checks": {"postgres": "ok", "redis": "ok"}}
