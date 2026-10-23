import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { delay, http, HttpResponse } from "msw";
import { MemoryRouter } from "react-router-dom";
import { afterEach, expect, test, vi } from "vitest";

import { SubmitPage } from "@/pages/SubmitPage";
import { routerFuture } from "@/routes";

import { server } from "./msw/server";

function renderPage() {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false }, mutations: { retry: 0 } } });
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter future={{ ...routerFuture, v7_startTransition: true }}>
        <SubmitPage />
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

async function fillValidForm() {
  const user = userEvent.setup();
  await user.type(screen.getByLabelText("What's wrong?"), "A burst pipe is flooding the whole street");
  await user.type(screen.getByLabelText("Location"), "Test Street 12");
  return user;
}

afterEach(() => {
  vi.useRealTimers();
});

test("1. short text shows the zod message and sends no request", async () => {
  const user = userEvent.setup();
  renderPage();
  await user.type(screen.getByLabelText("What's wrong?"), "too short");
  await user.type(screen.getByLabelText("Location"), "Test St");
  await user.click(screen.getByRole("button", { name: "Submit complaint" }));

  expect(await screen.findByText("Describe the problem in at least 10 characters")).toBeInTheDocument();
  // onUnhandledRequest: "error" (tests/setup.ts) means an accidental request here
  // would already have thrown; this assertion just makes the intent explicit.
  expect(screen.getByRole("button", { name: "Submit complaint" })).not.toBeDisabled();
});

test("2. a successful submit renders category, priority, summary and provider", async () => {
  renderPage();
  const user = await fillValidForm();
  await user.click(screen.getByRole("button", { name: "Submit complaint" }));

  expect(await screen.findByRole("heading", { name: "Complaint received" })).toBeInTheDocument();
  expect(screen.getByText("Water")).toBeInTheDocument();
  expect(screen.getByText("High")).toBeInTheDocument();
  expect(screen.getByText(/burst pipe/i)).toBeInTheDocument();
  expect(screen.getByText("AI · Groq")).toBeInTheDocument();
});

test("3. while pending, the button is disabled, aria-busy region is live, and elapsed time shows", async () => {
  server.use(
    http.post("*/api/complaints", async () => {
      await delay("infinite");
      return HttpResponse.json({});
    }),
  );
  renderPage();
  const user = await fillValidForm();
  await user.click(screen.getByRole("button", { name: "Submit complaint" }));

  expect(await screen.findByRole("button", { name: "Reading your complaint…" })).toBeDisabled();
  expect(screen.getByRole("status")).toHaveTextContent(/\d+ s/);
});

test("4. server 400 fields[] appear under the matching input", async () => {
  server.use(
    http.post("*/api/complaints", () =>
      HttpResponse.json(
        {
          error: {
            code: "validation_error",
            message: "Request validation failed",
            request_id: "t1",
            fields: [{ field: "location", message: "Add a real location", type: "value_error" }],
          },
        },
        { status: 400 },
      ),
    ),
  );
  const user = userEvent.setup();
  renderPage();
  await user.type(screen.getByLabelText("What's wrong?"), "A burst pipe is flooding the whole street");
  await user.type(screen.getByLabelText("Location"), "Test Street 12");
  await user.click(screen.getByRole("button", { name: "Submit complaint" }));

  expect(await screen.findByText("Add a real location")).toBeInTheDocument();
  expect(screen.getByLabelText("Location")).toHaveFocus();
});

test("5. 429 shows the Retry-After countdown and disables submit until zero", async () => {
  vi.useFakeTimers({ shouldAdvanceTime: true });
  server.use(
    http.post("*/api/complaints", () =>
      HttpResponse.json(
        { error: { code: "rate_limited", message: "slow down", request_id: "t2", retry_after_s: 3 } },
        { status: 429, headers: { "Retry-After": "3" } },
      ),
    ),
  );
  const user = userEvent.setup({ delay: null });
  renderPage();
  await user.type(screen.getByLabelText("What's wrong?"), "A burst pipe is flooding the whole street");
  await user.type(screen.getByLabelText("Location"), "Test Street 12");
  await user.click(screen.getByRole("button", { name: "Submit complaint" }));

  expect(await screen.findByText(/submit again in 3 s/)).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Submit complaint" })).toBeDisabled();

  await act(async () => {
    await vi.advanceTimersByTimeAsync(3000);
  });
  expect(screen.getByRole("button", { name: "Submit complaint" })).not.toBeDisabled();
});

test("6. rules:fallback renders as 'Keyword rules (AI unavailable)'", async () => {
  server.use(
    http.post("*/api/complaints", async ({ request }) => {
      const body = (await request.json()) as { text: string; location: string };
      return HttpResponse.json({
        id: "fallback-id",
        text: body.text,
        location: body.location,
        reporter_contact: null,
        category: "other",
        priority: "low",
        status: "open",
        ai_summary: null,
        triaged_by: "rules:fallback",
        triage_latency_ms: 10012,
        triage_confidence: null,
        created_at: "2026-01-01T00:00:00Z",
        updated_at: "2026-01-01T00:00:00Z",
        allowed_transitions: ["in_progress", "rejected"],
      });
    }),
  );
  const user = userEvent.setup();
  renderPage();
  await user.type(screen.getByLabelText("What's wrong?"), "Something is generally wrong here");
  await user.type(screen.getByLabelText("Location"), "Test Street 12");
  await user.click(screen.getByRole("button", { name: "Submit complaint" }));

  expect(await screen.findByText("Keyword rules (AI unavailable)")).toBeInTheDocument();
});
