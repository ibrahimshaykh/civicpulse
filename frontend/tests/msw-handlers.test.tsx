import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import type { ReactNode } from "react";
import { expect, test } from "vitest";

import { useComplaints, useCreateComplaint, useUpdateStatus } from "@/api/complaints";
import { ApiError } from "@/api/errors";
import { useProviders } from "@/api/meta";
import { useStats } from "@/api/stats";

function wrapper() {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: 0 } } });
  return ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={client}>{children}</QueryClientProvider>
  );
}

test("the fixture list is filterable by category and paginates", async () => {
  const { result } = renderHook(() => useComplaints({ category: "water", page: 1, pageSize: 20 }), {
    wrapper: wrapper(),
  });
  await waitFor(() => {
    expect(result.current.isSuccess).toBe(true);
  });
  expect(result.current.data?.items).toHaveLength(1);
  expect(result.current.data?.items[0]?.category).toBe("water");
});

test("creating a complaint adds it to the list and classifies it", async () => {
  const w = wrapper();
  const { result: create } = renderHook(() => useCreateComplaint(), { wrapper: w });
  create.current.mutate({ text: "A burst pipe is flooding the whole street", location: "Test St" });
  await waitFor(() => {
    expect(create.current.isSuccess).toBe(true);
  });
  expect(create.current.data?.category).toBe("water");

  const { result: list } = renderHook(() => useComplaints({ page: 1, pageSize: 20 }), { wrapper: w });
  await waitFor(() => {
    expect(list.current.data?.total).toBe(7); // 6 fixtures + the one just created
  });
});

test("the magic phrase triggers a 429 with Retry-After", async () => {
  const { result } = renderHook(() => useCreateComplaint(), { wrapper: wrapper() });
  result.current.mutate({ text: "RATE_LIMIT_ME please trigger the limit", location: "Test St" });
  await waitFor(() => {
    expect(result.current.isError).toBe(true);
  });
  expect(result.current.error).toBeInstanceOf(ApiError);
  expect((result.current.error as ApiError).retryAfterS).toBe(30);
});

test("an invalid status transition returns 409 with both statuses named", async () => {
  const { result } = renderHook(() => useUpdateStatus(), { wrapper: wrapper() });
  // fixture #3 (resolved) has no allowed transitions
  result.current.mutate({ id: "8c2d5e14-9b7a-4f0c-a1e3-6d8f2c4b1a09", status: "open" });
  await waitFor(() => {
    expect(result.current.isError).toBe(true);
  });
  expect(result.current.error).toBeInstanceOf(ApiError);
  expect((result.current.error as ApiError).code).toBe("invalid_transition");
});

test("stats and providers fixtures load with their headers", async () => {
  const { result: stats } = renderHook(() => useStats({ autoRefresh: false }), { wrapper: wrapper() });
  await waitFor(() => {
    expect(stats.current.data?.cache).toBe("HIT");
  });
  expect(stats.current.data?.stats.total).toBeGreaterThan(0);

  const { result: providers } = renderHook(() => useProviders(), { wrapper: wrapper() });
  await waitFor(() => {
    expect(providers.current.data?.active_provider).toBe("llm:groq");
  });
});
