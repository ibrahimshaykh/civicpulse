// crypto.randomUUID() only exists in secure contexts (HTTPS or localhost).
// On a plain-HTTP LAN host it is undefined at runtime, even though lib.dom's
// ambient types claim it's always present — hence the cast below rather than
// a plain `"randomUUID" in crypto` check, which TS narrows to `never`.
export function newRequestId(): string {
  const randomUUID = (crypto as { randomUUID?: () => string }).randomUUID;
  if (typeof randomUUID === "function") return randomUUID.call(crypto);

  const bytes = crypto.getRandomValues(new Uint8Array(16));
  bytes[6] = ((bytes[6] ?? 0) & 0x0f) | 0x40;
  bytes[8] = ((bytes[8] ?? 0) & 0x3f) | 0x80;
  const hex = [...bytes].map((b) => b.toString(16).padStart(2, "0")).join("");
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
}
