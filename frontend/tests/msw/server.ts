import { setupServer } from "msw/node";

import { handlers } from "./handlers";

// Used by tests/setup.ts (listen/resetHandlers/close) and by any test that needs
// server.use(...) for a one-off override.
export const server = setupServer(...handlers);
