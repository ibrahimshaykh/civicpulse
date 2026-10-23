import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { expect, test } from "vitest";

import { ComplaintDetailPage } from "@/pages/ComplaintDetailPage";
import { routerFuture } from "@/routes";

import { COMPLAINTS } from "./msw/fixtures";

function renderAt(path: string) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: 0 } } });
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[path]} future={{ ...routerFuture, v7_startTransition: true }}>
        <Routes>
          <Route path="/complaints/:id" element={<ComplaintDetailPage />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

test("12. a known id renders the full record, all fields, and StatusActions", async () => {
  const c = COMPLAINTS[0];
  if (!c) throw new Error("fixtures missing");
  renderAt(`/complaints/${c.id}`);

  expect(await screen.findByText(c.text)).toBeInTheDocument();
  expect(screen.getByText(c.location)).toBeInTheDocument();
  expect(screen.getByText(c.reporter_contact ?? "—")).toBeInTheDocument();
  expect(screen.getByText("Water")).toBeInTheDocument(); // CategoryLabel
  expect(screen.getByText("High")).toBeInTheDocument(); // PriorityBadge
  expect(screen.getByText("Open")).toBeInTheDocument(); // status
  expect(screen.getByText("AI · Groq")).toBeInTheDocument(); // ProviderTag
  // StatusActions: fixture #1's allowed_transitions is ["in_progress", "rejected"]
  expect(screen.getByRole("button", { name: "Move to In progress" })).toBeInTheDocument();
});

test("13. an unknown id renders the server's 404 message verbatim, with a link back", async () => {
  const unknownId = "00000000-0000-0000-0000-000000000000";
  renderAt(`/complaints/${unknownId}`);

  expect(await screen.findByText(`No complaint with id ${unknownId}.`)).toBeInTheDocument();
  expect(screen.getByRole("link", { name: "Back to dashboard" })).toHaveAttribute("href", "/dashboard");
});
