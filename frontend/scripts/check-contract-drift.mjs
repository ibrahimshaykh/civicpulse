#!/usr/bin/env node
// CI job `contract` (plan §7.6): regenerate the typed client from the committed
// backend/openapi.json and fail if it doesn't match what's checked in. Catches a
// backend PR that changed a schema without running `npm run gen:api`.
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const schemaPath = join(root, "src/api/schema.d.ts");

const before = readFileSync(schemaPath, "utf8");
// npm resolves to npm.cmd on Windows, which execFileSync can't find without a shell.
execFileSync("npm", ["run", "gen:api"], { cwd: root, stdio: "inherit", shell: true });
const after = readFileSync(schemaPath, "utf8");

if (before !== after) {
  console.error(
    "\nsrc/api/schema.d.ts is stale relative to backend/openapi.json.\n" +
      "Run `npm run gen:api` in frontend/ and commit the result.\n",
  );
  process.exit(1);
}

console.log("src/api/schema.d.ts matches backend/openapi.json.");
