import { delay, http, HttpResponse } from "msw";

import type { Category, Priority, Status } from "@/lib/enums";

import type { components } from "@/api/schema";
import { COMPLAINTS, PROVIDERS, STATS } from "./fixtures";

type ComplaintCreate = components["schemas"]["ComplaintCreate"];
type ComplaintOut = components["schemas"]["ComplaintOut"];
type ErrorBody = components["schemas"]["ErrorBody"];

// Mutable in-memory copy: creating or updating a complaint through these handlers
// changes this array, not the fixtures module, so tests see the effect of their
// own actions without polluting each other. Call resetComplaints() between tests.
let complaints: ComplaintOut[] = COMPLAINTS.map((c) => ({ ...c }));

export function resetComplaints(): void {
  complaints = COMPLAINTS.map((c) => ({ ...c }));
}

function rateLimitedBody(retryAfterS: number): ErrorBody {
  return {
    error: {
      code: "rate_limited",
      message: `Too many complaints from this address. Try again in ${String(retryAfterS)} seconds.`,
      request_id: "msw-77ee88ff",
      retry_after_s: retryAfterS,
    },
  };
}

function invalidTransitionBody(from: Status, to: Status): ErrorBody {
  return {
    error: {
      code: "invalid_transition",
      message: `Invalid status transition: ${from} → ${to}.`,
      request_id: "msw-9a8b7c6d",
      from_status: from,
      to_status: to,
      allowed: [],
    },
  };
}

function notFoundBody(id: string): ErrorBody {
  return {
    error: { code: "not_found", message: `No complaint with id ${id}.`, request_id: "msw-not-found" },
  };
}

// Standing in for the real triage service: enough of a heuristic to give the
// Submit form realistic-looking results while the backend's logic doesn't exist
// yet. Test scaffolding only — the app never re-implements this categorization.
function classify(text: string): { category: Category; priority: Priority } {
  const t = text.toLowerCase();
  if (/water|pipe|flood|leak/.test(t)) return { category: "water", priority: "high" };
  if (/electric|wire|transformer|spark/.test(t)) return { category: "electricity", priority: "high" };
  if (/garbage|trash|sewage|drain/.test(t)) return { category: "sanitation", priority: "normal" };
  if (/pothole|road|street(?!light)/.test(t)) return { category: "roads", priority: "normal" };
  if (/streetlight|lamp/.test(t)) return { category: "streetlights", priority: "normal" };
  return { category: "other", priority: "low" };
}

function makeComplaint(body: ComplaintCreate): ComplaintOut {
  const { category, priority } = classify(body.text);
  const now = new Date().toISOString();
  return {
    id: crypto.randomUUID(),
    text: body.text,
    location: body.location,
    reporter_contact: body.reporter_contact ?? null,
    category,
    priority,
    status: "open",
    ai_summary: body.text.length > 140 ? `${body.text.slice(0, 137)}...` : body.text,
    triaged_by: "llm:groq",
    triage_latency_ms: 420,
    triage_confidence: 0.9,
    created_at: now,
    updated_at: now,
    allowed_transitions: ["in_progress", "rejected"],
  };
}

export const handlers = [
  http.post("*/api/complaints", async ({ request }) => {
    const body = (await request.json()) as ComplaintCreate;
    // A magic phrase, not a real rate limiter, so FE-06's 429 test can trigger it on demand.
    if (body.text.includes("RATE_LIMIT_ME")) {
      return HttpResponse.json(rateLimitedBody(30), { status: 429, headers: { "Retry-After": "30" } });
    }
    await delay(300); // honest loading: give the Submit page something to show
    const created = makeComplaint(body);
    complaints = [created, ...complaints];
    return HttpResponse.json(created, {
      status: 201,
      headers: { Location: `/api/complaints/${created.id}` },
    });
  }),

  http.get("*/api/complaints/:id", ({ params }) => {
    const found = complaints.find((c) => c.id === params.id);
    if (!found) return HttpResponse.json(notFoundBody(String(params.id)), { status: 404 });
    return HttpResponse.json(found);
  }),

  http.get("*/api/complaints", ({ request }) => {
    const url = new URL(request.url);
    const category = url.searchParams.get("category");
    const priority = url.searchParams.get("priority");
    const status = url.searchParams.get("status");
    const page = Number(url.searchParams.get("page") ?? "1");
    const pageSize = Number(url.searchParams.get("page_size") ?? "20");

    const filtered = complaints.filter(
      (c) =>
        (!category || c.category === category) &&
        (!priority || c.priority === priority) &&
        (!status || c.status === status),
    );
    const start = (page - 1) * pageSize;
    return HttpResponse.json({
      items: filtered.slice(start, start + pageSize),
      total: filtered.length,
      page,
      page_size: pageSize,
      pages: Math.max(1, Math.ceil(filtered.length / pageSize)),
    });
  }),

  http.patch("*/api/complaints/:id/status", async ({ params, request }) => {
    const { status: to } = (await request.json()) as { status: Status };
    const found = complaints.find((c) => c.id === params.id);
    if (!found) return HttpResponse.json(notFoundBody(String(params.id)), { status: 404 });
    if (!found.allowed_transitions.includes(to)) {
      return HttpResponse.json(invalidTransitionBody(found.status, to), { status: 409 });
    }
    found.status = to;
    found.updated_at = new Date().toISOString();
    found.allowed_transitions = to === "open" || to === "in_progress" ? ["resolved", "rejected"] : [];
    return HttpResponse.json(found);
  }),

  http.get("*/api/stats", () => HttpResponse.json(STATS, { headers: { "X-Cache": "HIT" } })),

  http.get("*/api/meta/providers", () => HttpResponse.json(PROVIDERS)),
];
