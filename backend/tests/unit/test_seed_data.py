"""DB-03 acceptance: 33 rows, every category and status present, counts match
the brief's own breakdown (plan §9.5)."""

from app.seed import load_seed_rows


def test_thirty_three_rows_with_unique_slugs() -> None:
    rows = load_seed_rows()
    assert len(rows) == 33
    assert len({r.slug for r in rows}) == 33


def test_category_counts_match_the_plan() -> None:
    rows = load_seed_rows()
    counts: dict[str, int] = {}
    for r in rows:
        counts[r.category.value] = counts.get(r.category.value, 0) + 1
    assert counts == {
        "water": 6,
        "electricity": 6,
        "sanitation": 6,
        "roads": 6,
        "streetlights": 5,
        "other": 4,
    }


def test_status_counts_match_the_plan() -> None:
    rows = load_seed_rows()
    counts: dict[str, int] = {}
    for r in rows:
        counts[r.status.value] = counts.get(r.status.value, 0) + 1
    assert counts == {"open": 17, "in_progress": 9, "resolved": 4, "rejected": 3}


def test_every_category_and_status_appears() -> None:
    from app.domain.enums import Category, Status

    rows = load_seed_rows()
    assert {r.category for r in rows} == set(Category)
    assert {r.status for r in rows} == set(Status)


def test_every_row_satisfies_the_check_constraints() -> None:
    """Mirrors the DB check constraints (plan §9.1), so a seed row that would be
    rejected by Postgres fails here first, without needing a live database."""
    rows = load_seed_rows()
    for r in rows:
        assert 10 <= len(r.text) <= 2000, r.slug
        assert 3 <= len(r.location) <= 200, r.slug
        assert len(r.summary) <= 140, r.slug
        assert r.days_ago >= 0, r.slug
