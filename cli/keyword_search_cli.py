#!/usr/bin/env python3

import argparse
import json

MOVIES = "./data/movies.json"

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            print("Searching for:", args.query)
            pass
        case _:
            parser.print_help()
    with open(MOVIES, "r") as f:
        movies_list = json.load(f)
    result = []
    for movie in movies_list["movies"]:
        if movie["title"].lower().find(args.query.lower()) != -1:
            result.append(movie)
    final = sorted(result, key=lambda d: d["id"])
    for i in range(5):
        print(i + 1, ". ", final[i]["title"])
        


if __name__ == "__main__":
    main()