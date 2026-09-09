from pathlib import Path

from medintel.ingestion.chunker import chunk_document
from medintel.ingestion.pdf_parser import parse_pdf_file

FILE_PATH = Path("data/documents/has/bon_usage_antiemetiques.pdf")


def main() -> None:
    documents = parse_pdf_file(
        file_path=FILE_PATH,
        source="HAS",
        title="Bon usage des médicaments antiémétiques dans le traitement "
        "symptomatique des nausées et des vomissements",
    )

    for document in documents:
        chunks = chunk_document(document)

        print(
            f"\nPage {document.page_number}: "
            f"{len(chunks)} chunks"
        )

        for chunk in chunks:
            print(
                f"\n--- {chunk.chunk_id} "
                f"({len(chunk.text)} characters) ---"
            )
            print(chunk.text[:500])


if __name__ == "__main__":
    main()