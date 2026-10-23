import { defineConfig, mergeConfig } from "vitest/config";

import viteConfig from "./vite.config";

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      environment: "jsdom",
      // jsdom has no origin by default, so a relative URL (our client always uses
      // one — plan §8.1) fails to build a Request at all. Give it one.
      environmentOptions: { jsdom: { url: "http://localhost:5173" } },
      globals: true,
      setupFiles: ["./tests/setup.ts"],
      include: ["tests/**/*.test.tsx", "tests/**/*.test.ts"],
      coverage: { provider: "v8", include: ["src/**"], exclude: ["src/api/schema.d.ts"] },
    },
  }),
);
