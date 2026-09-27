import type { components } from "@/api/schema";

type ComplaintOut = components["schemas"]["ComplaintOut"];
type StatsOut = components["schemas"]["StatsOut"];
type ProvidersOut = components["schemas"]["ProvidersOut"];

// Computed relative to "now" (whenever the app happens to run) rather than fixed
// calendar dates, so the Dashboard's relative-time column always reads sensibly
// instead of showing complaints "from the future".
const HOUR_MS = 3_600_000;
const hoursAgo = (h: number): string => new Date(Date.now() - h * HOUR_MS).toISOString();

// `satisfies` means a contract change (a renamed or removed field) breaks these
// fixtures at compile time, not silently at runtime (plan §8.13).
export const COMPLAINTS: ComplaintOut[] = [
  {
    id: "4f1c2a9e-7c1b-4d3e-9a55-2b8f6f0f8e11",
    text: "Burst water main flooding Street 12 since fajr, water entering ground floors",
    location: "Street 12, G-9/2, Islamabad",
    reporter_contact: "0300-1234567",
    category: "water",
    priority: "high",
    status: "open",
    ai_summary: "Burst water main flooding Street 12 homes since dawn.",
    triaged_by: "llm:groq",
    triage_latency_ms: 412,
    triage_confidence: 0.93,
    created_at: hoursAgo(0.5),
    updated_at: hoursAgo(0.5),
    allowed_transitions: ["in_progress", "rejected"],
  } satisfies ComplaintOut,
  {
    id: "0b7e9d4c-3a2f-4e61-8c5d-9f1a2b3c4d5e",
    text: "Streetlight on F-7 Markaz corner has been out for two weeks, unsafe at night",
    location: "F-7 Markaz, Islamabad",
    reporter_contact: null,
    category: "streetlights",
    priority: "normal",
    status: "in_progress",
    ai_summary: "Streetlight outage at F-7 Markaz corner, two weeks.",
    triaged_by: "rules:fallback",
    triage_latency_ms: 10012,
    triage_confidence: null,
    created_at: hoursAgo(9),
    updated_at: hoursAgo(1),
    allowed_transitions: ["resolved", "rejected"],
  } satisfies ComplaintOut,
  {
    id: "8c2d5e14-9b7a-4f0c-a1e3-6d8f2c4b1a09",
    text: "Overflowing garbage bins on Service Road, attracting stray dogs and smell",
    location: "Service Road, I-10/2, Islamabad",
    reporter_contact: "0333-9876543",
    category: "sanitation",
    priority: "normal",
    status: "resolved",
    ai_summary: "Overflowing bins on Service Road drawing strays.",
    triaged_by: "llm:groq",
    triage_latency_ms: 388,
    triage_confidence: 0.81,
    created_at: hoursAgo(30),
    updated_at: hoursAgo(6),
    allowed_transitions: [],
  } satisfies ComplaintOut,
  {
    id: "1a3f5c7e-2b4d-4e6f-8091-a2b3c4d5e6f7",
    text: "Pothole widening dangerously on the roundabout near sector market",
    location: "Sector Market Roundabout, G-11",
    reporter_contact: "0301-1122334",
    category: "roads",
    priority: "high",
    status: "open",
    ai_summary: "Widening pothole at the sector market roundabout.",
    triaged_by: "llm:groq",
    triage_latency_ms: 455,
    triage_confidence: 0.88,
    created_at: hoursAgo(2),
    updated_at: hoursAgo(2),
    allowed_transitions: ["in_progress", "rejected"],
  } satisfies ComplaintOut,
  {
    id: "9d1e3f5a-4b6c-4d8e-a0b1-c2d3e4f5a6b7",
    text: "Transformer sparking intermittently near the park entrance since last night",
    location: "Park Entrance, F-10/3",
    reporter_contact: "0345-5566778",
    category: "electricity",
    priority: "high",
    status: "rejected",
    ai_summary: "Intermittent sparking transformer near park entrance.",
    triaged_by: "rules",
    triage_latency_ms: 4,
    triage_confidence: null,
    created_at: hoursAgo(56),
    updated_at: hoursAgo(47),
    allowed_transitions: [],
  } satisfies ComplaintOut,
  {
    id: "5e7f9a1b-6c8d-4e0f-b2a3-d4e5f6a7b8c9",
    text: "Loose manhole cover on the footpath, tripping hazard for pedestrians",
    location: "Footpath near F-8 Markaz",
    reporter_contact: null,
    category: "other",
    priority: "low",
    status: "open",
    ai_summary: "Loose manhole cover, tripping hazard on footpath.",
    triaged_by: "rules",
    triage_latency_ms: 3,
    triage_confidence: null,
    created_at: hoursAgo(90),
    updated_at: hoursAgo(90),
    allowed_transitions: ["in_progress", "rejected"],
  } satisfies ComplaintOut,
];

export const STATS: StatsOut = {
  total: COMPLAINTS.length,
  by_category: { water: 1, electricity: 1, sanitation: 1, roads: 1, streetlights: 1, other: 1 },
  by_priority: { high: 3, normal: 2, low: 1 },
  by_status: { open: 3, in_progress: 1, resolved: 1, rejected: 1 },
  generated_at: hoursAgo(0),
} satisfies StatsOut;

export const PROVIDERS: ProvidersOut = {
  active_provider: "llm:groq",
  fallback_provider: "rules",
  model: "llama-3.1-8b-instant",
  cache_hit_rate: 0.25,
  recent: [
    {
      complaint_id: "4f1c2a9e-7c1b-4d3e-9a55-2b8f6f0f8e11", // COMPLAINTS[0].id
      provider: "llm:groq",
      latency_ms: 412,
      fallback: false,
      cache_hit: false,
      error_class: null,
      at: hoursAgo(0.5),
    },
    {
      complaint_id: "0b7e9d4c-3a2f-4e61-8c5d-9f1a2b3c4d5e", // COMPLAINTS[1].id
      provider: "rules:fallback",
      latency_ms: 10012,
      fallback: true,
      cache_hit: false,
      error_class: "APITimeoutError",
      at: hoursAgo(9),
    },
  ],
} satisfies ProvidersOut;
