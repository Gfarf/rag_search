#!/usr/bin/env python3

import argparse
from lib.utils import full_tokenization
from lib.inverted_search import InvertedIndex, search_index

MOVIES = "./data/movies.json"

#It should build the inverted index and save it to disk.
#After doing so, it should print a message containing the first ID of the document for the token 'merida' (which should be document 4651, "Brave").

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    subparsers.add_parser("build", help="Build Inverted Index")

    tf_parser = subparsers.add_parser("tf", help="Search term frequencies in doc")
    tf_parser.add_argument("id", type=str, help="doc id")
    tf_parser.add_argument("query", type=str, help="Search query")

    idf_parser = subparsers.add_parser("idf", help="Give idf for term")
    idf_parser.add_argument("term", type=str, help="term which frequency is desired")

    tf_idf_parser = subparsers.add_parser("tfidf", help="Search term frequencies in doc")
    tf_idf_parser.add_argument("id", type=str, help="doc id")
    tf_idf_parser.add_argument("query", type=str, help="Search query")


    args = parser.parse_args()

    match args.command:
        case "search":
            print("Searching for:", args.query)
            index = InvertedIndex()
            index.load()
            tokens = full_tokenization(args.query)
            results = search_index(index, tokens)
            for res in results:
                print(res)
        case "build":
            index = InvertedIndex()
            index.build()
            index.save()
        case "tf":
            print("Searching for term frequency of:", args.query, "in", args.id)
            index = InvertedIndex()
            index.load()
            print(index.get_tf(int(args.id), args.query)) 
        case "idf":
            print("calculatind idf for:", args.term)
            index = InvertedIndex()
            index.load()
            idf = index.calculate_idf(args.term)
            print(f"Inverse document frequency of '{args.term}': {idf:.2f}") 
        case "tfidf":
            print("Calculating tf-idf of:", args.query, "in", args.id)
            index = InvertedIndex()
            index.load()   
            tf_idf = index.calculate_idf(args.query) * index.get_tf(int(args.id), args.query) 
            print(f"TF-IDF score of '{args.query}' in document '{args.id}': {tf_idf:.2f}")     
        case _:
            parser.print_help()

        


if __name__ == "__main__":
    main()