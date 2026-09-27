import { keepPreviousData, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import type { Status } from "@/lib/enums";

import { api } from "./client";
import { toApiError } from "./errors";
import { qk, type ComplaintFilters } from "./queryKeys";
import type { components } from "./schema";

export type ComplaintCreate = components["schemas"]["ComplaintCreate"];
export type ComplaintOut = components["schemas"]["ComplaintOut"];

export function useComplaints(f: ComplaintFilters) {
  return useQuery({
    queryKey: qk.complaints(f),
    queryFn: async () => {
      const { data, error, response } = await api.GET("/api/complaints", {
        params: {
          // Keys are omitted rather than set to undefined: with
          // exactOptionalPropertyTypes, an explicit `category: undefined` is not
          // assignable to an optional `category?: ... | null` query param.
          query: {
            ...(f.category !== undefined && { category: f.category }),
            ...(f.priority !== undefined && { priority: f.priority }),
            ...(f.status !== undefined && { status: f.status }),
            page: f.page,
            page_size: f.pageSize,
          },
        },
      });
      if (error) throw toApiError(response, error);
      return data;
    },
    placeholderData: keepPreviousData, // no flash to empty between pages
  });
}

export function useComplaint(id: string) {
  return useQuery({
    queryKey: qk.complaint(id),
    queryFn: async () => {
      const { data, error, response } = await api.GET("/api/complaints/{complaint_id}", {
        params: { path: { complaint_id: id } },
      });
      if (error) throw toApiError(response, error);
      return data;
    },
  });
}

export function useCreateComplaint() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (body: ComplaintCreate) => {
      const { data, error, response } = await api.POST("/api/complaints", { body });
      if (error) throw toApiError(response, error);
      return data;
    },
    retry: 0, // never retry a POST: it would create a duplicate complaint
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: ["complaints"] });
      void qc.invalidateQueries({ queryKey: qk.stats });
    },
  });
}

export function useUpdateStatus() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async ({ id, status }: { id: string; status: Status }) => {
      const { data, error, response } = await api.PATCH("/api/complaints/{complaint_id}/status", {
        params: { path: { complaint_id: id } },
        body: { status },
      });
      if (error) throw toApiError(response, error);
      return data;
    },
    retry: 0,
    onSuccess: (updated) => {
      qc.setQueryData(qk.complaint(updated.id), updated);
      void qc.invalidateQueries({ queryKey: ["complaints"] });
      void qc.invalidateQueries({ queryKey: qk.stats });
    },
    // A 409 means someone else changed it first; re-sync the list rather than trust our own guess.
    onError: () => {
      void qc.invalidateQueries({ queryKey: ["complaints"] });
    },
  });
}
