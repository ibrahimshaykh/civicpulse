import { LABEL, type Priority } from "@/lib/enums";

const STYLE: Record<Priority, string> = {
  high: "border-high text-high",
  normal: "border-normal text-normal",
  low: "border-low text-low",
};

export function PriorityBadge({ priority }: { priority: Priority }) {
  return (
    <span className={`inline-block rounded border px-2 py-0.5 text-sm font-medium ${STYLE[priority]}`}>
      {LABEL[priority]}
    </span>
  );
}
