import { Link } from "react-router-dom";

import { useDocumentTitle } from "@/lib/useDocumentTitle";

export function NotFoundPage() {
  useDocumentTitle("Page not found");
  return (
    <section className="max-w-form">
      <h1 className="text-xl font-semibold">Page not found</h1>
      <p className="mt-2">
        There is nothing at this address.{" "}
        <Link to="/submit" className="underline">
          Report a problem
        </Link>{" "}
        or{" "}
        <Link to="/dashboard" className="underline">
          open the dashboard
        </Link>
        .
      </p>
    </section>
  );
}
