from fastapi import APIRouter

from app.routes import _stubs
from app.schemas import ProvidersOut

router = APIRouter(tags=["meta"])


@router.get("/api/meta/providers", response_model=ProvidersOut)
async def get_providers() -> ProvidersOut:
    # Stub (C0-05). Later reads the active provider and the last 20 outcomes from Redis.
    return _stubs.providers()
