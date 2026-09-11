from pathlib import Path

from medintel.ingestion.chunk_store import load_chunks
from medintel.retrieval.hybrid import HybridRetriever

CHUNKS_PATH = Path("data/processed/chunks.jsonl")
QUERY = "What are the risks of domperidone?"


def main() -> None:
    chunks = load_chunks(CHUNKS_PATH)

    retriever = HybridRetriever(chunks)

    results = retriever.search(
        query=QUERY,
        limit=5,
    )

    print(f"Query: {QUERY}")
    print(f"Results: {len(results)}")

    for rank, (chunk, score) in enumerate(results, start=1):
        print(f"\n--- Result {rank} ---")
        print(f"Reranker score: {score:.4f}")
        print(f"Page: {chunk.page_number}")
        print(f"Chunk: {chunk.chunk_id}")
        print(f"Text: {chunk.text[:500]}")


if __name__ == "__main__":
    main()