import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { createMemoryRouter, RouterProvider, type RouteObject } from "react-router-dom";

import { Layout } from "@/components/Layout";
import { RouteBoundary } from "@/components/RouteBoundary";
import { routerFuture, routes } from "@/routes";

function renderAt(path: string, tree: RouteObject[] = routes) {
  const router = createMemoryRouter(tree, { initialEntries: [path], future: routerFuture });
  render(
    <QueryClientProvider client={new QueryClient()}>
      <RouterProvider router={router} future={{ v7_startTransition: true }} />
    </QueryClientProvider>,
  );
  return router;
}

test("root redirects to the submit page", async () => {
  const router = renderAt("/");
  expect(await screen.findByRole("heading", { level: 1, name: "Report a problem" })).toBeInTheDocument();
  expect(router.state.location.pathname).toBe("/submit");
  await waitFor(() => {
    expect(document.title).toBe("Submit complaint · CivicPulse");
  });
});

test("nav rail marks the current page and navigates", async () => {
  renderAt("/submit");
  const nav = screen.getByRole("navigation", { name: "Main" });
  expect(screen.getByRole("link", { name: "Submit" })).toHaveAttribute("aria-current", "page");

  await userEvent.click(screen.getByRole("link", { name: "Stats" }));
  expect(await screen.findByRole("heading", { level: 1, name: "Stats" })).toBeInTheDocument();
  expect(screen.getByRole("link", { name: "Stats" })).toHaveAttribute("aria-current", "page");
  expect(screen.getByRole("link", { name: "Submit" })).not.toHaveAttribute("aria-current");
  expect(nav).toBeInTheDocument();
});

test("skip link is the first focusable element", async () => {
  renderAt("/dashboard");
  await userEvent.tab();
  expect(screen.getByRole("link", { name: "Skip to content" })).toHaveFocus();
});

test("unknown paths show the not-found page", () => {
  renderAt("/nope");
  expect(screen.getByRole("heading", { level: 1, name: "Page not found" })).toBeInTheDocument();
});

test("a crashing route is isolated: the nav stays and Try again recovers", async () => {
  let shouldThrow = true;
  function Flaky() {
    if (shouldThrow) throw new Error("boom");
    return <h1>Recovered</h1>;
  }
  const errorSpy = vi.spyOn(console, "error").mockImplementation(() => undefined);

  renderAt("/flaky", [
    { element: <Layout />, children: [{ path: "flaky", element: <RouteBoundary><Flaky /></RouteBoundary> }] },
  ]);

  expect(screen.getByRole("alert")).toHaveTextContent("This page stopped working");
  expect(screen.getByRole("navigation", { name: "Main" })).toBeInTheDocument();

  shouldThrow = false;
  await userEvent.click(screen.getByRole("button", { name: "Try again" }));
  expect(screen.getByRole("heading", { name: "Recovered" })).toBeInTheDocument();
  errorSpy.mockRestore();
});
