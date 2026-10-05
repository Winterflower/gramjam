"""Build a trigram index over a file of newline-delimited JSON documents.

Each line of the input file is a JSON object of the form:
    {"id": 1, "content": "some text"}

The resulting index maps every trigram (3-character substring) to a list of
(document id, position) tuples, sorted by document id and then position.
"""

import argparse
import json
import pickle
from collections import defaultdict


def trigrams(text):
    """Return the set of unique trigrams in text and their positions as tuples."""
    return {(text[i:i + 3], i) for i in range(len(text) - 2)}


def read_documents(path):
    """Yield (id, content) pairs from a newline-delimited JSON file."""
    with open(path, encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                doc = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {e}") from e
            yield doc["id"], doc["content"]


def build_index(documents):
    """Build a trigram -> sorted list of document ids dictionary."""
    index = defaultdict(set)
    for doc_id, content in documents:
        for tri, position in trigrams(content):
            index[tri].add((doc_id, position))
    return {tri: sorted(ids) for tri, ids in index.items()}


def main():
    parser = argparse.ArgumentParser(description="Build a trigram index from NDJSON documents.")
    parser.add_argument("--path", required=True, help="Path to newline-delimited JSON file")
    parser.add_argument("--output", default="index.pkl", help="Where to write the pickled index")
    args = parser.parse_args()

    index = build_index(read_documents(args.path))

    with open(args.output, "wb") as f:
        pickle.dump(index, f)

    print(f"Indexed {len(index)} unique trigrams -> {args.output}")
    print(index['fox'])


if __name__ == "__main__":
    main()
