import { useDocumentTitle } from "@/lib/useDocumentTitle";

// Placeholder until FE-07.
export function DashboardPage() {
  useDocumentTitle("Dashboard");
  return (
    <section className="max-w-board">
      <h1 className="text-xl font-semibold">Complaints</h1>
      <p className="mt-2">Every reported problem, most urgent first.</p>
    </section>
  );
}
