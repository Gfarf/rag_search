#!/usr/bin/env python3

import argparse
from lib.utils import full_tokenization
from lib.inverted_search import InvertedIndex, search_index, bm25_idf_command, BM25_K1, bm25_tf_command

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

    bm25_idf_parser = subparsers.add_parser('bm25idf', help="Get BM25 IDF score for a given term")
    bm25_idf_parser.add_argument("term", type=str, help="Term to get BM25 IDF score for")

    bm25_tf_parser = subparsers.add_parser(
    "bm25tf", help="Get BM25 TF score for a given document ID and term"
    )
    bm25_tf_parser.add_argument("doc_id", type=int, help="Document ID")
    bm25_tf_parser.add_argument("term", type=str, help="Term to get BM25 TF score for")
    bm25_tf_parser.add_argument("k1", type=float, nargs='?', default=BM25_K1, help="Tunable BM25 K1 parameter")

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
        case "bm25idf":
            bm25idf = bm25_idf_command(args.term)
            print(f"BM25 IDF score of '{args.term}': {bm25idf:.2f}")
        case "bm25tf":
            bm25tf = bm25_tf_command(args.doc_id, args.term, args.k1)
            print(f"BM25 TF score of '{args.term}' in document '{args.doc_id}': {bm25tf:.2f}")
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