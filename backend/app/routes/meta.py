from fastapi import APIRouter, Depends

from app.api.deps import get_meta_service
from app.schemas import ProvidersOut
from app.services.meta_service import MetaService

router = APIRouter(tags=["meta"])


@router.get("/api/meta/providers", response_model=ProvidersOut)
async def get_providers(svc: MetaService = Depends(get_meta_service)) -> ProvidersOut:
    return await svc.providers()
