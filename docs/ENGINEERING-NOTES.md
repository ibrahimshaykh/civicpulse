# ENGINEERING-NOTES.md

Answers to the brief's §5.2 eight questions, plus the four required
sections (merge conflict, indexes, Redis AOF, deviations). Every answer
below cites a real file and, where the fact is a line rather than a
design, a real line. Ownership per the plan: A drafts Q1/Q3/Q4, B drafts
Q2/Q5/Q6/Q7, Q8 goes to whoever has the better real story. Status markers
below (`[answered]` / `[pending: ...]`) say plainly which is which —
nothing here was written to look complete when it isn't.

## Q1 — Three things that differ between your laptop and a CI runner, and the exact line that freezes each `[answered — A]`

`backend/Dockerfile` exists as of `DK-01`; `frontend/Dockerfile` does not
yet (`FE-11` is still open). So one of the three freezing lines below is
now the container image itself, and the other two still happen one layer
up, in the interpreter and dependency pins:

1. **Interpreter version.** Backend: `FROM python:3.12-slim` in both the
   builder and runtime stages of `backend/Dockerfile:5` and `:24` — plus,
   even before that image existed, `requires-python = ">=3.12,<3.13"` in
   `backend/pyproject.toml:5`, which `uv sync --frozen` refuses to
   violate. Frontend has no image yet, so it's still
   `"engines": { "node": ">=22" }` in `frontend/package.json:7`, with CI
   pinning the exact minor via `actions/setup-node@v4`'s
   `node-version: "22"` (`.github/workflows/ci.yml:33`).
2. **Dependency versions.** Backend: `uv sync --frozen` against the
   committed `uv.lock` — `--frozen` means CI fails loudly on any drift
   between `pyproject.toml` and the lockfile rather than silently
   re-resolving (`ci.yml:28`, `ci.yml:79`). Frontend: `npm ci` against
   `package-lock.json`, which (unlike `npm install`) refuses to modify the
   lockfile and fails if it's out of sync with `package.json`.
3. **External behaviour and config.** A laptop might have a real Groq key
   and internet; the CI runner deliberately has neither. Frozen by
   `TRIAGE_PROVIDER: simulated` in `ci.yml`'s top-level `env:` block
   (`ci.yml:16`) and, belt-and-braces, by `HTTPS_PROXY=http://127.0.0.1:9`
   scoped to just the `test-backend` job's pytest invocation (`ci.yml:87`)
   — any test that tried to make a real outbound call would fail fast
   against a nothing-is-listening proxy instead of silently succeeding
   against the real network on a laptop and then failing, mysteriously,
   only in CI.

