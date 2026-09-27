"""Exceptions shared across triage providers, kept separate from any one
provider module so `TriageService`'s retry policy (AI-05) can reference
them without importing a provider it doesn't otherwise depend on.
"""


class OllamaServerError(Exception):
    """Raised by OllamaTriage (AI-09) for a 5xx response from the Ollama
    server. Listed in TriageService.RETRYABLE ahead of AI-09 landing, the
    same way the frozen seam is coded against before every provider exists.
    """

    def __init__(self, status_code: int) -> None:
        self.status_code = status_code
        super().__init__(f"Ollama server error: {status_code}")
