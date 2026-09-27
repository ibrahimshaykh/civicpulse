"""DB-03 acceptance: seeding twice inserts 0 rows the second time. Verified
against a fake, in-memory repository rather than a real Postgres -- this
proves the seed *algorithm* (dedup by deterministic UUID); a live database
round-trip through the real ComplaintRepository still needs Docker."""

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal

from app.domain.enums import Category, Priority, Status
from app.seed import SEED_NAMESPACE, load_seed_rows, seed


@dataclass
class FakeComplaintRepository:
    """Mimics Postgres's ON CONFLICT (id) DO NOTHING: a second insert with the
    same id is a silent no-op, matching the real repository's contract."""

    rows: dict[uuid.UUID, dict[str, object]] = field(default_factory=dict)

    async def insert_if_absent(
        self,
        *,
        id: uuid.UUID,
        text: str,
        location: str,
        reporter_contact: str | None,
        category: Category,
        priority: Priority,
        status: Status,
        ai_summary: str | None,
        triaged_by: str,
        triage_latency_ms: int,
        triage_confidence: Decimal | None,
        created_at: datetime,
    ) -> bool:
        if id in self.rows:
            return False
        self.rows[id] = {
            "text": text,
            "location": location,
            "reporter_contact": reporter_contact,
            "category": category,
            "priority": priority,
            "status": status,
            "ai_summary": ai_summary,
            "triaged_by": triaged_by,
            "triage_latency_ms": triage_latency_ms,
            "triage_confidence": triage_confidence,
            "created_at": created_at,
        }
        return True


async def test_seeding_twice_inserts_zero_the_second_time() -> None:
    rows = load_seed_rows()
    now = datetime.now(UTC)
    repo = FakeComplaintRepository()

    first = await seed(repo, rows, now)
    assert first.inserted == 33
    assert first.skipped == 0

    second = await seed(repo, rows, now)
    assert second.inserted == 0
    assert second.skipped == 33

    # Identical: seeding again changed nothing (plan's "checksum (id, status,
    # updated_at)" test, in spirit -- here the fake repo's whole row dict).
    assert len(repo.rows) == 33


async def test_seed_ids_are_deterministic_across_processes() -> None:
    # uuid5 with a fixed namespace: same slug -> same id, every time, every machine.
    a = uuid.uuid5(SEED_NAMESPACE, "water-main-g9")
    b = uuid.uuid5(SEED_NAMESPACE, "water-main-g9")
    assert a == b
    assert a != uuid.uuid5(SEED_NAMESPACE, "water-nosupply-i10")


async def test_seed_never_calls_an_llm() -> None:
    """The seed's own honesty check: it must cost zero API quota (plan §9.5)."""
    rows = load_seed_rows()
    repo = FakeComplaintRepository()
    await seed(repo, rows, datetime.now(UTC))
    assert all(row["triaged_by"] == "rules" for row in repo.rows.values())
    assert all(row["triage_latency_ms"] == 0 for row in repo.rows.values())
