import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ReadinessReport:
    ok: bool
    checks: dict[str, str]
    failed: list[str] = field(default_factory=list)


class ReadinessService:
    """`/health` is "the event loop answers"; `/ready` is "this pod should
    receive traffic". Both Postgres and Redis are probed concurrently, each
    under its own timeout, so a hung dependency can't make the endpoint itself
    hang (plan §10.8).
    """

    def __init__(
        self,
        ping_db: Callable[[], Awaitable[None]],
        ping_redis: Callable[[], Awaitable[None]],
        timeout_s: float,
        is_shutting_down: Callable[[], bool],
    ) -> None:
        self._ping_db = ping_db
        self._ping_redis = ping_redis
        self._timeout_s = timeout_s
        self._is_shutting_down = is_shutting_down

    async def check(self) -> ReadinessReport:
        if self._is_shutting_down():
            # Draining: fail /ready immediately without even probing, so the pod
            # leaves the Service's endpoint list as fast as possible (BE-06).
            return ReadinessReport(
                ok=False, checks={"postgres": "skipped", "redis": "skipped"}, failed=["shutting_down"]
            )
        pg, rd = await asyncio.gather(self._probe(self._ping_db), self._probe(self._ping_redis))
        checks = {"postgres": pg, "redis": rd}
        failed = [name for name, result in checks.items() if result != "ok"]
        return ReadinessReport(ok=not failed, checks=checks, failed=failed)

    async def _probe(self, fn: Callable[[], Awaitable[None]]) -> str:
        # Deliberately broad: any failure at all means "not ready".
        try:
            await asyncio.wait_for(fn(), timeout=self._timeout_s)
            return "ok"
        except Exception as e:
            return f"error:{type(e).__name__}"
