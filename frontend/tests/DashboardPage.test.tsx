import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { http, HttpResponse } from "msw";
import { MemoryRouter, useLocation } from "react-router-dom";
import { expect, test } from "vitest";

import { DashboardPage } from "@/pages/DashboardPage";
import { routerFuture } from "@/routes";

import { COMPLAINTS } from "./msw/fixtures";
import { server } from "./msw/server";

function LocationProbe() {
  const location = useLocation();
  return <p data-testid="location">{location.pathname + location.search}</p>;
}

function renderPage() {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: 0 } } });
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={["/dashboard"]} future={{ ...routerFuture, v7_startTransition: true }}>
        <DashboardPage />
        <LocationProbe />
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

test("7. an invalid transition shows the server's 409 message verbatim", async () => {
  const user = userEvent.setup();
  renderPage();
  // fixture #3 (Sanitation, Resolved) has no allowed_transitions, so its "Other
  // status" menu is the only way to trigger a 409 against the terminal row.
  const row = (await screen.findByText("Overflowing bins on Service Road drawing strays.")).closest("tr");
  if (!row) throw new Error("row not found");
  await user.selectOptions(within(row).getByLabelText(/Other status for complaint/), "open");

  expect(
    await screen.findByText("Invalid status transition: resolved → open. 'resolved' is terminal."),
  ).toBeInTheDocument();
  // the row itself is untouched: still shows the true, current status
  expect(within(row).getByText("Final: Resolved")).toBeInTheDocument();
});

test("8. changing a filter updates the URL and the query, and resets page to 1", async () => {
  const user = userEvent.setup();
  renderPage();
  await screen.findByText("Overflowing bins on Service Road drawing strays.");

  await user.selectOptions(screen.getByLabelText("Category"), "water");

  await waitFor(() => {
    expect(screen.getByTestId("location")).toHaveTextContent("/dashboard?category=water&page=1");
  });
  expect(await screen.findByText("Burst water main flooding Street 12 homes since dawn.")).toBeInTheDocument();
  expect(screen.queryByText("Overflowing bins on Service Road drawing strays.")).not.toBeInTheDocument();
});

test("9. Next requests page=2 and the range text reflects it", async () => {
  server.use(
    http.get("*/api/complaints", ({ request }) => {
      const page = Number(new URL(request.url).searchParams.get("page") ?? "1");
      const pageSize = 20;
      const total = 45;
      const [first] = COMPLAINTS;
      if (!first) throw new Error("fixtures missing");
      const items = page === 2 ? [{ ...first, id: "page-2-item" }] : COMPLAINTS;
      return HttpResponse.json({ items, total, page, page_size: pageSize, pages: 3 });
    }),
  );
  const user = userEvent.setup();
  renderPage();
  expect(await screen.findByText("Showing 1–20 of 45")).toBeInTheDocument();

  await user.click(screen.getByRole("button", { name: "Next" }));

  await waitFor(() => {
    expect(screen.getByTestId("location")).toHaveTextContent("/dashboard?page=2");
  });
  expect(await screen.findByText("Showing 21–40 of 45")).toBeInTheDocument();
});

test("10. primary actions render exactly the server's allowed_transitions", async () => {
  renderPage();
  const row = (await screen.findByText("Burst water main flooding Street 12 homes since dawn.")).closest("tr");
  if (!row) throw new Error("row not found");

  // COMPLAINTS[0].allowed_transitions is ["in_progress", "rejected"] — no client table.
  expect(within(row).getByRole("button", { name: "Move to In progress" })).toBeInTheDocument();
  expect(within(row).getByRole("button", { name: "Move to Rejected" })).toBeInTheDocument();
  expect(within(row).queryByRole("button", { name: "Move to Resolved" })).not.toBeInTheDocument();
  expect(within(row).queryByRole("button", { name: "Move to Open" })).not.toBeInTheDocument();

  // The remaining enum values are still reachable via "Other status…", proving
  // the component knows the full enum but only defaults to the server's allowlist.
  const other = within(row).getByLabelText(/Other status for complaint/);
  expect(within(other).getByRole("option", { name: "Resolved" })).toBeInTheDocument();
});
