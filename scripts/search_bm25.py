from pathlib import Path

from medintel.ingestion.chunk_store import load_chunks
from medintel.retrieval.bm25 import BM25Retriever

CHUNKS_PATH = Path("data/processed/chunks.jsonl")

QUERY = "What are the risks of domperidone?"


def main() -> None:
    chunks = load_chunks(CHUNKS_PATH)

    retriever = BM25Retriever(chunks)

    results = retriever.search(
        query=QUERY,
        limit=5,
    )

    print(f"Query: {QUERY}")
    print(f"Results: {len(results)}")

    for index, (chunk, score) in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print(f"Score: {score:.4f}")
        print(f"Page: {chunk.page_number}")
        print(f"Text: {chunk.text[:500]}")


if __name__ == "__main__":
    main()