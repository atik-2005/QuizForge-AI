from keybert import KeyBERT

kw_model = KeyBERT("all-MiniLM-L6-v2")


def extract_keywords(text, top_n=20):

    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=top_n
    )

    return [keyword for keyword, score in keywords]
