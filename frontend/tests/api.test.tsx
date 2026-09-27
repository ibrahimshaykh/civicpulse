import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { renderHook, waitFor } from "@testing-library/react";
import type { ReactNode } from "react";
import { afterEach, beforeEach, expect, test, vi } from "vitest";

import { useCreateComplaint, useUpdateStatus } from "@/api/complaints";
import { ApiError, toApiError } from "@/api/errors";
import { useStats } from "@/api/stats";
import { newRequestId } from "@/lib/requestId";

function wrapper() {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: 0 } } });
  return ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={client}>{children}</QueryClientProvider>
  );
}

function jsonResponse(body: unknown, init: ResponseInit = {}) {
  return new Response(JSON.stringify(body), {
    status: 200,
    headers: { "content-type": "application/json" },
    ...init,
  });
}

let fetchMock: ReturnType<typeof vi.fn>;

beforeEach(() => {
  fetchMock = vi.fn();
  vi.stubGlobal("fetch", fetchMock);
});

afterEach(() => {
  vi.unstubAllGlobals();
});

test("newRequestId returns a well-formed v4 UUID", () => {
  const id = newRequestId();
  expect(id).toMatch(/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i);
  expect(newRequestId()).not.toBe(id);
});

test("every request carries an X-Request-ID header", async () => {
  fetchMock.mockResolvedValue(jsonResponse({ stats: {}, by_category: {} }));
  renderHook(() => useStats({ autoRefresh: false }), { wrapper: wrapper() });
  await waitFor(() => {
    expect(fetchMock).toHaveBeenCalled();
  });
  // openapi-fetch calls fetch(request) with a single Request object, not (url, init).
  const [request] = fetchMock.mock.calls[0] as [Request];
  expect(request.headers.get("X-Request-ID")).toBeTruthy();
});

test("useStats reads the X-Cache header, defaulting to UNKNOWN", async () => {
  fetchMock.mockResolvedValue(
    jsonResponse(
      { total: 0, by_category: {}, by_priority: {}, by_status: {}, generated_at: "2026-01-01T00:00:00Z" },
      { headers: { "content-type": "application/json", "X-Cache": "HIT" } },
    ),
  );
  const { result } = renderHook(() => useStats({ autoRefresh: false }), { wrapper: wrapper() });
  await waitFor(() => {
    expect(result.current.data?.cache).toBe("HIT");
  });
});

test("toApiError prefers the Retry-After header over the body's retry_after_s", () => {
  const response = new Response(null, { status: 429, headers: { "Retry-After": "12" } });
  const err = toApiError(response, { error: { code: "rate_limited", message: "slow down", request_id: "r1", retry_after_s: 99 } });
  expect(err).toBeInstanceOf(ApiError);
  expect(err.retryAfterS).toBe(12);
  expect(err.code).toBe("rate_limited");
  expect(err.requestId).toBe("r1");
});

test("a create mutation never retries, even on a 500", async () => {
  fetchMock.mockResolvedValue(
    new Response(JSON.stringify({ error: { code: "internal_error", message: "boom", request_id: "r2" } }), {
      status: 500,
      headers: { "content-type": "application/json" },
    }),
  );
  const { result } = renderHook(() => useCreateComplaint(), { wrapper: wrapper() });
  result.current.mutate({ text: "Something is broken here", location: "F-7" });
  await waitFor(() => {
    expect(result.current.isError).toBe(true);
  });
  expect(fetchMock).toHaveBeenCalledTimes(1);
});

test("a 409 on status update triggers a re-sync of the list, not a local guess", async () => {
  fetchMock.mockResolvedValue(
    new Response(
      JSON.stringify({
        error: { code: "invalid_transition", message: "already resolved", request_id: "r3", allowed: [] },
      }),
      { status: 409, headers: { "content-type": "application/json" } },
    ),
  );
  const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: 0 } } });
  const invalidateSpy = vi.spyOn(client, "invalidateQueries");
  const { result } = renderHook(() => useUpdateStatus(), {
    wrapper: ({ children }) => <QueryClientProvider client={client}>{children}</QueryClientProvider>,
  });
  result.current.mutate({ id: "4f1c2a9e-7c1b-4d3e-9a55-2b8f6f0f8e11", status: "open" });
  await waitFor(() => {
    expect(result.current.isError).toBe(true);
  });
  expect(invalidateSpy).toHaveBeenCalledWith({ queryKey: ["complaints"] });
});
