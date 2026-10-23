import "@fontsource-variable/public-sans";
import "./styles/index.css";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider } from "react-router-dom";

import { ApiError } from "./api/errors";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { router } from "./router";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (count, err) => err instanceof ApiError && err.status >= 500 && count < 2,
      refetchOnWindowFocus: false,
      staleTime: 5_000,
    },
    mutations: { retry: 0 },
  },
});

const root = document.getElementById("root");
if (!root) throw new Error("#root element missing from index.html");

// Dynamic import so msw/browser (and its handlers) is dead code in a production
// build: DEV is a compile-time constant, so the whole branch is eliminated
// (plan §8.13). Run with VITE_USE_MSW=true npm run dev before the backend exists.
async function enableMocking(): Promise<void> {
  if (!(import.meta.env.DEV && import.meta.env.VITE_USE_MSW === "true")) return;
  const { worker } = await import("../tests/msw/browser");
  await worker.start({ onUnhandledRequest: "bypass" });
}

void enableMocking().then(() => {
  createRoot(root).render(
    <StrictMode>
      <ErrorBoundary>
        <QueryClientProvider client={queryClient}>
          <RouterProvider router={router} future={{ v7_startTransition: true }} />
        </QueryClientProvider>
      </ErrorBoundary>
    </StrictMode>,
  );
});
