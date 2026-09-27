import { useDocumentTitle } from "@/lib/useDocumentTitle";

// Placeholder until FE-05.
export function SubmitPage() {
  useDocumentTitle("Submit complaint");
  return (
    <section className="max-w-form">
      <h1 className="text-xl font-semibold">Report a problem</h1>
      <p className="mt-2">Tell us what is wrong and where. We read it and route it to the right crew.</p>
    </section>
  );
}
