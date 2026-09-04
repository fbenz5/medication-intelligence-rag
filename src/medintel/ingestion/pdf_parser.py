from pathlib import Path

import pymupdf

from medintel.ingestion.document_cleaner import clean_text
from medintel.models.document import Document


def parse_pdf_file(
    file_path: Path,
    source: str,
    title: str,
) -> list[Document]:
    documents: list[Document] = []

    with pymupdf.open(file_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            text = clean_text(page.get_text("text"))

            if not text:
                continue

            documents.append(
                Document(
                    source=source,
                    title=title,
                    filename=file_path.name,
                    page_number=page_number,
                    text=text,
                )
            )

    return documents