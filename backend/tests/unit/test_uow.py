"""SqlAlchemyUoW just delegates to the session -- checked against a fake
session rather than a real one, so no database connection is needed."""

from dataclasses import dataclass, field

from app.repositories.uow import SqlAlchemyUoW
from app.services.uow import UnitOfWork


@dataclass
class FakeSession:
    committed: bool = False
    rolled_back: bool = False
    calls: list[str] = field(default_factory=list)

    async def commit(self) -> None:
        self.committed = True
        self.calls.append("commit")

    async def rollback(self) -> None:
        self.rolled_back = True
        self.calls.append("rollback")


async def test_commit_delegates_to_the_session() -> None:
    session = FakeSession()
    uow = SqlAlchemyUoW(session)  # type: ignore[arg-type]
    await uow.commit()
    assert session.committed is True
    assert session.calls == ["commit"]


async def test_rollback_delegates_to_the_session() -> None:
    session = FakeSession()
    uow = SqlAlchemyUoW(session)  # type: ignore[arg-type]
    await uow.rollback()
    assert session.rolled_back is True
    assert session.calls == ["rollback"]


def test_sqlalchemy_uow_satisfies_the_service_layer_protocol() -> None:
    # app/services/** may never import sqlalchemy (ruff's banned-api rule);
    # this is the structural proof that the Protocol and the impl actually match.
    uow: UnitOfWork = SqlAlchemyUoW(FakeSession())  # type: ignore[arg-type]
    assert uow is not None
