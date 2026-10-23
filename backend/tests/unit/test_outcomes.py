"""AI-10 acceptance (test A16): newest-first, capped at 20, across two
`OutcomeLog` instances sharing one Redis -- proving state lives in Redis,
not in either instance's memory."""

from uuid import uuid4

import fakeredis

from app.domain.enums import Category, Priority
from app.providers.triage.base import TriageResult
from app.providers.triage.outcomes import OutcomeLog
from app.services.triage_service import TriageOutcome

RESULT = TriageResult(category=Category.roads, priority=Priority.normal, summary="x", confidence=0.5)


def _outcome(triaged_by: str = "rules") -> TriageOutcome:
    return TriageOutcome(RESULT, triaged_by, 5, cache_hit=False, fallback=False, error_class=None)


async def test_A16_recent_is_newest_first_and_capped_at_20_across_two_instances() -> None:
    redis = fakeredis.FakeAsyncRedis()
    writer = OutcomeLog(redis)
    reader = OutcomeLog(redis)  # a second "pod" sharing the same Redis

    for i in range(25):
        await writer.record(uuid4(), _outcome(f"rules-{i}"))

    recent = await reader.recent()
    assert len(recent) == 20
    assert recent[0]["provider"] == "rules-24"  # most recent first
    assert recent[-1]["provider"] == "rules-5"  # oldest of the retained 20


async def test_recent_is_empty_before_anything_is_recorded() -> None:
    redis = fakeredis.FakeAsyncRedis()
    assert await OutcomeLog(redis).recent() == []


async def test_record_carries_the_complaint_id_and_a_timestamp() -> None:
    redis = fakeredis.FakeAsyncRedis()
    log = OutcomeLog(redis)
    complaint_id = uuid4()
    await log.record(complaint_id, _outcome())
    recent = await log.recent()
    assert recent[0]["complaint_id"] == str(complaint_id)
    assert "at" in recent[0]
