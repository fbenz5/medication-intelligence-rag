from pathlib import Path

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

    print(f"Pages extracted: {len(documents)}")

    for document in documents[:2]:
        print(f"\n--- Page {document.page_number} ---")
        print(document.text[:1000])


if __name__ == "__main__":
    main()