from pathlib import Path

from medintel.embedding.service import EmbeddingService
from medintel.ingestion.chunk_store import load_chunks
from medintel.retrieval.bm25 import BM25Retriever
from medintel.retrieval.rrf import reciprocal_rank_fusion
from medintel.vectorstore.qdrant import QdrantVectorStore

CHUNKS_PATH = Path("data/processed/chunks.jsonl")

QUERY = "What are the risks of domperidone?"


def main() -> None:
    chunks = load_chunks(CHUNKS_PATH)

    embedding_service = EmbeddingService()
    vector_store = QdrantVectorStore()

    # Dense retrieval
    query_vector = embedding_service.embed_text(QUERY)

    dense_results = vector_store.search(
        query_vector=query_vector,
        limit=5,
    )

    dense_chunks = [
        chunks_by_id[point.payload["chunk_id"]]
        for point in dense_results
    ]

    # BM25 retrieval
    bm25_retriever = BM25Retriever(chunks)

    bm25_results = bm25_retriever.search(
        query=QUERY,
        limit=5,
    )

    bm25_chunks = [
        chunk
        for chunk, _score in bm25_results
    ]

    # RRF
    fused_results = reciprocal_rank_fusion(
        ranked_results=[
            dense_chunks,
            bm25_chunks,
        ],
        limit=5,
    )

    print(f"Query: {QUERY}")

    print("\n=== Dense retrieval ===")
    for rank, chunk in enumerate(dense_chunks, start=1):
        print(
            f"{rank}. Page {chunk.page_number} "
            f"| {chunk.chunk_id}"
        )

    print("\n=== BM25 retrieval ===")
    for rank, chunk in enumerate(bm25_chunks, start=1):
        print(
            f"{rank}. Page {chunk.page_number} "
            f"| {chunk.chunk_id}"
        )

    print("\n=== RRF ===")
    for rank, (chunk, score) in enumerate(fused_results, start=1):
        print(
            f"{rank}. Score {score:.6f} "
            f"| Page {chunk.page_number} "
            f"| {chunk.chunk_id}"
        )


if __name__ == "__main__":
    chunks_by_id = {
        chunk.chunk_id: chunk
        for chunk in load_chunks(CHUNKS_PATH)
    }

    main()