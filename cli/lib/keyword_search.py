from .utils import DEFAULT_SEARCH_LIMIT, load_movies, remove_punctuation, tokenize, remove_stop_word, stemming

def search_command(query: str, limit: int = DEFAULT_SEARCH_LIMIT) -> list[dict]:
    movies_list = load_movies()
    query = preprocess_to_lower(query)
    query = remove_punctuation(query)
    list_query = tokenize(query)
    list_query = remove_stop_word(list_query)
    list_query = stemming(list_query)
    result = []
    for movie in movies_list:
        movie1 = preprocess_to_lower(movie["title"])
        movie1 = remove_punctuation(movie1)
        list_movie = tokenize(movie1)
        list_movie = remove_stop_word(list_movie)
        found = False
        for token in list_movie:
            if found:
                break
            for item in list_query:
                if token.find(item) != -1:
                    result.append(movie)
                    found = True
                    break
        if len(result) >= limit:
            break
    return result

def preprocess_to_lower(enter: str) -> str:
    enter = enter.lower()
    return enter