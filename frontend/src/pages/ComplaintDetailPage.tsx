import { Link, useParams } from "react-router-dom";

import { useComplaint } from "@/api/complaints";
import { ApiError } from "@/api/errors";
import { CategoryLabel } from "@/components/CategoryLabel";
import { InlineAlert } from "@/components/InlineAlert";
import { PriorityBadge } from "@/components/PriorityBadge";
import { ProviderTag } from "@/components/ProviderTag";
import { StatusActions } from "@/components/StatusActions";
import { LABEL } from "@/lib/enums";
import { msLabel, relativeTime } from "@/lib/format";
import { useDocumentTitle } from "@/lib/useDocumentTitle";

// Full record view (plan §8.11): all fields, StatusActions, timestamps.
// A 404 (unknown id) and a 400 (malformed UUID) both land here as an
// ApiError and are rendered the same way -- the server's own message,
// verbatim, plus a link back to the dashboard (plan §8.1's rule that the
// frontend never rewrites what the backend said).
export function ComplaintDetailPage() {
  const { id = "" } = useParams();
  useDocumentTitle("Complaint");
  const query = useComplaint(id);

  if (query.isPending) {
    return (
      <section className="max-w-board">
        <p className="text-low">Loading…</p>
      </section>
    );
  }

  if (query.isError) {
    const message = query.error instanceof ApiError ? query.error.message : "Could not load this complaint.";
    return (
      <section className="max-w-board">
        <InlineAlert>{message}</InlineAlert>
        <Link to="/dashboard" className="btn mt-4 inline-block">
          Back to dashboard
        </Link>
      </section>
    );
  }

  const c = query.data;

  return (
    <section className="max-w-board">
      <div className="flex flex-wrap items-center gap-2">
        <h1 className="text-xl font-semibold">Complaint</h1>
        <PriorityBadge priority={c.priority} />
        <ProviderTag triagedBy={c.triaged_by} />
      </div>
      <p className="tabular mt-1 break-all text-sm text-low">{c.id}</p>

      <dl className="mt-6 grid grid-cols-1 gap-x-8 gap-y-4 sm:grid-cols-2">
        <div>
          <dt className="text-sm text-low">Category</dt>
          <dd className="mt-1">
            <CategoryLabel category={c.category} />
          </dd>
        </div>
        <div>
          <dt className="text-sm text-low">Status</dt>
          <dd className="mt-1">{LABEL[c.status]}</dd>
        </div>
        <div>
          <dt className="text-sm text-low">Location</dt>
          <dd className="mt-1 break-words">{c.location}</dd>
        </div>
        <div>
          <dt className="text-sm text-low">Reporter contact</dt>
          <dd className="mt-1 break-words">{c.reporter_contact ?? "—"}</dd>
        </div>
        <div>
          <dt className="text-sm text-low">Created</dt>
          <dd className="tabular mt-1" title={c.created_at}>
            {relativeTime(c.created_at)}
          </dd>
        </div>
        <div>
          <dt className="text-sm text-low">Last updated</dt>
          <dd className="tabular mt-1" title={c.updated_at}>
            {relativeTime(c.updated_at)}
          </dd>
        </div>
        <div>
          <dt className="text-sm text-low">Triage confidence</dt>
          <dd className="tabular mt-1">
            {c.triage_confidence === null ? "—" : `${String(Math.round(c.triage_confidence * 100))}%`}
          </dd>
        </div>
        <div>
          <dt className="text-sm text-low">Triage latency</dt>
          <dd className="tabular mt-1">{msLabel(c.triage_latency_ms)}</dd>
        </div>
      </dl>

      <div className="mt-6">
        <p className="text-sm text-low">Reported text</p>
        <p className="mt-1 whitespace-pre-wrap">{c.text}</p>
      </div>

      {c.ai_summary && (
        <div className="mt-4">
          <p className="text-sm text-low">Summary</p>
          <p className="mt-1">{c.ai_summary}</p>
        </div>
      )}

      <div className="mt-6">
        <StatusActions complaint={c} />
      </div>
    </section>
  );
}
