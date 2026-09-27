import { Link } from "react-router-dom";

import type { ComplaintOut } from "@/api/complaints";
import { relativeTime } from "@/lib/format";

import { CategoryLabel } from "./CategoryLabel";
import { PriorityBadge } from "./PriorityBadge";
import { PriorityRail } from "./PriorityRail";
import { ProviderTag } from "./ProviderTag";
import { StatusActions } from "./StatusActions";

const STATUS_LABEL: Record<ComplaintOut["status"], string> = {
  open: "Open",
  in_progress: "In progress",
  resolved: "Resolved",
  rejected: "Rejected",
};

function truncate(text: string, max = 80): string {
  return text.length > max ? `${text.slice(0, max - 1)}…` : text;
}

export function ComplaintTable({ items }: { items: ComplaintOut[] }) {
  return (
    <div className="overflow-x-auto rounded border border-rule bg-panel">
      <table className="w-full min-w-[900px] text-left text-sm">
        <thead>
          <tr className="border-b border-rule text-low">
            <th className="w-1" aria-hidden="true" />
            <th className="px-3 py-2 font-medium">Created</th>
            <th className="px-3 py-2 font-medium">Category</th>
            <th className="px-3 py-2 font-medium">Priority</th>
            <th className="px-3 py-2 font-medium">Status</th>
            <th className="px-3 py-2 font-medium">Location</th>
            <th className="px-3 py-2 font-medium">Summary</th>
            <th className="px-3 py-2 font-medium">Triaged by</th>
            <th className="px-3 py-2 font-medium">Actions</th>
          </tr>
        </thead>
        <tbody>
          {items.map((c) => (
            <tr key={c.id} className="relative border-b border-rule last:border-0">
              <td className="p-0">
                <PriorityRail priority={c.priority} />
              </td>
              <td className="tabular whitespace-nowrap px-3 py-2" title={c.created_at}>
                {relativeTime(c.created_at)}
              </td>
              <td className="px-3 py-2">
                <CategoryLabel category={c.category} />
              </td>
              <td className="px-3 py-2">
                <PriorityBadge priority={c.priority} />
              </td>
              <td className="px-3 py-2">{STATUS_LABEL[c.status]}</td>
              <td className="max-w-[160px] truncate px-3 py-2" title={c.location}>
                {c.location}
              </td>
              <td className="max-w-xs px-3 py-2">
                <Link to={`/complaints/${c.id}`} className="block truncate underline" title={c.ai_summary ?? c.text}>
                  {truncate(c.ai_summary ?? c.text)}
                </Link>
              </td>
              <td className="px-3 py-2">
                <ProviderTag triagedBy={c.triaged_by} />
              </td>
              <td className="px-3 py-2">
                <StatusActions complaint={c} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
