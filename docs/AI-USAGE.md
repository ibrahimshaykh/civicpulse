# AI-USAGE.md

This project made heavy, direct use of AI coding assistance. This document
says plainly what for, what a human accepted as-is, what got rejected or
corrected and why, and how generated code was verified. It is written to
be checked, not skimmed: every claim below points at a real commit, test,
or file rather than a general impression.

## Tools used

| Tool | Who | What for |
|---|---|---|
| Claude Code (Claude Sonnet 5, Anthropic), connected to GitHub via MCP | Partner A (Ibrahim) | Nearly all backend and frontend implementation, tests, CI configuration, and documentation (this file included) |
| _Partner B's own AI tool usage_ | Partner B (Salman) | _To be filled in by Salman: which tool(s), for which tasks. Recorded separately so this section states only what each of us can personally verify._ |

**Commit attribution.** Claude Code's commits in this repository are
authored as Ibrahim Ahmed / `ibrahimshaykh`, because that is whose GitHub
account authorized the connector (plan §3, "commit attribution warning").
Salman's tasks are committed from his own `SalmanAsadDev` account so that
`git shortlog -sn --no-merges` reflects real authorship, not a proxy —
this was an explicit, repeated instruction throughout the session (see
EV-04's commit audit) rather than an afterthought.

## What Claude was used for

Effectively full end-to-end implementation of Partner A's task list
(`docs/progress.toml`, `owner = "A"`): domain schemas, the repository/UoW
layer, service layer, routes, the read-through stats cache, the graceful
shutdown server, the backend test suite, and the entire frontend (Vite
scaffold, typed API client, every page and component, the Vitest suite).
It was also used, once Partner A's queue was clear, for several
Partner-B-labelled AI-layer tasks whose implementation and tests don't
need a live Groq key or Docker to write and verify (`AI-04` GroqTriage,
`AI-08` the triage cache, `AI-09` OllamaTriage), and for CI configuration,
ADRs, and this document. Every task Claude touched is logged in
`docs/progress.toml`'s `[[log]]` entries with a specific, falsifiable
account of what was built and how it was checked — this document
summarizes that log rather than duplicating it line for line.

**Representative prompts** (verbatim from the session, not paraphrased):

- *"hey so my partner did some hanges to the repo so take the latest pull
  from teh dev branh"* — routine sync-and-continue instruction.
- *"lets ontinue aording to the implenetation plan whats left"* — the
  standing instruction to keep working through the plan's task list.
- *"beffore the doker an we do the i d pipeline"*, followed by *"leave it
  and do the remaining frontend bakend data layer and the ahe layetr and
  the ai layer work that is left"* — a scope decision made by the human,
  not by Claude: don't touch Docker/Kubernetes (Partner B's active work),
  work everything else.
- *"and just start end to end do every thing and dont ask me to shall i
  ontinue automatially start the other task withou me telling and i dont
  want you to stop"* — explicit authorization to proceed through the
  remaining task queue without per-task confirmation, given a fixed window
  of unsupervised time.

## What was accepted as-is

The large majority of Claude's output: it was reviewed by running the
project's own gates (tests, `ruff check`/`ruff format`/`mypy --strict` for
the backend; `eslint`/`tsc`/`vitest` for the frontend; the OpenAPI/typed-client
drift check) rather than by eyeballing the diff and trusting it. Nothing
was merged to `dev` without every one of those passing first, task by
task, PR by PR — the sequence in every commit message and PR description
in this repository is: implement, test, run every gate, *then* commit.

## What was rejected or corrected, and why

This is the part most worth reading closely, because it is the direct
evidence that generated code was checked against reality rather than
trusted:

- **A bug in the plan's own reference code, not Claude's.** The
  implementation plan's literal `TriageService.triage()` snippet caches
  the primary provider's result unconditionally on success — but the same
  document states elsewhere that "no cache is used [for rules], since
  rules are cheaper than Redis." Taken literally, a `rules`-primary
  deployment would still round-trip Redis on every request. Caught while
  writing `AI-03`'s fallback test, not by inspection; fixed by guarding
  the cache write with the same `primary.name != "rules"` check already
  used on the read side.
- **A hand-written migration produced double-prefixed constraint names**
  (`ck_complaints_ck_complaints_text_length`), because `op.create_table`
  re-applies Alembic's naming convention on top of a name that was already
  given the full prefixed form by hand. Caught by a regression test that
  diffs the migration's generated DDL against the ORM model's own compiled
  DDL byte-for-byte, deliberately broken once to confirm the test actually
  catches drift, then fixed by using the same short names the ORM model
  uses (`DB-02`).
