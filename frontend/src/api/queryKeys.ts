import type { Category, Priority, Status } from "@/lib/enums";

export type ComplaintFilters = {
  category?: Category;
  priority?: Priority;
  status?: Status;
  page: number;
  pageSize: number;
};

export const qk = {
  complaints: (f: ComplaintFilters) => ["complaints", f] as const,
  complaint: (id: string) => ["complaint", id] as const,
  stats: ["stats"] as const,
  providers: ["providers"] as const,
};
