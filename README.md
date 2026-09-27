# CivicPulse

Municipal complaint triage for CS4032 Software Construction and Design, Assignment 01. Citizens report a problem; an LLM classifies it by category and priority, with a rule-based fallback, so a burst water main never waits behind three streetlight reports.

**Project status:** see [STATUS.md](STATUS.md) for progress and marks secured so far.
**Plan:** [docs/IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md).

The full README (architecture diagram, one-command quickstart, API table, screenshots) arrives with task DOC-01.

## Updating the status page

After finishing a task, set its status in `docs/progress.toml`, then run:

    python scripts/update_status.py

Commit `docs/progress.toml` and `STATUS.md` together with the task's work. CI fails if they're out of sync.
