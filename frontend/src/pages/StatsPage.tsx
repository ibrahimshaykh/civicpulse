import { useDocumentTitle } from "@/lib/useDocumentTitle";

// Placeholder until FE-09.
export function StatsPage() {
  useDocumentTitle("Stats");
  return (
    <section className="max-w-board">
      <h1 className="text-xl font-semibold">Stats</h1>
      <p className="mt-2">Totals by category, priority and status.</p>
    </section>
  );
}
