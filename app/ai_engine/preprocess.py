import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer

# Required NLTK resources
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def clean_text(text):

    # Remove C/C++ code
    text = re.sub(r'#include.*', ' ', text)
    text = re.sub(r'printf.*', ' ', text)
    text = re.sub(r'scanf.*', ' ', text)
    text = re.sub(r'void\s+main', ' ', text)
    text = re.sub(r'int\s+main', ' ', text)

    # Remove special symbols
    text = re.sub(r'[{}();<>#]', ' ', text)

    # Remove numbers
    text = re.sub(r'\d+', ' ', text)

    # Keep only English letters and punctuation
    text = re.sub(r'[^a-zA-Z.,!? ]', ' ', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def sentence_split(text):
    return sent_tokenize(text)


def word_split(text):
    return word_tokenize(text)


def remove_stopwords(words):
    return [
        word for word in words
        if word.lower() not in stop_words and len(word) > 2
    ]


def lemmatize(words):
    return [lemmatizer.lemmatize(word.lower()) for word in words]
