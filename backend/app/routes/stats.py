from fastapi import APIRouter, Depends, Response

from app.api.deps import get_stats_service
from app.schemas import StatsOut
from app.services.stats_service import StatsService

router = APIRouter(tags=["stats"])


@router.get("/api/stats", response_model=StatsOut)
async def get_stats(response: Response, svc: StatsService = Depends(get_stats_service)) -> StatsOut:
    stats, cache = await svc.get()
    response.headers["X-Cache"] = cache
    response.headers["Cache-Control"] = "no-store"  # browsers must not cache; Redis is the cache
    return stats
