import json
import os
import string
from nltk.stem import PorterStemmer

DEFAULT_SEARCH_LIMIT = 5

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "movies.json")
WORDS_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "stopwords.txt")


def load_movies() -> list[dict]:
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data["movies"]

def load_stopwords() -> list:
    with open(WORDS_DATA_PATH, "r") as f:
        data = f.read()
    data = data.splitlines()
    return data 

def remove_punctuation(enter: str) -> str:
    # Create a translation table that maps each punctuation character to None
    translator = str.maketrans('', '', string.punctuation)
    
    # Use the translate method to remove punctuation
    clean_text = enter.translate(translator)
    return clean_text

def tokenize(enter: str) -> list:
    lista = enter.split()
    filtered_list = [item for item in lista if item]
    return filtered_list

def remove_stop_word(enter: list) -> list:
    stopwords = load_stopwords()
    for item in enter:
        if item in stopwords:
            enter.remove(item)
    return enter

def stemming(enter: list) -> list:
    stemmer = PorterStemmer()
    for i, item in enumerate(enter):
        enter[i] = stemmer.stem(item)
    return enter