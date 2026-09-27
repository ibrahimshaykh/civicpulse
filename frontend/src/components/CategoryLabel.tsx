import { LABEL, type Category } from "@/lib/enums";

// A small glyph per category, distinct in shape (not only color) so it still
// carries meaning for a color-blind viewer or in print (plan §8.2).
const GLYPH: Record<Category, string> = {
  water: "M10 2c-3 4-5 7-5 10a5 5 0 0 0 10 0c0-3-2-6-5-10Z",
  electricity: "m11 2-7 10h4l-2 6 7-10h-4Z",
  sanitation: "M4 4h12l-1 12a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2Z M3 4h14 M7 4V2h6v2",
  roads: "M4 17 8 3h4l4 14 M9 8h2 M8.5 12h3",
  streetlights: "M10 2v3 M6 5h8l-1 4H7Z M9 9h2v7H9Z M6 16h8",
  other: "M10 3a7 7 0 1 0 0 14 7 7 0 0 0 0-14Z",
};

export function CategoryLabel({ category }: { category: Category }) {
  return (
    <span className="inline-flex items-center gap-1.5">
      <svg viewBox="0 0 20 20" width="16" height="16" aria-hidden="true" className="shrink-0 text-ink">
        <path d={GLYPH[category]} fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      {LABEL[category]}
    </span>
  );
}