- **A real `mypy --strict` error, not a style nitpick.**
  `complaint_repository.py::get_status_stmt` was typed `Select[Any]`, so
  `get_status()` silently returned `Any` instead of `Status | None` — mypy
  caught this only once the CI job ran under the *actually pinned*
  SQLAlchemy version (2.0.54; the working environment had drifted to
  2.1.1). Fixed by typing the statement `Select[Status]` (`CI-01`).
- **A redis-py 5.3.1 typing gap.** `lrange()`'s stub returns a union type
  that fails a bare `await` under `mypy --strict`, because the same stub
  backs both the sync and async Redis clients. Fixed with an explicit
  `cast("Awaitable[list[str]]", ...)`, documented in the code as to why
  the cast is safe at runtime even though the stub can't express it
  (`AI-10`/`outcomes.py`).
- **A suggested synchronous provider interface, from the brief itself, not
  from Claude.** The brief's own printed example for `TriageProvider.triage`
  is a plain `def`. Rejected in favor of `async def` because every real
  provider is I/O-bound over HTTP (Groq, Ollama) and `TriageService` needs
  one generic `await` path under `asyncio.timeout()`, not a per-provider
  sync/async branch — written down and justified in `docs/adr/0001-provider-interface.md`
  (`DOC-02`), including the trade-off this creates (`RuleBasedTriage.triage()`
  is `async def` with a body that never awaits anything, purely to satisfy
  the shape).
- **Claude's own first draft of that same ADR was itself corrected before
  being committed.** It initially claimed `RuleBasedTriage`'s safety-floor
  logic went through `triage_sync()` as a third caller. Grepping the actual
  code (`triage_sync` has exactly two callers: `TriageService`'s fallback
  path, and `SimulatedTriage`) showed the safety floor actually checks
  `HIGH_RISK` keywords directly and never calls into `RuleBasedTriage` at
  all — the claim was corrected before the ADR was published, not after.
  This is deliberately included here as the clearest example in this
  project of Claude's own output being checked against the code and found
  wrong, not just checked against a test suite.
- **A hardcoded, redundant test file, avoided rather than corrected after
  the fact.** `FE-10`'s plan called for a new B-owned test file; in
  practice Partner A's own earlier PRs already wrote every test the plan's
  §8.14 names for it. Writing a second, duplicate file just to manufacture
  a commit against that task ID would have misrepresented real authorship
  for the commit-split rubric item (`A2`/`A4`) — so the task was marked
  done under its true authorship instead of padded with throwaway code.
- **A coverage floor left looser than the plan's own stated target.**
  `backend/pyproject.toml` enforced 65% coverage while the plan's own
  `BE-07` acceptance criterion is "coverage >= 70%" — a gate that doesn't
  match its own stated bar isn't actually enforcing anything. Raised to
  70% (with the matching CI flag) once actual measured coverage (over 90%)
  was confirmed to clear it comfortably, rather than left as a permanently
  loose placeholder (`BE-07`).

## How generated code was verified

- **Automated gates, every task, before every commit:** `pytest` (280
  backend tests as of `AI-09`, over 92% branch coverage, enforced by
  `--cov-fail-under`), `ruff check` / `ruff format --check` / `mypy
  --strict` for the backend; `vitest` (31 frontend tests), `eslint --max-warnings 0`,
  `tsc --noEmit`, and a production `vite build` for the frontend.
- **Contract drift, not just types:** `python -m app.cli export-openapi`
  diffed byte-for-byte against the committed `backend/openapi.json`, and
  `npm run gen:api && npm run check:contract` diffed the generated
  `schema.d.ts` against the committed one, on every task that touched a
  route or a response schema.
- **No live call treated as equivalent to a real one.** Every provider
  that talks to a real network service (`GroqTriage`, `OllamaTriage`) was
  tested exclusively against a mocked client — inspecting the actual
  request the code would send (model, redaction applied, no `location`/
  `reporter_contact` leaked) rather than trusting that it probably does
  the right thing. Where a task's own acceptance criterion needs a genuine
  live call this sandbox cannot make (a real Groq API key, a real Ollama
  model, a live Postgres at 200k rows), the task was left `in_progress` in
  `docs/progress.toml` with that gap stated explicitly, rather than marked
  done on the strength of the mocked tests alone.
- **A real unreachable host, not a mock, for the one behavior that needs
  a genuine failure:** `/ready`'s dependency-failure reporting was tested
  against `10.255.255.1` (a private, unrouted address) with a short
  connect timeout, because the point of that test is precisely that
  nothing answers on the other end — a mock cannot prove a timeout path
  actually fires (`BE-05`).

## What still needs a human check

Per this task's own note in `docs/progress.toml` (`DOC-08`): confirm the
account above is accurate before submission — in particular, that the
"accepted as-is" characterization matches your own recollection of what
you reviewed, and that Partner B fills in their own AI-tool-usage row
above rather than have it stated on their behalf.
