"""ReadinessService against fake ping callables -- deterministic and instant,
covering the branch logic itself. test_ready_route_and_real_unreachable_hosts.py
covers the same behaviour end to end against genuinely unreachable hosts."""

import asyncio

from app.services.readiness_service import ReadinessService


async def _ok() -> None:
    return None


async def _boom() -> None:
    raise ConnectionError("refused")


async def _hangs() -> None:
    await asyncio.sleep(10)


async def test_ready_when_both_dependencies_answer() -> None:
    svc = ReadinessService(ping_db=_ok, ping_redis=_ok, timeout_s=1, is_shutting_down=lambda: False)
    report = await svc.check()
    assert report.ok is True
    assert report.checks == {"postgres": "ok", "redis": "ok"}
    assert report.failed == []


async def test_not_ready_when_postgres_fails() -> None:
    svc = ReadinessService(ping_db=_boom, ping_redis=_ok, timeout_s=1, is_shutting_down=lambda: False)
    report = await svc.check()
    assert report.ok is False
    assert report.checks["postgres"] == "error:ConnectionError"
    assert report.failed == ["postgres"]


async def test_not_ready_when_redis_fails() -> None:
    svc = ReadinessService(ping_db=_ok, ping_redis=_boom, timeout_s=1, is_shutting_down=lambda: False)
    report = await svc.check()
    assert report.failed == ["redis"]


async def test_not_ready_when_both_fail() -> None:
    svc = ReadinessService(ping_db=_boom, ping_redis=_boom, timeout_s=1, is_shutting_down=lambda: False)
    report = await svc.check()
    assert set(report.failed) == {"postgres", "redis"}


async def test_a_hung_dependency_times_out_instead_of_hanging_the_check() -> None:
    svc = ReadinessService(ping_db=_hangs, ping_redis=_ok, timeout_s=0.2, is_shutting_down=lambda: False)
    report = await svc.check()
    assert report.checks["postgres"] == "error:TimeoutError"


async def test_shutting_down_skips_both_probes_and_fails_immediately() -> None:
    probed = {"db": False, "redis": False}

    async def _track_db() -> None:
        probed["db"] = True

    async def _track_redis() -> None:
        probed["redis"] = True

    svc = ReadinessService(
        ping_db=_track_db, ping_redis=_track_redis, timeout_s=1, is_shutting_down=lambda: True
    )
    report = await svc.check()

    assert report.ok is False
    assert report.failed == ["shutting_down"]
    assert report.checks == {"postgres": "skipped", "redis": "skipped"}
    assert probed == {"db": False, "redis": False}  # neither dependency was actually touched
