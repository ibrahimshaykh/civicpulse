import { useQuery } from "@tanstack/react-query";

import { api } from "./client";
import { toApiError } from "./errors";
import { qk } from "./queryKeys";

export type CacheState = "HIT" | "MISS" | "UNKNOWN";

export function useStats(opts: { autoRefresh: boolean }) {
  return useQuery({
    queryKey: qk.stats,
    queryFn: async () => {
      const { data, error, response } = await api.GET("/api/stats");
      // The OpenAPI schema only documents a 200 for this route (CA-01 adds real error
      // responses), so TS narrows `error` to always-undefined. The check stays: the
      // server can still fail at runtime in ways the schema doesn't yet describe.
      // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
      if (error) throw toApiError(response, error);
      const header = response.headers.get("X-Cache");
      const cache: CacheState = header === "HIT" || header === "MISS" ? header : "UNKNOWN";
      return { stats: data, cache, fetchedAt: new Date() };
    },
    staleTime: 0, // always ask the server, so the X-Cache header is meaningful
    refetchInterval: opts.autoRefresh ? 10_000 : false,
  });
}
