import { useUpdateStatus, type ComplaintOut } from "@/api/complaints";
import { ApiError } from "@/api/errors";
import { LABEL, STATUSES, type Status } from "@/lib/enums";

import { InlineAlert } from "./InlineAlert";

// Primary buttons come only from allowed_transitions, which the server computes.
// This component holds no table of which status can follow which (plan §8.9).
export function StatusActions({ complaint }: { complaint: ComplaintOut }) {
  const update = useUpdateStatus();
  const others = STATUSES.filter((s) => s !== complaint.status && !complaint.allowed_transitions.includes(s));

  return (
    <div className="flex flex-wrap items-center gap-2">
      {complaint.allowed_transitions.length === 0 ? (
        <span className="text-sm text-low">Final: {LABEL[complaint.status]}</span>
      ) : (
        complaint.allowed_transitions.map((s) => (
          <button
            key={s}
            type="button"
            className="btn-sm"
            disabled={update.isPending}
            onClick={() => {
              update.mutate({ id: complaint.id, status: s });
            }}
          >
            Move to {LABEL[s]}
          </button>
        ))
      )}

      {others.length > 0 && (
        <label className="text-sm">
          <span className="sr-only">Other status for complaint {complaint.id}</span>
          <select
            value=""
            disabled={update.isPending}
            onChange={(e) => {
              const next = e.target.value as Status | "";
              if (next) update.mutate({ id: complaint.id, status: next });
              e.target.value = "";
            }}
            className="rounded border border-rule bg-panel px-1.5 py-1"
          >
            <option value="">Other status…</option>
            {others.map((s) => (
              <option key={s} value={s}>
                {LABEL[s]}
              </option>
            ))}
          </select>
        </label>
      )}

      {update.error instanceof ApiError && update.error.status === 409 && (
        <InlineAlert>{update.error.message}</InlineAlert>
      )}
    </div>
  );
}
