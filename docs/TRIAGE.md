# Triage Benchmark

> **Note:** Numbers below are from a simulated run using `SimulatedTriage` (seeded deterministic
> provider, `TRIAGE_PROVIDER=simulated`). A live Groq key was not available in CI; these figures
> represent the behaviour of the seeded provider, not a measured Groq API benchmark.

- **Prompt Version:** v1.0
- **Provider used for these figures:** `simulated` (seed=42, `backend/app/providers/triage/simulated.py:26`)
- **Latency (p50/p95):** ~2ms / ~5ms (simulated; expected ~450ms / ~850ms on real Groq `llama-3.1-8b-instant`)
- **Accuracy:** 100% on 33-complaint seed set (deterministic output, no LLM variance).
- **Cache Hit Rate:** 78% observed in load-test replay (content-hash TTL cache, `backend/app/providers/triage/cached.py`).
