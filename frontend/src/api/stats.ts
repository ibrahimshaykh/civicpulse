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
      // responses), so TS narrows `error` to always-undefined. The check stays and
      // goes by `response.ok`, not the truthiness of the parsed error body: a failed
      // response with an empty/non-JSON body (e.g. the dev proxy when the backend is
      // unreachable) parses to a falsy `error`, which would otherwise slip through
      // and leave `data` undefined inside an object that itself looks "loaded".
      // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
      if (!response.ok) throw toApiError(response, error);
      const header = response.headers.get("X-Cache");
      const cache: CacheState = header === "HIT" || header === "MISS" ? header : "UNKNOWN";
      return { stats: data, cache, fetchedAt: new Date() };
    },
    staleTime: 0, // always ask the server, so the X-Cache header is meaningful
    refetchInterval: opts.autoRefresh ? 10_000 : false,
  });
}
