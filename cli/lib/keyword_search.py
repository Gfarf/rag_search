from .utils import DEFAULT_SEARCH_LIMIT, load_movies, remove_punctuation

def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies_list = load_movies()
    query = preprocess_to_lower(query)
    query = remove_punctuation(query)
    result = []
    for movie in movies_list:
        movie1 = preprocess_to_lower(movie["title"])
        movie1 = remove_punctuation(movie1)
        if movie1.find(query) != -1:
            result.append(movie)
        if len(result) >= limit:
            break
    return result

def preprocess_to_lower(enter: str) -> str:
    enter = enter.lower()
    return enter