import json
import os
import string

DEFAULT_SEARCH_LIMIT = 5

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "movies.json")


def load_movies() -> list[dict]:
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data["movies"]

def remove_punctuation(enter: str) -> str:
    # Create a translation table that maps each punctuation character to None
    translator = str.maketrans('', '', string.punctuation)
    
    # Use the translate method to remove punctuation
    clean_text = enter.translate(translator)
    return clean_text