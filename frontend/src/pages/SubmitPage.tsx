import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { Link } from "react-router-dom";

import { useCreateComplaint, type ComplaintCreate, type ComplaintOut } from "@/api/complaints";
import { ApiError } from "@/api/errors";
import { CategoryLabel } from "@/components/CategoryLabel";
import { ElapsedTimer } from "@/components/ElapsedTimer";
import { FieldError } from "@/components/FieldError";
import { InlineAlert } from "@/components/InlineAlert";
import { PriorityBadge } from "@/components/PriorityBadge";
import { PriorityRail } from "@/components/PriorityRail";
import { ProviderTag } from "@/components/ProviderTag";
import { useCountdown } from "@/lib/useCountdown";
import { useDocumentTitle } from "@/lib/useDocumentTitle";
import { useElapsed } from "@/lib/useElapsed";
import { complaintSchema, type ComplaintForm } from "@/lib/validation";

const KNOWN_FIELDS = new Set<keyof ComplaintForm>(["text", "location", "reporter_contact"]);

export function SubmitPage() {
  useDocumentTitle("Submit complaint");

  const form = useForm<ComplaintForm>({
    resolver: zodResolver(complaintSchema),
    defaultValues: { text: "", location: "", reporter_contact: "" },
  });
  const mutation = useCreateComplaint();

  const apiError = mutation.error instanceof ApiError ? mutation.error : null;
  const isRateLimited = apiError?.code === "rate_limited";
  const countdown = useCountdown(isRateLimited ? (apiError.retryAfterS ?? 0) : null);
  const elapsed = useElapsed(mutation.isPending);
  const textLength = form.watch("text").length;

  // Map the server's field errors onto the form and focus the first one (plan §8.8).
  useEffect(() => {
    if (apiError?.code !== "validation_error") return;
    let firstField: keyof ComplaintForm | null = null;
    for (const field of apiError.fields) {
      if (!KNOWN_FIELDS.has(field.field as keyof ComplaintForm)) continue;
      const name = field.field as keyof ComplaintForm;
      form.setError(name, { type: "server", message: field.message });
      firstField ??= name;
    }
    if (firstField) form.setFocus(firstField);
  }, [apiError, form]);

  function onValid(values: ComplaintForm) {
    const payload: ComplaintCreate = {
      text: values.text,
      location: values.location,
      ...(values.reporter_contact !== undefined && { reporter_contact: values.reporter_contact }),
    };
    mutation.mutate(payload);
  }

  function submitAnother() {
    form.reset();
    mutation.reset();
  }

  if (mutation.isSuccess) {
    return <ResultTicket complaint={mutation.data} onSubmitAnother={submitAnother} />;
  }

  const unknownFields =
    apiError?.code === "validation_error"
      ? apiError.fields.filter((f) => !KNOWN_FIELDS.has(f.field as keyof ComplaintForm))
      : [];
  const genericMessage =
    apiError && apiError.code !== "validation_error" && apiError.code !== "rate_limited" ? apiError.message : null;
  const networkError = mutation.isError && !apiError;

  return (
    <section className="max-w-form">
      <h1 className="text-xl font-semibold">Report a problem</h1>
      <p className="mt-2">Tell us what is wrong and where. We read it and route it to the right crew.</p>

      <form onSubmit={(e) => void form.handleSubmit(onValid)(e)} noValidate className="mt-6 space-y-5">
        <div>
          <label htmlFor="text" className="block font-medium">
            What&apos;s wrong?
          </label>
          <textarea
            id="text"
            rows={6}
            className="mt-1 w-full rounded border border-rule bg-panel p-2"
            aria-invalid={!!form.formState.errors.text}
            aria-describedby={form.formState.errors.text ? "text-error" : "text-count"}
            {...form.register("text")}
          />
          <p id="text-count" className={`tabular mt-1 text-sm ${textLength > 2000 ? "text-high" : "text-low"}`}>
            {textLength} / 2000
          </p>
          <FieldError id="text-error" message={form.formState.errors.text?.message} />
        </div>

        <div>
          <label htmlFor="location" className="block font-medium">
            Location
          </label>
          <input
            id="location"
            type="text"
            placeholder="Street 12, G-9/2, Islamabad"
            className="mt-1 w-full rounded border border-rule bg-panel p-2"
            aria-invalid={!!form.formState.errors.location}
            aria-describedby={form.formState.errors.location ? "location-error" : undefined}
            {...form.register("location")}
          />
          <FieldError id="location-error" message={form.formState.errors.location?.message} />
        </div>

        <div>
          <label htmlFor="reporter_contact" className="block font-medium">
            Contact (optional)
          </label>
          <input
            id="reporter_contact"
            type="text"
            className="mt-1 w-full rounded border border-rule bg-panel p-2"
            aria-invalid={!!form.formState.errors.reporter_contact}
            aria-describedby={form.formState.errors.reporter_contact ? "reporter_contact-error" : "contact-hint"}
            {...form.register("reporter_contact")}
          />
          <p id="contact-hint" className="mt-1 text-sm text-low">
            Phone or email, only if you want a callback.
          </p>
          <FieldError id="reporter_contact-error" message={form.formState.errors.reporter_contact?.message} />
        </div>

        {unknownFields.length > 0 && (
          <InlineAlert>
            {unknownFields.map((f) => (
              <p key={f.field}>
                {f.field}: {f.message}
              </p>
            ))}
          </InlineAlert>
        )}
        {genericMessage && <InlineAlert>{genericMessage}</InlineAlert>}
        {networkError && <InlineAlert>Could not reach the server. Check your connection and try again.</InlineAlert>}
        {isRateLimited && (
          <InlineAlert>
            Too many complaints from this connection. You can submit again in {countdown} s.
          </InlineAlert>
        )}

        <button
          type="submit"
          disabled={mutation.isPending || (isRateLimited && countdown > 0)}
          className="btn"
        >
          {mutation.isPending ? "Reading your complaint…" : "Submit complaint"}
        </button>

        {mutation.isPending && (
          <div role="status" aria-live="polite" className="text-sm text-low">
            <p>
              Reading your complaint… <ElapsedTimer seconds={elapsed} />
            </p>
            {elapsed >= 8 && <p>Still working. The AI service is slow, so we may use our backup classifier.</p>}
          </div>
        )}
      </form>
    </section>
  );
}

