export type CountEntry = { key: string; label: string; count: number };

// CSS-width bars, not a chart library: keeps the bundle tiny, and the number is
// printed alongside each bar so color is never the only carrier of meaning
// (plan §8.10).
export function CountBars({ title, entries }: { title: string; entries: CountEntry[] }) {
  const max = Math.max(1, ...entries.map((e) => e.count));
  return (
    <div>
      <h3 className="font-medium">{title}</h3>
      <ul className="mt-2 space-y-1.5">
        {entries.map((e) => (
          <li key={e.key} className="flex items-center gap-2 text-sm">
            <span className="w-28 shrink-0 text-low">{e.label}</span>
            <span className="h-3 flex-1 overflow-hidden rounded bg-rule">
              <span
                className="block h-3 rounded bg-ink"
                style={{ width: `${String((e.count / max) * 100)}%` }}
              />
            </span>
            <span className="tabular w-8 text-right">{e.count}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
