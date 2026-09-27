import { QueryErrorResetBoundary } from "@tanstack/react-query";
import type { ReactNode } from "react";

import { ErrorBoundary } from "./ErrorBoundary";

// One boundary per route, so a Stats crash doesn't blank the Dashboard.
// QueryErrorResetBoundary makes "Try again" also retry the failed queries.
export function RouteBoundary({ children }: { children: ReactNode }) {
  return (
    <QueryErrorResetBoundary>
      {({ reset }) => (
        <ErrorBoundary
          fallback={(_err, resetBoundary) => (
            <div role="alert" className="max-w-form rounded border border-rule bg-panel p-6">
              <h2 className="text-lg font-semibold">This page stopped working</h2>
              <p className="mt-2">The rest of the app still works. Try again, or pick another page.</p>
              <button
                type="button"
                className="btn mt-4"
                onClick={() => {
                  reset();
                  resetBoundary();
                }}
              >
                Try again
              </button>
            </div>
          )}
        >
          {children}
        </ErrorBoundary>
      )}
    </QueryErrorResetBoundary>
  );
}
