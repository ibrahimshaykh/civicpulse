import type { components } from "./schema";

type ErrorDetail = components["schemas"]["ErrorDetail"];

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly detail: ErrorDetail | null,
    public readonly retryAfterS: number | null,
  ) {
    super(detail?.message ?? `Request failed with status ${String(status)}`);
    this.name = "ApiError";
  }

  get code(): string {
    return this.detail?.code ?? "unknown";
  }

  get fields(): NonNullable<ErrorDetail["fields"]> {
    return this.detail?.fields ?? [];
  }

  get requestId(): string | null {
    return this.detail?.request_id ?? null;
  }
}

export function toApiError(response: Response, body: unknown): ApiError {
  const detail = isErrorBody(body) ? body.error : null;
  const header = response.headers.get("Retry-After");
  const parsed = header ? Number.parseInt(header, 10) : (detail?.retry_after_s ?? null);
  const retryAfter = parsed !== null && Number.isFinite(parsed) ? parsed : null;
  return new ApiError(response.status, detail, retryAfter);
}

function isErrorBody(x: unknown): x is { error: ErrorDetail } {
  return typeof x === "object" && x !== null && "error" in x;
}
