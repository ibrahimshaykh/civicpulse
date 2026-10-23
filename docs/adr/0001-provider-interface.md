# ADR 0001: The triage provider interface

- Status: Accepted
- Date: 2026-09-29
- Deciders: A, B

## Context

The brief requires at least three interchangeable triage implementations
(rule-based, a hosted LLM, a self-hosted LLM) selected by an environment
variable, with a fourth (`simulated`) needed for tests and demos that must
not depend on a live network. Partner A's `ComplaintService` needs to call
triage on Day 2, long before Partner B's real providers (`AI-01..09`)
exist, so the interface has to be frozen and coded against with a stub
before either partner's concrete work starts (`C0-04`).

The brief's own printed example for this interface uses a synchronous
`def triage(...)`. Every concrete provider we actually need to write is
I/O-bound (an HTTP call to Groq, an HTTP call to a local Ollama server) or,
for the two that aren't, trivially fast (rule matching, a seeded random
draw) — see plan §1.3's own resolution table, row "Protocol printed as
sync `def triage`".

## Decision

`app/providers/triage/base.py` defines the seam as a `Protocol`, not an
abstract base class, with an **async** method:

```python
@runtime_checkable
class TriageProvider(Protocol):
    name: str
    async def triage(self, text: str, location: str) -> TriageResult: ...
```

- **Async, not the brief's printed sync signature.** FastAPI's request
  handlers are already async all the way down (`ComplaintService.create()`
  awaits `TriageService.triage()`); a synchronous `def triage` calling out
  to Groq or Ollama over HTTP would block the single worker's event loop
  for the entire call — up to the full `triage_timeout_s` — stalling every
  other in-flight request on that pod. `RuleBasedTriage` and
  `SimulatedTriage` don't need to be async on their own merits, but giving
  every provider the same async signature is what lets `TriageService`
  call `await self._primary.triage(...)` once, generically, under
  `asyncio.timeout()`, without a per-provider sync/async branch.
- **`Protocol`, not an ABC.** Nothing about this seam needs shared base
  behaviour (a base `__init__`, a template method, inherited state) — every
  concrete provider's `triage()` is a completely different implementation.
  A `Protocol` expresses "these classes happen to have the same shape"
  without forcing them into a common inheritance hierarchy, which matters
  concretely here: `RuleBasedTriage` is also used directly as
  `TriageService`'s `fallback`, constructed and called (`triage_sync`) in
  places that have nothing to do with being "a kind of provider" — an ABC
  would make that inheritance mean something it doesn't.
- **`@runtime_checkable`**, so `isinstance(x, TriageProvider)` is available
  as a static guard if a future task needs one (for example, an
  architecture test asserting every registered provider satisfies the
  shape). Nothing in this codebase actually calls `isinstance` against it
  today — see Consequences below.
- **Frozen on Day 2, alongside `TriageResult`, `TriageOutcome`, and the
  `TriageCache`/`OutcomeSink` Protocols** (`C0-04`), each with a `Null*`
  default implementation. This is what let `BE-03`'s `ComplaintService`
  be written and tested against `tests/fakes.py::StubTriageService` before
  `AI-01`'s `RuleBasedTriage` — the first real provider — existed, and
  what let `AI-08`'s Redis-backed cache and `AI-10`'s Redis-backed outcome
  log land later without changing `TriageService`'s constructor or any of
  its callers.

## Alternatives considered

- **Synchronous interface, run providers in a thread pool.** Matches the
  brief's printed signature exactly. Rejected: it trades one problem
  (blocking the event loop) for a different one (a thread-pool call still
  needs its own timeout/cancellation story to fit `asyncio.timeout()`,
  and Ollama's and Groq's own client libraries are already async-native,
  so this would add a sync-over-async shim for no benefit).
- **Abstract base class (`abc.ABC`) with `triage()` as `@abstractmethod`.**
  Would also work, and would let a shared base hold common logic. Rejected
  because there is no common logic to share — see Decision above — and
  because an ABC forces every provider into one inheritance root, which
  `RuleBasedTriage`'s dual role (provider and `TriageService`'s fallback)
  doesn't need.
- **A plain callable (`Callable[[str, str], Awaitable[TriageResult]]`)
  instead of a class with a `.name`.** Simpler on paper, but every consumer
  (`/api/meta/providers`, the outcome log, the safety floor's `rules`
  special-case) needs to know *which* provider answered, not just get a
  result back — `.name` is load-bearing, not decoration. Rejected.

## Consequences

- Every current and future provider (`RuleBasedTriage`, `SimulatedTriage`,
  `GroqTriage`, `OllamaTriage`) implements the same two-member shape, so
  `factory.py::build_primary` can return any of them from one `match`
  statement and `TriageService` never needs to know which one it holds.
- `@runtime_checkable` is currently decorative: no code in this repository
  calls `isinstance(x, TriageProvider)`. It costs nothing to keep (a
  `Protocol` marked `runtime_checkable` behaves identically to one that
  isn't, until someone actually calls `isinstance`), and it is there
  precisely so a later test or assertion can use it without needing this
  ADR revisited first.
- The async requirement means `RuleBasedTriage.triage()` is `async def`
  even though its body never awaits anything — it exists purely to satisfy
  the shape. `RuleBasedTriage` also exposes a synchronous `triage_sync()`
  for the two callers that need the result without an `await` hop:
  `TriageService`'s own fallback path (already inside an `except` block,
  not worth a further `async` call for a sub-millisecond keyword match),
  and `SimulatedTriage`, which builds on the same rule-based classification
  under a seeded confidence. The "everything is async" rule has exactly
  these two documented, deliberate exceptions rather than an accidental
  inconsistency.

## Verification

- `app/providers/triage/base.py`: the Protocol itself.
- `app/providers/triage/rules.py`, `simulated.py`, `llm.py`, `ollama.py`:
  four independent implementations, none inheriting from a shared base
  class, each satisfying the same shape (test A17 in
  `tests/unit/test_factory.py` selects each one by `TRIAGE_PROVIDER` and
  asserts the concrete type and its threaded-through settings).
- `tests/fakes.py::StubTriageService` and `tests/unit/test_triage_service.py`
  show the seam being coded against and tested independently of any real
  provider, which is the whole point of freezing it on Day 2.
