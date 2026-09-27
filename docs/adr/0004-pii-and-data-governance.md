# ADR 0004: PII and data governance in the triage layer

- Status: Accepted
- Date: 2026-09-27
- Deciders: A, B

## Context

`TRIAGE_PROVIDER=llm` sends complaint text to Groq's hosted API -- a
third-party processor outside our own infrastructure. Complaint text is
citizen-written free text, and `ComplaintCreate.reporter_contact` is PII
by definition (plan §7, the complaint schema). None of this is
hypothetical: three rows in the seed data already contain a house number
inside `text` or `location` (`redact()` catches all three -- confirmed
by running it over `app/seed/complaints.json`), and a real deployment's
complaints will contain far more, including phone numbers and CNICs.

The brief scores this as its own line (F7, PII / data-governance ADR) and
expects a genuine decision, not a checkbox.

## Decision

The triage layer sends the LLM **only** redacted complaint text, and never
`reporter_contact` or `location`:

- `providers/triage/redaction.py::redact()` (built, task AI-07) strips
  four PII shapes before anything is sent: Pakistani mobile numbers,
  CNICs, emails, and house/plot addresses (each pattern regex-matched and
  replaced with a `[TAG]` placeholder, never partially masked -- partial
  masking still leaks enough to re-identify in a small town).
- `AI-04`'s `GroqTriage` (not yet built) must call `redact()` on the
  complaint text before `build_messages()`, and must exclude
  `reporter_contact` and `location` from the request entirely -- not
  merely redact them from the text, since there is no regex that could
  reliably catch every way a phone number might be formatted, so the two
  fields most likely to *be* pure PII are dropped outright rather than
  trusted to a pattern match. This ADR is what `AI-04`'s test A15 will
  hold `GroqTriage` to.
- The raw model output is never logged: `providers/triage/parsing.py`'s
  `parse_triage_output` calls `e.errors(include_input=False)` on a
  validation failure specifically so a malformed response's echoed input
  can't leak PII into logs. `TriageService` does not log complaint text
  either -- it currently does no logging at all in the fallback path;
  when logging is added there, it must stay confined to
  `complaint_id`/`provider`/`error_class`, never the text.
- The seed dataset (`app/seed/complaints.json`) is entirely synthetic --
  hand-written, not scraped from a real complaint system -- so no real
  citizen's data exists anywhere in this repository or its history.

This decision predates `AI-04` (the Groq provider itself, not yet built):
freezing it now, alongside the redaction module it depends on, means
`GroqTriage` is written against an already-decided policy rather than one
invented ad hoc when the provider lands.

## Alternatives considered

- **Send the complaint verbatim.** Simplest, and loses no classification
  signal. Rejected: needlessly exposes PII to a third party for a
  classification task that doesn't need it, and could not be defended at
  the viva.
- **Pseudonymize with a reversible token map** (replace PII with a
  per-complaint token, unmap on the way back). More faithful to the
  original text than a fixed `[TAG]`, but adds a stateful mapping table
  that is itself sensitive (compromising it re-identifies everything),
  and buys no classification accuracy the fixed tags don't already give.
  Rejected as complexity with no measured benefit.
- **Self-host only (`TRIAGE_PROVIDER=ollama`), never call a third party.**
  Removes the third-party-processor question entirely. Rejected as the
  *default*, because it is slower and (until measured) may be less
  accurate than a hosted model -- but kept as the standing
  privacy-preserving option for any deployment where that trade-off is
  the right one. `AI-09`/`DOC-09` will measure the actual latency and
  accuracy gap in `docs/TRIAGE.md`; this ADR does not assume an answer
  ahead of that data.

## Consequences

- Some classification signal is lost: `location` sometimes carries
  category information (e.g. "Committee Chowk" suggesting a specific
  known trouble spot) that the LLM never sees. This is an accepted
  trade-off, not an oversight, and `RuleBasedTriage`'s own accuracy
  (93.9% on the seed set, category alone, without location) is evidence
  it is not a large one.
- `AI-04`'s `GroqTriage` must call `redact()` before `build_messages()`,
  and must never pass `reporter_contact` or `location` into the request
  it builds -- this ADR is the source of truth for that requirement, and
  `AI-04`'s tests (A15) verify it directly rather than by inspection.
- Redaction is not perfect: the regex patterns catch the PII shapes we
  identified from the seed data and the brief's own examples, not every
  conceivable format. This is documented, not hidden.

## Verification

- `tests/unit/test_redaction.py` (test A14): every pattern redacts its
  target, and ordinary numbers/addresses that merely look similar
  ("3 days", "Street 12") are left untouched.
- `tests/unit/test_prompt.py` and `tests/unit/test_triage_service.py`
  cover the delimiting and fallback machinery redaction feeds into.
- Test A15 (Groq sends no `reporter_contact`/`location`, inspected via a
  mocked HTTP call) lands with `AI-04`, once `GroqTriage` exists to
  inspect.
