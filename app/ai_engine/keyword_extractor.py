import re
from collections import Counter


STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then",
    "is", "are", "was", "were", "be", "been", "being",
    "to", "of", "in", "on", "for", "with", "as", "by",
    "at", "from", "this", "that", "these", "those",
    "it", "its", "into", "about", "than", "their",
    "they", "them", "he", "she", "his", "her",
    "you", "your", "we", "our", "can", "will"
}


def extract_keywords(text, top_n=20):

    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())

    words = [
        word for word in words
        if word not in STOP_WORDS
    ]

    frequency = Counter(words)

    return [
        word
        for word, count in frequency.most_common(top_n)
    ]
