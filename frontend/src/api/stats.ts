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
      // `error` is what narrows `data` to defined for TS (openapi-fetch's data/error
      // pair is a discriminated union keyed off `error`, not off response.ok). But a
      // failed response with an empty/non-JSON body (e.g. the dev proxy when the
      // backend is unreachable) parses to a falsy `error` even though the request
      // failed, so `response.ok` is checked too or that case would slip through and
      // leave `data` undefined inside an object that itself looks "loaded".
      // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
      if (error || !response.ok) throw toApiError(response, error);
      const header = response.headers.get("X-Cache");
      const cache: CacheState = header === "HIT" || header === "MISS" ? header : "UNKNOWN";
      return { stats: data, cache, fetchedAt: new Date() };
    },
    staleTime: 0, // always ask the server, so the X-Cache header is meaningful
    refetchInterval: opts.autoRefresh ? 10_000 : false,
  });
}
