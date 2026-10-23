import path from "node:path";

import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// Dev-only proxy target. This is host → published container port, not
// service-to-service traffic, so it is not the "localhost" deduction.
const devApiTarget = process.env.DEV_API_TARGET ?? "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [react()],
  resolve: { alias: { "@": path.resolve(import.meta.dirname, "src") } },
  server: { proxy: { "/api": { target: devApiTarget, changeOrigin: false } } },
  build: { sourcemap: false, target: "es2022", assetsInlineLimit: 0 },
});
