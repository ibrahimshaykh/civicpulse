/// <reference types="vite/client" />

interface ImportMetaEnv {
  // Dev-only mock toggle (plan §8.13), never read outside main.tsx's dynamic
  // import guard. Not an API URL — plan §8.1's ban is on VITE_API_* only.
  readonly VITE_USE_MSW?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
