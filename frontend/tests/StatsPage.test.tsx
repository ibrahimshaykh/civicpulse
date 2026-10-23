import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { http, HttpResponse } from "msw";
import { expect, test } from "vitest";

import { StatsPage } from "@/pages/StatsPage";

import { STATS } from "./msw/fixtures";
import { server } from "./msw/server";

function renderPage() {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={client}>
      <StatsPage />
    </QueryClientProvider>,
  );
}

test("11a. X-Cache: HIT renders the HIT indicator", async () => {
  server.use(http.get("*/api/stats", () => HttpResponse.json(STATS, { headers: { "X-Cache": "HIT" } })));
  renderPage();
  expect(await screen.findByText("Served from cache (HIT)")).toBeInTheDocument();
});

test("11b. X-Cache: MISS renders the MISS indicator", async () => {
  server.use(http.get("*/api/stats", () => HttpResponse.json(STATS, { headers: { "X-Cache": "MISS" } })));
  renderPage();
  expect(await screen.findByText("Computed fresh (MISS)")).toBeInTheDocument();
});

test("totals and provider observability render from the fixtures", async () => {
  renderPage();
  expect(await screen.findByText(`${String(STATS.total)} total complaints`)).toBeInTheDocument();
  expect(screen.getByText("By category")).toBeInTheDocument();
  expect(screen.getByText("By priority")).toBeInTheDocument();
  expect(screen.getByText("By status")).toBeInTheDocument();
  // "AI · Groq" appears both as the active provider and in the outcomes table.
  expect((await screen.findAllByText("AI · Groq")).length).toBeGreaterThan(0);
  expect(await screen.findByText("Keyword rules (AI unavailable)")).toBeInTheDocument();
});
