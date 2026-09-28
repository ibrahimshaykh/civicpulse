"""CA-02 acceptance: atomicity (INCR+EXPIRE in one script), the limit itself,
and fail-open when Redis is unavailable. Against fakeredis, which runs the
real Lua script through its own EVAL implementation -- not a hand-rolled
counter that could drift from what real Redis does."""

import fakeredis
import pytest
from redis.exceptions import RedisError

from app.providers.rate_limiter import RedisFixedWindowLimiter


@pytest.fixture
def redis() -> fakeredis.FakeAsyncRedis:
    return fakeredis.FakeAsyncRedis()


async def test_allows_up_to_the_limit_then_blocks(redis: fakeredis.FakeAsyncRedis) -> None:
    limiter = RedisFixedWindowLimiter(redis, limit=3, window_s=60)
    decisions = [await limiter.hit("1.2.3.4") for _ in range(4)]
    assert [d.allowed for d in decisions] == [True, True, True, False]
    assert decisions[-1].retry_after_s > 0


async def test_remaining_counts_down(redis: fakeredis.FakeAsyncRedis) -> None:
    limiter = RedisFixedWindowLimiter(redis, limit=3, window_s=60)
    first = await limiter.hit("1.2.3.4")
    second = await limiter.hit("1.2.3.4")
    assert first.remaining == 2
    assert second.remaining == 1


async def test_different_clients_have_independent_budgets(redis: fakeredis.FakeAsyncRedis) -> None:
    limiter = RedisFixedWindowLimiter(redis, limit=1, window_s=60)
    a = await limiter.hit("1.1.1.1")
    b = await limiter.hit("2.2.2.2")
    assert a.allowed is True
    assert b.allowed is True


async def test_fails_open_when_redis_is_unavailable() -> None:
    class BrokenRedis:
        def register_script(self, script: str) -> object:
            async def _raise(*, keys: list[str], args: list[object]) -> None:
                raise RedisError("boom")

            return _raise

    limiter = RedisFixedWindowLimiter(BrokenRedis(), limit=3, window_s=60)  # type: ignore[arg-type]
    decision = await limiter.hit("1.2.3.4")
    assert decision.allowed is True
    assert decision.remaining == decision.limit
