const MINUTE = 60_000;
const HOUR = 60 * MINUTE;
const DAY = 24 * HOUR;

/**
 * "3 min ago", "2 h ago", "5 d ago" — falls back to a plain date beyond a week.
 * Handles a timestamp slightly in the future (clock skew) the same way, saying
 * "from now" instead of "ago", rather than collapsing every past date to
 * "just now" the way a naive `diff < MINUTE` check would.
 */
export function relativeTime(iso: string, now: Date = new Date()): string {
  const diff = now.getTime() - new Date(iso).getTime();
  const abs = Math.abs(diff);
  const suffix = diff < 0 ? "from now" : "ago";
  if (abs < MINUTE) return "just now";
  if (abs < HOUR) return `${String(Math.floor(abs / MINUTE))} min ${suffix}`;
  if (abs < DAY) return `${String(Math.floor(abs / HOUR))} h ${suffix}`;
  if (abs < 7 * DAY) return `${String(Math.floor(abs / DAY))} d ${suffix}`;
  return new Date(iso).toLocaleDateString();
}

export function msLabel(ms: number): string {
  return `${String(ms)} ms`;
}
