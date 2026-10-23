import type { CacheState } from "@/api/stats";

const LABEL: Record<CacheState, string> = {
  HIT: "Served from cache (HIT)",
  MISS: "Computed fresh (MISS)",
  UNKNOWN: "Loading…",
};

export function CacheIndicator({
  cache,
  fetchedAt,
  onRefresh,
}: {
  cache: CacheState;
  fetchedAt: Date | undefined;
  onRefresh: () => void;
}) {
  return (
    <div className="flex flex-wrap items-center gap-3 text-sm">
      <span
        className={`rounded border px-2 py-1 ${cache === "HIT" ? "border-normal text-normal" : "border-rule"}`}
      >
        {LABEL[cache]}
      </span>
      {fetchedAt && <span className="tabular text-low">fetched {fetchedAt.toLocaleTimeString()}</span>}
      <button type="button" className="btn-sm" onClick={onRefresh}>
        Refresh
      </button>
    </div>
  );
}
