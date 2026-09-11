from pathlib import Path

from medintel.embedding.service import EmbeddingService
from medintel.ingestion.langchain_chunker import chunk_document_with_langchain
from medintel.ingestion.pdf_parser import parse_pdf_file

FILE_PATH = Path("data/documents/has/bon_usage_antiemetiques.pdf")


def main() -> None:
    documents = parse_pdf_file(
        file_path=FILE_PATH,
        source="HAS",
        title=(
            "Bon usage des médicaments antiémétiques dans le traitement "
            "symptomatique des nausées et des vomissements"
        ),
    )

    chunks = chunk_document_with_langchain(documents[0])

    embedding_service = EmbeddingService()

    vector = embedding_service.embed_text(chunks[0].text)

    print(f"Chunk length: {len(chunks[0].text)}")
    print(f"Embedding dimension: {len(vector)}")
    print(f"First 5 values: {vector[:5]}")


if __name__ == "__main__":
    main()