function ResultTicket({
  complaint,
  onSubmitAnother,
}: {
  complaint: ComplaintOut;
  onSubmitAnother: () => void;
}) {
  function copyId() {
    // navigator.clipboard is typed as always present, but isn't on every real
    // browser/context (e.g. non-secure origins), hence the try/catch.
    try {
      navigator.clipboard.writeText(complaint.id).catch(() => undefined);
    } catch {
      // Clipboard unsupported here; the ID is still visible to select and copy by hand.
    }
  }

  return (
    <section className="max-w-form">
      <div className="relative overflow-hidden rounded border border-rule bg-panel p-6 pl-8">
        <PriorityRail priority={complaint.priority} />
        <h1 className="text-xl font-semibold">Complaint received</h1>
        <p className="tabular mt-1 flex items-center gap-2 break-all text-sm text-low">
          {complaint.id}
          <button type="button" onClick={copyId} className="underline">
            Copy
          </button>
        </p>

        <dl className="mt-4 space-y-3">
          <div className="flex justify-between gap-4">
            <dt className="text-low">Category</dt>
            <dd>
              <CategoryLabel category={complaint.category} />
            </dd>
          </div>
          <div className="flex justify-between gap-4">
            <dt className="text-low">Priority</dt>
            <dd>
              <PriorityBadge priority={complaint.priority} />
            </dd>
          </div>
          <div className="flex justify-between gap-4">
            <dt className="text-low">Summary</dt>
            <dd className="text-right">{complaint.ai_summary ?? "No summary"}</dd>
          </div>
          <div className="flex justify-between gap-4">
            <dt className="text-low">Triaged by</dt>
            <dd>
              <ProviderTag triagedBy={complaint.triaged_by} />
            </dd>
          </div>
          <div className="flex justify-between gap-4">
            <dt className="text-low">Triage time</dt>
            <dd className="tabular">{complaint.triage_latency_ms} ms</dd>
          </div>
        </dl>

        <div className="mt-6 flex gap-3">
          <Link to={`/complaints/${complaint.id}`} className="btn">
            View complaint
          </Link>
          <button type="button" onClick={onSubmitAnother} className="btn">
            Submit another
          </button>
        </div>
      </div>
    </section>
  );
}
