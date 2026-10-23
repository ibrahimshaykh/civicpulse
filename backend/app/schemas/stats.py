from datetime import datetime

from pydantic import BaseModel

from app.domain.enums import Category, Priority, Status


class StatsOut(BaseModel):
    total: int
    # Every enum key is present, zero-filled, so the frontend never guesses at missing buckets.
    by_category: dict[Category, int]
    by_priority: dict[Priority, int]
    by_status: dict[Status, int]
    generated_at: datetime
