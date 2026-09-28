"""BE-06 acceptance: `GracefulServer.handle_exit` flips readiness to failing
*before* delegating to uvicorn's own drain -- proven here as an ordering
unit test. The full subprocess + SIGTERM + live-drain scenario (plan
§10.11's `test_graceful_shutdown.py`) is a genuine integration test that
needs a running Postgres/Redis to actually serve a POST; it stays a
separate, still-open task until Docker/Compose exists in this environment.
"""

from app.core import lifecycle
from app.server import GracefulServer


def test_handle_exit_sets_shutting_down_before_calling_super() -> None:
    calls: list[str] = []

    def fake_super_handle_exit(self: GracefulServer, sig: int, frame: object) -> None:
        # By the time uvicorn's own handler runs, shutting_down must already
        # be True -- that's what makes /ready fail immediately on SIGTERM.
        calls.append("super_handle_exit")
        assert lifecycle.shutting_down is True

    import uvicorn

    original = uvicorn.Server.handle_exit
    uvicorn.Server.handle_exit = fake_super_handle_exit  # type: ignore[method-assign]
    lifecycle.shutting_down = False
    try:
        server = GracefulServer.__new__(GracefulServer)
        server.handle_exit(15, None)
    finally:
        uvicorn.Server.handle_exit = original  # type: ignore[method-assign]
        lifecycle.shutting_down = False

    assert calls == ["super_handle_exit"]
