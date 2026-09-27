import type { Priority } from "@/lib/enums";

const COLOR: Record<Priority, string> = {
  high: "bg-high",
  normal: "bg-normal",
  low: "bg-low",
};

// The 4px priority rail on the left edge of a row or ticket (plan §8.2's
// "memorable element" — an operator scanning many rows sees the red ones first).
export function PriorityRail({ priority }: { priority: Priority }) {
  return <span aria-hidden="true" className={`absolute inset-y-0 left-0 w-1 ${COLOR[priority]}`} />;
}
