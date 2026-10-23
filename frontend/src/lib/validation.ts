import { z } from "zod";

// Mirrors ComplaintCreate (backend/app/schemas/complaint.py) for a fast client
// check. The server's answer is authoritative — this never replaces it (plan §8.1).
export const complaintSchema = z.object({
  text: z
    .string()
    .trim()
    .min(10, "Describe the problem in at least 10 characters")
    .max(2000, "Keep it under 2000 characters"),
  location: z
    .string()
    .trim()
    .min(3, "Add a location of at least 3 characters")
    .max(200, "Keep the location under 200 characters"),
  reporter_contact: z
    .string()
    .trim()
    .max(120, "Keep the contact under 120 characters")
    .optional()
    .transform((v) => (v === "" ? undefined : v))
    .refine((v) => v === undefined || v.length >= 3, "Contact must be at least 3 characters"),
});

export type ComplaintForm = z.input<typeof complaintSchema>;
