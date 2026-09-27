"""BE-05 acceptance (I12, I13): "/ready reports the failed dependency by
name", proven against a genuinely unreachable host (10.255.255.1, a private,
unrouted address -- plan's own suggested design) rather than a mock. No
Docker needed: the point of this test is precisely that nothing answers on
the other end, and a real connect timeout is what actually fires.
"""

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import create_async_engine

from app.services.readiness_service import ReadinessService

UNROUTABLE_HOST = "10.255.255.1"
CONNECT_TIMEOUT_S = 0.3


async def _ok() -> None:
    return None


async def _ping_unreachable_postgres() -> None:
    engine = create_async_engine(
        f"postgresql+asyncpg://user:pass@{UNROUTABLE_HOST}:5432/db",
        connect_args={"timeout": CONNECT_TIMEOUT_S},
    )
    try:
        async with engine.connect():
            pass
    finally:
        await engine.dispose()


async def _ping_unreachable_redis() -> None:
    redis = Redis(host=UNROUTABLE_HOST, port=6379, socket_connect_timeout=CONNECT_TIMEOUT_S)
    try:
        await redis.ping()
    finally:
        await redis.aclose()


async def test_ready_reports_postgres_failed_by_name_against_a_real_unreachable_host() -> None:
    svc = ReadinessService(
        ping_db=_ping_unreachable_postgres, ping_redis=_ok, timeout_s=1.0, is_shutting_down=lambda: False
    )
    report = await svc.check()

    assert report.ok is False
    assert report.failed == ["postgres"]
    assert report.checks["redis"] == "ok"
    assert report.checks["postgres"].startswith("error:")


async def test_ready_reports_redis_failed_by_name_against_a_real_unreachable_host() -> None:
    svc = ReadinessService(
        ping_db=_ok, ping_redis=_ping_unreachable_redis, timeout_s=1.0, is_shutting_down=lambda: False
    )
    report = await svc.check()

    assert report.ok is False
    assert report.failed == ["redis"]
    assert report.checks["postgres"] == "ok"
    assert report.checks["redis"].startswith("error:")


async def test_ready_reports_both_failed_against_real_unreachable_hosts() -> None:
    svc = ReadinessService(
        ping_db=_ping_unreachable_postgres,
        ping_redis=_ping_unreachable_redis,
        timeout_s=1.0,
        is_shutting_down=lambda: False,
    )
    report = await svc.check()

    assert report.ok is False
    assert set(report.failed) == {"postgres", "redis"}
