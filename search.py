"""Look up documents in a pickled trigram index built by index.py.

For now the query must be exactly one trigram (3 characters).
"""

import argparse
import pickle
import sys


def load_index(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def search(index, query):
    """Return the sorted list of document ids containing the trigram query."""
    if len(query) != 3:
        raise ValueError(f"query must be exactly 3 characters, got {len(query)}: {query!r}")
    return index.get(query, [])


def main():
    parser = argparse.ArgumentParser(description="Search a trigram index.")
    parser.add_argument("--query", required=True, help="Trigram to search for, e.g. 'abc'")
    parser.add_argument("--index", default="index.pkl", help="Path to the pickled index")
    args = parser.parse_args()

    index = load_index(args.index)

    try:
        doc_ids = search(index, args.query)
    except ValueError as e:
        sys.exit(f"error: {e}")

    if doc_ids:
        print(f"{args.query!r} found in {len(doc_ids)} document(s): {doc_ids}")
    else:
        print(f"{args.query!r} not found")


if __name__ == "__main__":
    main()
