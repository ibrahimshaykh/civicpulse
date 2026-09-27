import type { components } from "@/api/schema";

// Filter dropdowns need the list of values. That is schema, not a rule the
// frontend owns, so it must never silently drift from the server (plan §8.6).
export type Category = components["schemas"]["Category"];
export type Priority = components["schemas"]["Priority"];
export type Status = components["schemas"]["Status"];

// Exhaustiveness in both directions: `satisfies` catches an extra or misspelled
// value below; `Exact` fails to compile if the server has a value this list lacks.
type Exact<T, U extends readonly T[]> = [T] extends [U[number]] ? U : never;

export const CATEGORIES = [
  "water",
  "electricity",
  "sanitation",
  "roads",
  "streetlights",
  "other",
] as const satisfies readonly Category[];
export const PRIORITIES = ["high", "normal", "low"] as const satisfies readonly Priority[];
export const STATUSES = ["open", "in_progress", "resolved", "rejected"] as const satisfies readonly Status[];

// Type-only, exported so tsc's noUnusedLocals doesn't flag it: fails to compile
// (never a runtime check) if a list above is missing a value the server has.
export type CategoriesExact = Exact<Category, typeof CATEGORIES>;
export type PrioritiesExact = Exact<Priority, typeof PRIORITIES>;
export type StatusesExact = Exact<Status, typeof STATUSES>;

export const LABEL: Record<Category | Priority | Status, string> = {
  water: "Water",
  electricity: "Electricity",
  sanitation: "Sanitation",
  roads: "Roads",
  streetlights: "Streetlights",
  other: "Other",
  high: "High",
  normal: "Normal",
  low: "Low",
  open: "Open",
  in_progress: "In progress",
  resolved: "Resolved",
  rejected: "Rejected",
};