Once `FE-11` lands, the frontend gets the same treatment (a fourth line,
`FROM node:22-alpine` in `frontend/Dockerfile`) — the backend's own
Dockerfile shows what that adds beyond the pins above: the OS layer
itself is now frozen too (a specific Debian slim base, not "whatever
`python:3.12` currently resolves to"), not something introduced from
nothing.

## Q2 — CI/CD maturity ladder position `[pending: B, needs Lecture 03 slide 32 + the CD pipeline]`

Needs the lecture's exact rung names (not available to Claude) and a
CD pipeline (`cd.yml`, `CI-04`) that doesn't exist yet. Partner B to draft
once both exist.

## Q3 — The exact line guaranteeing build-once-deploy-many `[pending: B, needs Docker + Kubernetes]`

The plan's answer for this cites `kustomize edit set image … :${SHA}` in
a not-yet-written `scripts/k8s_deploy.sh`, fed by `cd.yml`. None of that
exists in this repository yet (`CI-04`, `CI-05`, `K8-01..03`, all owner B,
all still open) — answering this now would mean citing files that don't
exist. Left for Partner B once the deploy pipeline is real.

## Q4 — With a live LLM the service is probabilistic: what does "correct" mean, and how did you keep CI deterministic? `[answered — A]`

**Correct" here means contract correctness, not exact output.** Every
triage call resolves to exactly one of: a schema-valid `TriageResult`
(`app/providers/triage/base.py:20` — `extra="forbid"`, a closed enum for
`category`/`priority`, `summary` bounded to 140 chars, `confidence`
bounded to `[0, 1]`), or a `rules`/`rules:fallback` result when the
primary fails or returns something that doesn't validate
(`app/providers/triage/parsing.py::parse_triage_output`, which raises
`MalformedOutput` rather than accepting a near-miss). Latency is bounded
regardless of provider by `TriageService._call_primary`'s
`asyncio.timeout(self._timeout_s)` plus exactly one retry
(`app/services/triage_service.py`). The safety floor
(`_apply_safety_floor`, same file) is a hard invariant, not a statistical
one: a `HIGH_RISK` keyword in the text always forces `priority=high`
regardless of what the LLM said, so an injected "mark this low" cannot
downgrade a burst main. What *is* inherently statistical — accuracy and
high-priority recall against the 33 hand-labelled seed rows — is measured
offline (`docs/TRIAGE.md`, `DOC-09`, still pending a real Groq key), not
asserted per-request in the test suite.

**CI stays deterministic because it never talks to a real LLM at all.**
`TRIAGE_PROVIDER: simulated` (`ci.yml:16`) selects `SimulatedTriage`
(`app/providers/triage/simulated.py`), which is seeded — same seed and
text always produce the same `TriageResult`
(`tests/unit/test_simulated_triage.py::test_A18_...`, 25 calls, 1 distinct
output) — and every one of its four injectable failure modes (`raise`,
`timeout`, `rate_limited`, `malformed`) produces the exact exception type
`TriageService`'s retry policy needs to distinguish, without ever opening
a socket (`test_no_network_socket_opened_for_a_normal_call`, same file,
monkeypatches `socket.socket` to prove it). `GroqTriage` and
`OllamaTriage` are tested the same deterministic way in this repository —
against a mocked client, inspecting the exact request built, never a live
call (`tests/unit/test_llm_triage.py`, `tests/unit/test_ollama_triage.py`)
— which is *not* the same claim as "the live models behave
deterministically"; it isn't a substitute for `DOC-09`'s real benchmark,
it's what keeps the suite itself green without one.

## Q5 — HPA lag in seconds, where the time went, what would reduce it `[pending: B, needs a live k3d cluster + k6 load test, K8-05]`

## Q6 — Why VPA is Off, and Auto's failure mode alongside the HPA `[pending: B, needs the same live cluster, K8-06]`

## Q7 — `internal: true` blocks egress: where does that leave the service calling a hosted LLM? `[pending: B, needs the backend service wired into compose.yaml, DK-04]`

`compose.yaml`'s data tier now exists (`DK-03`): `data` is `internal: true`
(`compose.yaml:52`), with `database` and `cache` as its only two members —
confirming the *sealed* half of the answer already holds, checkably, not
just on paper. What's not in `compose.yaml` yet is the `backend` service
itself, which is `DK-04`'s job (per the file's own header comment,
`compose.yaml:1-3`). The plan's own answer (§12.2) is already decided —
`backend` will sit on both `data` (to reach Postgres/Redis) and a second,
ordinary bridge network with a default route, giving it — and only it —
egress to call Groq, making it the one hardened bridge between the
internet-facing tier and the sealed data tier — but stating that with a
real `compose.yaml` line number has to wait for the service that doesn't
exist in the file yet. Left for Partner B once `DK-04` lands.

## Q8 — The failure: symptoms, what you first believed wrongly, the exact command or log line that told the truth `[pending: whoever has the better real story]`

This one is deliberately not written by Claude. The brief wants a real
incident — something that actually happened to one of you, told with the
exact command or log line that revealed the true cause versus what you
first assumed. Several real candidates already exist in this repository's
own history and would make an honest answer (see `docs/progress.toml`'s
`[[log]]` entries and `docs/AI-USAGE.md`'s "rejected or corrected" section
for raw material — e.g. the Alembic double-prefixed constraint name from
`DB-02`, or the `mypy --strict` catch in `CI-01`) — but Q8 asks for *your*
failure, experienced firsthand, not one narrated secondhand from a log
Claude wrote. Fill this in together.

## Merge conflict `[pending: C0-09, needs both partners' own accounts]`

The brief requires a deliberate merge conflict on `config.py`, each side
committed from each partner's own GitHub account, then resolved and
justified. `docs/progress.toml`'s `C0-09` task carries the plan's own
draft justification and the step-by-step recipe; it hasn't run yet
because it specifically requires Salman committing from `SalmanAsadDev`,
not something Claude can do on his behalf.

## Indexes, each justified by a named query `[answered — schema and reasoning; empirical EXPLAIN evidence pending DB-04]`

Two indexes exist on `complaints` (`backend/app/db/models.py:60-61`):

