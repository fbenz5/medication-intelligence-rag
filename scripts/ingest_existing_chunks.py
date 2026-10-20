
from medintel.config import settings
from medintel.embedding.service import EmbeddingService
from medintel.ingestion.chunk_store import load_chunks
from medintel.vectorstore.qdrant import QdrantVectorStore


def main() -> None:
    chunks = load_chunks(settings.data_processed_path / "chunks.jsonl")
    print(f"Loaded {len(chunks)} chunks.")

    embedding_service = EmbeddingService()
    embeddings = embedding_service.embed_documents(
        [chunk.text for chunk in chunks]
    )

    vector_store = QdrantVectorStore()
    vector_store.upsert_chunks(chunks=chunks, embeddings=embeddings)

    print(f"Successfully imported {len(chunks)} chunks into Qdrant Cloud.")


if __name__ == "__main__":
    main()
