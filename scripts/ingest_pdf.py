from pathlib import Path

from medintel.embedding.service import EmbeddingService
from medintel.ingestion.langchain_chunker import (
    chunk_document_with_langchain,
)
from medintel.ingestion.pdf_parser import parse_pdf_file
from medintel.vectorstore.qdrant import QdrantVectorStore


FILE_PATH = Path("data/documents/has/bon_usage_antiemetiques.pdf")

TITLE = (
    "Bon usage des médicaments antiémétiques dans le traitement "
    "symptomatique des nausées et des vomissements"
)


def main() -> None:
    documents = parse_pdf_file(
        file_path=FILE_PATH,
        source="HAS",
        title=TITLE,
    )

    chunks = [
        chunk
        for document in documents
        for chunk in chunk_document_with_langchain(document)
    ]

    print(f"Documents: {len(documents)}")
    print(f"Chunks: {len(chunks)}")

    embedding_service = EmbeddingService()

    embeddings = embedding_service.embed_documents(
        [chunk.text for chunk in chunks]
    )

    print(f"Embeddings: {len(embeddings)}")
    print(f"Embedding dimension: {len(embeddings[0])}")

    vector_store = QdrantVectorStore()

    vector_store.upsert_chunks(
        chunks=chunks,
        embeddings=embeddings,
    )

    print("Chunks successfully stored in Qdrant.")


if __name__ == "__main__":
    main()