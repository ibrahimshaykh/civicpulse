import { CATEGORIES, LABEL, PRIORITIES, STATUSES, type Category, type Priority, type Status } from "@/lib/enums";

export type Filters = {
  category?: Category | undefined;
  priority?: Priority | undefined;
  status?: Status | undefined;
};

export function FilterBar({
  filters,
  onChange,
}: {
  filters: Filters;
  onChange: (filters: Filters) => void;
}) {
  return (
    <div className="flex flex-wrap gap-3">
      <label className="flex items-center gap-1.5 text-sm">
        Category
        <select
          value={filters.category ?? ""}
          onChange={(e) => {
            onChange({ ...filters, category: (e.target.value || undefined) as Category | undefined });
          }}
          className="rounded border border-rule bg-panel px-2 py-1"
        >
          <option value="">All</option>
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>
              {LABEL[c]}
            </option>
          ))}
        </select>
      </label>
      <label className="flex items-center gap-1.5 text-sm">
        Priority
        <select
          value={filters.priority ?? ""}
          onChange={(e) => {
            onChange({ ...filters, priority: (e.target.value || undefined) as Priority | undefined });
          }}
          className="rounded border border-rule bg-panel px-2 py-1"
        >
          <option value="">All</option>
          {PRIORITIES.map((p) => (
            <option key={p} value={p}>
              {LABEL[p]}
            </option>
          ))}
        </select>
      </label>
      <label className="flex items-center gap-1.5 text-sm">
        Status
        <select
          value={filters.status ?? ""}
          onChange={(e) => {
            onChange({ ...filters, status: (e.target.value || undefined) as Status | undefined });
          }}
          className="rounded border border-rule bg-panel px-2 py-1"
        >
          <option value="">All</option>
          {STATUSES.map((s) => (
            <option key={s} value={s}>
              {LABEL[s]}
            </option>
          ))}
        </select>
      </label>
    </div>
  );
}
