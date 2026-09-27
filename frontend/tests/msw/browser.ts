import { setupWorker } from "msw/browser";

import { handlers } from "./handlers";

// Only ever started from main.tsx behind the DEV + VITE_USE_MSW=true guard, and
// only via a dynamic import, so this (and the msw/browser runtime) is tree-shaken
// out of the production bundle rather than merely unused.
export const worker = setupWorker(...handlers);
