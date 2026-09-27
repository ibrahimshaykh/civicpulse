import createClient, { type Middleware } from "openapi-fetch";

import { newRequestId } from "@/lib/requestId";

import type { paths } from "./schema";

// Relative baseUrl: same origin always (nginx proxy in prod, Vite proxy in dev).
// No import.meta.env.VITE_API_URL anywhere — plan §8.1. `MODE` is Vite's own
// built-in flag, not a custom VITE_ variable, and is only ever "test" under
// Vitest: outside tests baseUrl is "" exactly as the plan requires. It exists
// because Node's URL parser (unlike a browser) can't resolve a bare "/api/..."
// with no document to resolve it against.
const baseUrl = import.meta.env.MODE === "test" ? "http://localhost" : "";

// `fetch` is passed as an indirection rather than left to openapi-fetch's own
// `globalThis.fetch` default, which it reads once at client-creation time. Without
// this, a test that stubs `globalThis.fetch` after this module has loaded would
// never reach the client — the indirection re-reads the global on every call.
export const api = createClient<paths>({
  baseUrl,
  fetch: (...args: Parameters<typeof fetch>) => globalThis.fetch(...args),
});

const requestIdMiddleware: Middleware = {
  onRequest({ request }) {
    if (!request.headers.has("X-Request-ID")) {
      request.headers.set("X-Request-ID", newRequestId());
    }
    return request;
  },
};

api.use(requestIdMiddleware);
