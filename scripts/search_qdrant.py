from medintel.embedding.service import EmbeddingService
from medintel.vectorstore.qdrant import QdrantVectorStore

QUERY = "What medications are recommended for nausea and vomiting?"


def main() -> None:
    embedding_service = EmbeddingService()
    vector_store = QdrantVectorStore()

    query_vector = embedding_service.embed_text(QUERY)

    results = vector_store.search(
        query_vector=query_vector,
        limit=5,
    )

    print(f"\nQuery: {QUERY}\n")

    for rank, result in enumerate(results, start=1):
        print(f"--- Result {rank} ---")
        print(f"Score: {result.score:.4f}")
        print(f"Source: {result.payload['source']}")
        print(f"Page: {result.payload['page_number']}")
        print(f"Chunk: {result.payload['chunk_id']}")
        print(f"\n{result.payload['text'][:500]}")
        print()


if __name__ == "__main__":
    main()