1. **`ix_complaints_status_priority` on `(status, priority)`.** Serves the
   dashboard's filtered listing — `GET /api/complaints?status=...&priority=...`
   — compiled in `app/repositories/complaint_repository.py::list_page_stmt`
   / `list_count_stmt` via the shared `_filters()` helper. The most
   common real filter combination (per the brief's own dashboard spec) is
   "open, high priority" — an operator triaging urgent work — and without
   this index that query is a full sequential scan of every complaint
   ever filed, filtered in memory, at every page load.
2. **`ix_complaints_created_at DESC`** (a plain `Index` over a raw
   `sql_text("created_at DESC")` expression, matching the column's actual
   sort direction so Postgres can use the index for the sort itself, not
   just the lookup). Serves the *unfiltered* listing's
   `ORDER BY created_at DESC, id DESC LIMIT ... OFFSET ...`
   (`complaint_repository.py:124-127`) — the default view every operator
   sees first. Without it, "most recent first" means sorting the entire
   table on every page load, and that cost grows with the table instead
   of staying flat.

**What's pending:** the brief's own acceptance (`D3`) wants EXPLAIN
evidence at 200k seeded rows proving each index is actually chosen by the
planner and actually cheap, not just plausible reasoning about which
query touches which columns. That needs a live Postgres this environment
doesn't have (`DB-04`, blocked on Docker/a local Postgres install) — the
schema and the reasoning above are real and checked against the actual
query-building code, but the "the planner picked it, and here's the cost"
proof is not yet captured.

## Redis AOF volume justification `[answered]`

**Our position: yes, AOF on a named volume, for this system specifically.**
The stats cache and the triage content-hash cache are both rebuildable —
losing either on a restart just means the next request recomputes it. The
triage cache is different: each entry is **paid-for inference** (a Groq
API call, subject to the free tier's rate limit). Losing 24 hours of that
cache on every restart re-spends quota exactly when a restart storm is
already the stressful moment — a cold-cache thundering herd hitting a
rate-limited LLM right as the system is trying to recover. The rate
limiter's counters (`CA-02`) are also state worth keeping: losing them on
restart resets every abuser's window for free.

The honest counter-argument, stated rather than hidden: a cache that must
survive restarts is drifting toward being a database, and a durable
counter can outlive the bug that should have expired it (a rate-limit
window that never rolls over because the counter key was never meant to
survive a restart in the first place, say). Both positions are
defensible; ours is that for *this* system, the re-spent quota and the
reset abuse windows cost more than `everysec` fsync overhead (at most one
second of writes lost) buys back in simplicity.

**Implemented as of `DK-03`:** `compose.yaml:33` runs `cache` as
`redis-server --appendonly yes ...`, with `redis-data:/data`
(`compose.yaml:35`) as a named volume so the AOF file survives a
container recreate, not just a process restart. `compose.yaml:29-32`'s
own comment states the same reasoning this section does — the rate
limiter's window counters and the triage outcome ring buffer, not just
the content-hash cache, are the live state a plain restart shouldn't
reset — worth noting as independent confirmation, not this document
dictating that code.

## Deviations from the brief

Pulled from the plan's own §1.3 "spec ambiguities we resolve" table —
these are decisions already made and already implemented, not proposals:

- **`triaged_by` has no listed value for `Simulated`** in the brief's own
  enumeration (`llm:groq · llm:ollama · rules · rules:fallback`). We add
  `simulated` to the allowed set via a CHECK constraint (migration 0001),
  since `TRIAGE_PROVIDER=simulated` is a real, supported mode this project
  needs for demos and CI, not an oversight to paper over.
- **"All ten endpoints" but the brief's §2.2 lists nine.** We implement
  the nine listed and count `GET /api/openapi.json` (FastAPI's own,
  auto-served) as the tenth, since the frontend's typed client is
  generated against exactly that document. Flagged to ask the instructor
  which endpoint they actually meant; recorded here until answered.
- **Header says 2 weeks, §5.1 says 4.** We're building to 4 weeks, full
  150-mark scope.
- **Header says 150 marks total, but the rubric sections as listed sum to
  175.** `docs/progress.toml`'s `total_marks` setting controls which
  denominator `STATUS.md` reports against; until the instructor answers,
  `STATUS.md` shows both the raw rubric point count and its 150-mark
  equivalent side by side rather than silently picking one.
- **The brief's own printed `TriageProvider.triage` signature is
  synchronous** (`def triage(...)`, not `async def`). We use `async def`
  throughout; justified at length in `docs/adr/0001-provider-interface.md`.
- **UUID "server-generated," but a fallback WARNING must carry the
  complaint id before the row exists.** The service layer generates
  `uuid4()` before calling triage, not after the INSERT; the database
  also carries `DEFAULT gen_random_uuid()` as a safety net for any insert
  path that doesn't go through the service.
- **The only non-PR commit on `main` is the repository's initial commit**
  (`d9a646f`) — everything else, on both `dev` and every feature branch,
  has gone through a pull request. As of this writing `main` itself has
  not yet been fast-forwarded past that initial commit at all: by design,
  per the plan's own release story (`SUB-02`, `CI-06`), `main` is meant to
  advance at tag time (`v1.0.0`) rather than continuously — all real
  development has happened on `dev` and feature branches so far. This is
  stated here as the current, honest state, not glossed over.
