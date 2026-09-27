"""PII redaction before anything reaches a third-party LLM or gets logged
(task AI-07, feeds ADR 0004). `reporter_contact` and `location` are never
sent at all (plan §11.4); this catches PII that shows up inside the
complaint text itself, which citizens do write despite the form's own
field separation.
"""

import re

PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"(?:\+92|0092|0)3\d{2}[\s-]?\d{7}"), "[PHONE]"),  # Pakistani mobile
    (re.compile(r"\b\d{5}-?\d{7}-?\d\b"), "[CNIC]"),  # national ID
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), "[EMAIL]"),
    (re.compile(r"\b(?:house|h\.?\s?no\.?|plot)\s*#?\s*\d+[a-z]?\b", re.IGNORECASE), "[ADDRESS]"),
]


def redact(text: str) -> str:
    for pattern, replacement in PATTERNS:
        text = pattern.sub(replacement, text)
    return text
