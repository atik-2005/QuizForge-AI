
import re
from collections import Counter

def extract_keywords(text, top_n=10):
    if not text:
        return []

    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    frequency = Counter(words)

    return [word for word, _ in frequency.most_common(top_n)]
