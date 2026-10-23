const PROVIDER_LABEL: Record<string, string> = {
  "llm:groq": "AI · Groq",
  "llm:ollama": "AI · Ollama (offline)",
  rules: "Keyword rules",
  "rules:fallback": "Keyword rules (AI unavailable)",
  simulated: "Simulated",
};

// The fallback case gets a visually distinct outline so it's obviously
// different in the demo video, not just a different label (plan §8.8).
export function ProviderTag({ triagedBy }: { triagedBy: string }) {
  const isFallback = triagedBy === "rules:fallback";
  const label = PROVIDER_LABEL[triagedBy] ?? triagedBy;
  return (
    <span
      className={`inline-block rounded border px-2 py-0.5 text-sm ${
        isFallback ? "border-high border-dashed text-high" : "border-rule text-ink"
      }`}
    >
      {label}
    </span>
  );
}
