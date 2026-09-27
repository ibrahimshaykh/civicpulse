"""App lifespan. Minimal for now: DB-02/CA-01 extend this to open and close the
Postgres and Redis pools; BE-05/BE-06 read `shutting_down` from /ready and the
graceful-shutdown drain.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

shutting_down = False


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    global shutting_down
    shutting_down = False
    yield
    shutting_down = True
