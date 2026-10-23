"""Text normalization shared by the rule-based provider (matching) and the
content-hash cache (AI-08, hashing) -- one implementation so the two never
drift apart and disagree on what counts as "the same complaint".
"""

import re
import unicodedata


def normalize(text: str) -> str:
    t = unicodedata.normalize("NFKC", text).casefold()
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def first_sentence(text: str, *, limit: int) -> str:
    """The text's first sentence, truncated at a word boundary to `limit` chars."""
    stripped = text.strip()
    end = len(stripped)
    for punct in (". ", "! ", "? ", ".\n"):
        idx = stripped.find(punct)
        if idx != -1:
            end = min(end, idx + 1)
    sentence = stripped[:end].strip()
    if len(sentence) <= limit:
        return sentence
    truncated = sentence[:limit].rsplit(" ", 1)[0]
    return truncated.rstrip(",;: ") + "..."
