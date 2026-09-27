import "@testing-library/jest-dom/vitest";

import { afterAll, afterEach, beforeAll } from "vitest";

import { resetComplaints } from "./msw/handlers";
import { server } from "./msw/server";

// onUnhandledRequest: "error" so an untested fetch fails loudly instead of hanging
// (plan §8.14, test 1: "no request is sent" is asserted via this, not a spy).
beforeAll(() => {
  server.listen({ onUnhandledRequest: "error" });
});

afterEach(() => {
  server.resetHandlers();
  resetComplaints();
});

afterAll(() => {
  server.close();
});
