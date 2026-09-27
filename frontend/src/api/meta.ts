import { useQuery } from "@tanstack/react-query";

import { api } from "./client";
import { toApiError } from "./errors";
import { qk } from "./queryKeys";

export function useProviders() {
  return useQuery({
    queryKey: qk.providers,
    queryFn: async () => {
      const { data, error, response } = await api.GET("/api/meta/providers");
      // See stats.ts: this route's schema only documents a 200 today.
      // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
      if (error) throw toApiError(response, error);
      return data;
    },
    refetchInterval: 10_000,
  });
}
