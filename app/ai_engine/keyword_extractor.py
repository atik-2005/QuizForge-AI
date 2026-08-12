from collections import Counter
import re

STOP_WORDS = {
    "the", "is", "are", "was", "were", "a", "an", "and", "or",
    "of", "to", "in", "on", "for", "with", "by", "from", "as",
    "at", "this", "that", "these", "those", "it", "its", "be",
    "been", "being", "has", "have", "had", "can", "will", "would",
    "should", "could", "about", "into", "than", "then", "their",
    "there", "they", "them", "we", "you", "your", "he", "she",
    "his", "her"
}

def extract_keywords(text, top_n=20):
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())

    words = [
        word for word in words
        if word not in STOP_WORDS
    ]

    frequency = Counter(words)

    return [word for word, count in frequency.most_common(top_n)]
