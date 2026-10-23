import type { ReactNode } from "react";

// Server messages are rendered verbatim — the frontend never rewrites what the
// backend said (plan §8.1's "client validation mirrors, it does not replace").
export function InlineAlert({ children }: { children: ReactNode }) {
  return (
    <div role="alert" className="rounded border border-high bg-high/5 px-4 py-3 text-sm text-high">
      {children}
    </div>
  );
}
