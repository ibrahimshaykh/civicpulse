export function EmptyState({ onClear }: { onClear: () => void }) {
  return (
    <div className="rounded border border-rule bg-panel p-8 text-center">
      <p>No complaints match these filters.</p>
      <button type="button" onClick={onClear} className="btn mt-4">
        Clear filters
      </button>
    </div>
  );
}
