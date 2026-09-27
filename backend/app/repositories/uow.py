from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyUoW:
    """Implements app.services.uow.UnitOfWork. Kept in repositories, not
    services, since it holds the actual AsyncSession (plan §10.1's note on the
    services/repositories split)."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
