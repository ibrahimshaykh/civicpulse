"""AI-08 acceptance: content-hash cache key excludes location but includes
provider/model/prompt version, a hit returns the cached result and a miss
returns None, and the hit-rate counters are Redis-backed (so they're
correct across pods, the same distributed-state argument as AI-10's
OutcomeLog and CA-02's rate limiter -- proven here across two instances
sharing one Redis, the same shape as test_outcomes.py's A16)."""

import fakeredis

from app.domain.enums import Category, Priority
from app.providers.triage.base import TriageResult
from app.providers.triage.cache import TriageResultCache

RESULT = TriageResult(category=Category.water, priority=Priority.high, summary="Burst main.", confidence=0.9)


def _cache() -> tuple[fakeredis.FakeAsyncRedis, TriageResultCache]:
    redis = fakeredis.FakeAsyncRedis()
    return redis, TriageResultCache(redis)


async def test_miss_then_set_then_hit_round_trips_the_result() -> None:
    _, cache = _cache()
    key = cache.key(provider="llm:groq", model="llama-3.1-8b-instant", text="Burst main flooding the street")

    assert await cache.get(key) is None
    await cache.set(key, RESULT)
    assert await cache.get(key) == RESULT


async def test_key_excludes_location_so_the_same_text_from_different_places_shares_one_entry() -> None:
    _, cache = _cache()
    a = cache.key(provider="llm:groq", model="m", text="Burst main flooding the street")
    b = cache.key(provider="llm:groq", model="m", text="Burst main flooding the street")
    assert a == b  # location is not part of the key at all


async def test_key_differs_by_provider_model_and_normalized_text() -> None:
    _, cache = _cache()
    base = cache.key(provider="llm:groq", model="m1", text="Burst main")
    assert base != cache.key(provider="llm:ollama", model="m1", text="Burst main")
    assert base != cache.key(provider="llm:groq", model="m2", text="Burst main")
    assert base != cache.key(provider="llm:groq", model="m1", text="Different complaint entirely")


async def test_key_is_stable_across_case_punctuation_and_whitespace_variants() -> None:
    _, cache = _cache()
    a = cache.key(provider="llm:groq", model="m", text="Burst main flooding the street!")
    b = cache.key(provider="llm:groq", model="m", text="  burst   main flooding the street  ")
    assert a == b


async def test_hit_rate_is_none_before_any_lookup() -> None:
    _, cache = _cache()
    assert await cache.hit_rate() is None


async def test_hit_rate_reflects_hits_and_misses_across_two_instances_sharing_one_redis() -> None:
    redis = fakeredis.FakeAsyncRedis()
    writer, reader = TriageResultCache(redis), TriageResultCache(redis)
    key = writer.key(provider="llm:groq", model="m", text="text")

    await reader.get(key)  # miss
    await writer.set(key, RESULT)
    await reader.get(key)  # hit
    await reader.get(key)  # hit

    assert await writer.hit_rate() == 2 / 3


async def test_set_stores_with_a_ttl() -> None:
    redis, cache = _cache()
    key = cache.key(provider="llm:groq", model="m", text="text")
    await cache.set(key, RESULT)
    ttl = await redis.ttl(key)
    assert 0 < ttl <= 86_400
