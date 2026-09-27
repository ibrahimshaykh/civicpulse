import { useSearchParams } from "react-router-dom";

import { useComplaints } from "@/api/complaints";
import { ComplaintTable } from "@/components/ComplaintTable";
import { EmptyState } from "@/components/EmptyState";
import { FilterBar, type Filters } from "@/components/FilterBar";
import { PAGE_SIZES, Pagination } from "@/components/Pagination";
import { CATEGORIES, PRIORITIES, STATUSES } from "@/lib/enums";
import { useDocumentTitle } from "@/lib/useDocumentTitle";

// An unknown value (?category=foo) is dropped rather than sent to the server (plan §8.9).
function parseEnum<T extends string>(value: string | null, allowed: readonly T[]): T | undefined {
  return value !== null && (allowed as readonly string[]).includes(value) ? (value as T) : undefined;
}

function parsePage(value: string | null): number {
  const n = value !== null ? Number.parseInt(value, 10) : NaN;
  return Number.isInteger(n) && n >= 1 ? n : 1;
}

function parsePageSize(value: string | null): number {
  const n = value !== null ? Number.parseInt(value, 10) : NaN;
  return (PAGE_SIZES as readonly number[]).includes(n) ? n : 20;
}

export function DashboardPage() {
  useDocumentTitle("Dashboard");
  const [params, setParams] = useSearchParams();

  const filters: Filters = {
    category: parseEnum(params.get("category"), CATEGORIES),
    priority: parseEnum(params.get("priority"), PRIORITIES),
    status: parseEnum(params.get("status"), STATUSES),
  };
  const page = parsePage(params.get("page"));
  const pageSize = parsePageSize(params.get("page_size"));

  const query = useComplaints({ ...filters, page, pageSize });

  function applyFilters(next: Filters) {
    const p = new URLSearchParams(params);
    (["category", "priority", "status"] as const).forEach((key) => {
      const value = next[key];
      if (value) p.set(key, value);
      else p.delete(key);
    });
    p.set("page", "1"); // changing a filter resets to page 1 (plan §8.9)
    setParams(p);
  }

  function goToPage(next: number) {
    const p = new URLSearchParams(params);
    p.set("page", String(next));
    setParams(p);
  }

  function changePageSize(next: number) {
    const p = new URLSearchParams(params);
    p.set("page_size", String(next));
    p.set("page", "1");
    setParams(p);
  }

  function clearFilters() {
    setParams(new URLSearchParams());
  }

  return (
    <section className="max-w-board">
      <h1 className="text-xl font-semibold">Complaints</h1>
      <p className="mt-2">Every reported problem, most urgent first.</p>

      <div className="mt-6">
        <FilterBar filters={filters} onChange={applyFilters} />
      </div>

      <div className="mt-4">
        {query.isPending && <p className="text-low">Loading…</p>}
        {query.isError && <p className="text-high">Could not load complaints.</p>}
        {query.data && query.data.items.length === 0 && <EmptyState onClear={clearFilters} />}
        {query.data && query.data.items.length > 0 && (
          <>
            <ComplaintTable items={query.data.items} />
            <Pagination
              page={query.data.page}
              pageSize={query.data.page_size}
              total={query.data.total}
              onPageChange={goToPage}
              onPageSizeChange={changePageSize}
            />
          </>
        )}
      </div>
    </section>
  );
}
