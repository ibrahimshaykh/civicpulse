import { useParams } from "react-router-dom";

import { useDocumentTitle } from "@/lib/useDocumentTitle";

// Placeholder until the API client exists (FE-02); plan §8.11.
export function ComplaintDetailPage() {
  const { id = "" } = useParams();
  useDocumentTitle("Complaint");
  return (
    <section className="max-w-board">
      <h1 className="text-xl font-semibold">Complaint</h1>
      <p className="tabular mt-2 break-all text-low">{id}</p>
    </section>
  );
}
