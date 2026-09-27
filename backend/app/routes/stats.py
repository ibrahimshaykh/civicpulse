from fastapi import APIRouter, Response

from app.routes import _stubs
from app.schemas import StatsOut

router = APIRouter(tags=["stats"])


@router.get("/api/stats", response_model=StatsOut)
async def get_stats(response: Response) -> StatsOut:
    # Stub (C0-05). CA-01 makes this a Redis read-through cache that reports HIT or MISS.
    response.headers["X-Cache"] = "MISS"
    response.headers["Cache-Control"] = "no-store"  # browsers must not cache; Redis is the cache
    return _stubs.stats()
