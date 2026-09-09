from pathlib import Path

from medintel.ingestion.chunker import chunk_document
from medintel.ingestion.langchain_chunker import (
    chunk_document_with_langchain,
)
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

    for document in documents:
        custom_chunks = chunk_document(document)
        langchain_chunks = chunk_document_with_langchain(document)

        print(f"\n{'=' * 70}")
        print(f"PAGE {document.page_number}")
        print(f"{'=' * 70}")

        print(f"\nCustom chunker: {len(custom_chunks)} chunks")
        for chunk in custom_chunks:
            print(
                f"\n--- {chunk.chunk_id} "
                f"({len(chunk.text)} characters) ---"
            )
            print(chunk.text[:300])

        print(f"\nLangChain: {len(langchain_chunks)} chunks")
        for chunk in langchain_chunks:
            print(
                f"\n--- {chunk.chunk_id} "
                f"({len(chunk.text)} characters) ---"
            )
            print(chunk.text[:300])


if __name__ == "__main__":
    main()