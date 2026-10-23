import { useState } from "react";

import { useProviders } from "@/api/meta";
import { useStats } from "@/api/stats";
import { CacheIndicator } from "@/components/CacheIndicator";
import { CountBars, type CountEntry } from "@/components/CountBars";
import { ProviderTag } from "@/components/ProviderTag";
import { CATEGORIES, LABEL, PRIORITIES, STATUSES } from "@/lib/enums";
import { msLabel, relativeTime } from "@/lib/format";
import { useDocumentTitle } from "@/lib/useDocumentTitle";

export function StatsPage() {
  useDocumentTitle("Stats");
  const [autoRefresh, setAutoRefresh] = useState(false);
  const stats = useStats({ autoRefresh });
  const providers = useProviders();

  const data = stats.data?.stats;
  const categoryEntries: CountEntry[] = data
    ? CATEGORIES.map((c) => ({ key: c, label: LABEL[c], count: data.by_category[c] ?? 0 }))
    : [];
  const priorityEntries: CountEntry[] = data
    ? PRIORITIES.map((p) => ({ key: p, label: LABEL[p], count: data.by_priority[p] ?? 0 }))
    : [];
  const statusEntries: CountEntry[] = data
    ? STATUSES.map((s) => ({ key: s, label: LABEL[s], count: data.by_status[s] ?? 0 }))
    : [];

  return (
    <section className="max-w-board">
      <h1 className="text-xl font-semibold">Stats</h1>
      <p className="mt-2">Totals by category, priority and status.</p>

      <div className="mt-6 flex flex-wrap items-center gap-4">
        <CacheIndicator
          cache={stats.data?.cache ?? "UNKNOWN"}
          fetchedAt={stats.data?.fetchedAt}
          onRefresh={() => void stats.refetch()}
        />
        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={autoRefresh}
            onChange={(e) => {
              setAutoRefresh(e.target.checked);
            }}
          />
          Auto-refresh (10 s)
        </label>
      </div>

      {stats.isError && <p className="mt-4 text-high">Could not load stats.</p>}

      {stats.data && (
        <>
          <p className="tabular mt-6">{stats.data.stats.total} total complaints</p>
          <div className="mt-4 grid gap-x-8 gap-y-6 md:grid-cols-3">
            <CountBars title="By category" entries={categoryEntries} />
            <CountBars title="By priority" entries={priorityEntries} />
            <CountBars title="By status" entries={statusEntries} />
          </div>
        </>
      )}

      <div className="mt-10">
        <h2 className="text-lg font-semibold">Providers</h2>
        {providers.isError && <p className="mt-2 text-high">Could not load provider data.</p>}
        {providers.data && (
          <>
            <dl className="mt-2 flex flex-wrap gap-x-8 gap-y-2 text-sm">
              <div className="flex items-center gap-2">
                <dt className="text-low">Active</dt>
                <dd>
                  <ProviderTag triagedBy={providers.data.active_provider} />
                </dd>
              </div>
              <div className="flex items-center gap-2">
                <dt className="text-low">Model</dt>
                <dd>{providers.data.model ?? "—"}</dd>
              </div>
              <div className="flex items-center gap-2">
                <dt className="text-low">Cache hit rate</dt>
                <dd className="tabular">
                  {providers.data.cache_hit_rate !== null
                    ? `${String(Math.round(providers.data.cache_hit_rate * 100))}%`
                    : "—"}
                </dd>
              </div>
            </dl>

            <div className="mt-4 overflow-x-auto rounded border border-rule bg-panel">
              <table className="w-full min-w-[600px] text-left text-sm">
                <thead>
                  <tr className="border-b border-rule text-low">
                    <th className="px-3 py-2 font-medium">Provider</th>
                    <th className="px-3 py-2 font-medium">Latency</th>
                    <th className="px-3 py-2 font-medium">Fallback</th>
                    <th className="px-3 py-2 font-medium">Cache</th>
                    <th className="px-3 py-2 font-medium">When</th>
                  </tr>
                </thead>
                <tbody>
                  {providers.data.recent.map((outcome, i) => (
                    <tr
                      key={`${outcome.complaint_id}-${String(i)}`}
                      className={`border-b border-rule last:border-0 ${outcome.fallback ? "border-l-4 border-l-high border-dashed" : ""}`}
                    >
                      <td className="px-3 py-2">
                        <ProviderTag triagedBy={outcome.provider} />
                      </td>
                      <td className="tabular px-3 py-2">{msLabel(outcome.latency_ms)}</td>
                      <td className="px-3 py-2">{outcome.fallback ? "Yes" : "No"}</td>
                      <td className="px-3 py-2">{outcome.cache_hit ? "Yes" : "No"}</td>
                      <td className="px-3 py-2" title={outcome.at}>
                        {relativeTime(outcome.at)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </div>
    </section>
  );
}
