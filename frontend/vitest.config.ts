import { defineConfig, mergeConfig } from "vitest/config";

import viteConfig from "./vite.config";

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      environment: "jsdom",
      globals: true,
      setupFiles: ["./tests/setup.ts"],
      include: ["tests/**/*.test.tsx", "tests/**/*.test.ts"],
      coverage: { provider: "v8", include: ["src/**"], exclude: ["src/api/schema.d.ts"] },
    },
  }),
);
