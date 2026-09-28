"""The explicit status transition table (task BE-04). `MappingProxyType` +
`frozenset` makes it immutable at runtime -- the frontend never holds its
own copy of this table; it only ever renders `ComplaintOut.allowed_transitions`,
which the service computes from here.
"""

from types import MappingProxyType
from typing import Final

from app.domain.enums import Status

TRANSITIONS: Final[MappingProxyType[Status, frozenset[Status]]] = MappingProxyType(
    {
        Status.open: frozenset({Status.in_progress, Status.rejected}),
        Status.in_progress: frozenset({Status.resolved, Status.rejected}),
        Status.resolved: frozenset(),
        Status.rejected: frozenset(),
    }
)

_ORDER: Final = list(Status)


def allowed_from(current: Status) -> list[Status]:
    return sorted(TRANSITIONS[current], key=_ORDER.index)


def is_allowed(current: Status, target: Status) -> bool:
    return target in TRANSITIONS[current]
