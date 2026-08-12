from collections import Counter
import re


def extract_keywords(text, top_n=20):
    """
    Lightweight keyword extraction.
    No KeyBERT, PyTorch, or Transformer model required.
    """

    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9-]{2,}\b", text.lower())

    stop_words = {
        "the", "and", "for", "are", "with", "that", "this",
        "from", "was", "were", "have", "has", "had", "not",
        "but", "you", "your", "their", "they", "there",
        "what", "which", "when", "where", "how", "why",
        "into", "about", "then", "than", "also", "can",
        "will", "would", "could", "should", "been", "being",
        "using", "used", "use", "its", "it", "is", "in",
        "on", "of", "to", "a", "an", "as", "by", "or"
    }

    filtered_words = [
        word for word in words
        if word not in stop_words
    ]

    frequency = Counter(filtered_words)

    return [
        word
        for word, count in frequency.most_common(top_n)
    ]
