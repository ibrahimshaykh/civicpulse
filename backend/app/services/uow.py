"""The service layer's only view of a database transaction. Services receive
this Protocol, never an AsyncSession, so `app/services/**` can never import
sqlalchemy (ruff's banned-api rule enforces it) -- a service that needs a
session for typing would be a design failure the plan calls out explicitly.
"""

from typing import Protocol


class UnitOfWork(Protocol):
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
