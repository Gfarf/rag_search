from .utils import full_tokenization, load_movies, PROJECT_ROOT, DEFAULT_SEARCH_LIMIT
from collections import defaultdict, Counter
import os
import pickle
import math

CACHE = os.path.join(PROJECT_ROOT, "cache")
CACHE_INDEX = os.path.join(CACHE, "index.pkl")
CACHE_DOCMAP = os.path.join(CACHE, "docmap.pkl")
CACHE_TERM_FREQUENCIES = os.path.join(CACHE, "term_frequencies.pkl")
BM25_K1 = 1.5

class InvertedIndex:

    def __init__(self):
        self.index = defaultdict(set) 
    #a dictionary mapping tokens (strings) to sets of document IDs (integers).
        self.docmap = defaultdict() 
    #a dictionary mapping document IDs to their full document objects.
        self.term_frequencies = defaultdict(Counter)
    #a dictionary of document IDs to Counter objects.

    def __add_document(self, doc_id: int, text: str):
        list_text = full_tokenization(text)
        self.term_frequencies[doc_id] = Counter(list_text)
        set_text = set(list_text)
        for token in set_text:
            self.index[token].add(doc_id)


    #Tokenize the input text, then add each token to the index with the document ID.

    def get_documents(self, term: str) -> list:
        result = list(self.index[term])
        return sorted(result)
    #It should get the set of document IDs for a given token, and return them as a list, sorted in ascending order. 

    def build(self):
        full = load_movies()
        for item in full:
            self.docmap[item["id"]] = item
            self.__add_document(item["id"], f"{item["title"]}{item["description"]}")
    #. It should iterate over all the movies and add them to both the index and the docmap.
#When adding the movie data to the index with __add_document(), concatenate the title and the description and use that as the input text. For example:
#f"{m['title']} {m['description']}"

    def save(self):
        os.makedirs(CACHE, exist_ok=True)
        with open(CACHE_INDEX, 'wb') as f:
            pickle.dump(self.index, f)
        with open(CACHE_DOCMAP, 'wb') as f:
            pickle.dump(self.docmap, f)
        with open(CACHE_TERM_FREQUENCIES, 'wb') as f:
            pickle.dump(self.term_frequencies, f)

    #It should save the index and docmap attributes to disk using the pickle module's dump function.
#Use the file path/name cache/index.pkl for the index.
#Use the file path/name cache/docmap.pkl for the docmap.
#Have this method create the cache directory if it doesn't exist (before trying to write files into it).

    def load(self):
        if not os.path.exists(CACHE_INDEX):
            raise Exception("Index file not found")
        if not os.path.exists(CACHE_DOCMAP):
            raise Exception("Docmap file not found") 
        with open(CACHE_INDEX, 'rb') as f:
            self.index = pickle.load(f)
        with open(CACHE_DOCMAP, 'rb') as f:
            self.docmap = pickle.load(f) 
        with open(CACHE_TERM_FREQUENCIES, 'rb') as f:
            self.term_frequencies = pickle.load(f) 

    def get_tf(self, doc_id: int, term: str) -> int:
        token = full_tokenization(term)
        if len(token) > 1:
            raise Exception("get_tf accepts only one token at a time")
        return self.term_frequencies[doc_id][token[0]]
    
    def get_bm25_tf(self, doc_id: int, term: str, k1: float = BM25_K1) -> float:
        tf = self.get_tf(doc_id, term)
        return ((tf * (k1 + 1)) / (tf + k1))        

    def calculate_idf(self, term: str) -> float:
        token = full_tokenization(term)
        doc_count = len(self.docmap)
        term_doc_count = len(self.index[token[0]])
        return math.log((doc_count + 1) / (term_doc_count + 1))

    def get_bm25_idf(self, term: str) -> float:
        token = full_tokenization(term)
        if len(token) > 1:
            print("too many arguments")
            raise Exception
        doc_count = len(self.docmap)
        term_doc_count = len(self.index[token[0]])
        return math.log((doc_count - term_doc_count + 0.5) / (term_doc_count + 0.5) + 1)


def search_index(index: InvertedIndex, query: list) -> list:
    results = set()
    for term in query:
        if len(results) > DEFAULT_SEARCH_LIMIT:
            break
        results.update(index.get_documents(term))
    intermediate = sorted(list(results))
    finals = []
    count = 0
    for i in intermediate:
        finals.append(f"id {i}: {index.docmap[i]["title"]}")
        count += 1
        if count > DEFAULT_SEARCH_LIMIT:
            break
    return finals

def bm25_idf_command(term: str) -> float:
    index = InvertedIndex()
    index.load()
    return index.get_bm25_idf(term)

def bm25_tf_command(doc_id: int, term: str, k1: float = BM25_K1) -> float:
    index = InvertedIndex()
    index.load()
    return index.get_bm25_tf(doc_id, term, k1)