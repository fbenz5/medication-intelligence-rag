from medintel.models.chunk import Chunk
from medintel.models.document import Document

TARGET_CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def chunk_document(document: Document) -> list[Chunk]:
    paragraphs = [
        paragraph.strip()
        for paragraph in document.text.split("\n\n")
        if paragraph.strip()
    ]

    chunks: list[Chunk] = []
    current_text = ""

    for paragraph in paragraphs:
        if len(paragraph) > TARGET_CHUNK_SIZE:
            if current_text:
                chunks.append(
                    _create_chunk(
                        document=document,
                        chunk_number=len(chunks) + 1,
                        text=current_text,
                    )
                )
                current_text = ""

            chunks.extend(
                _split_large_paragraph(
                    document=document,
                    paragraph=paragraph,
                    start_chunk_number=len(chunks) + 1,
                )
            )
            continue

        candidate = (
            f"{current_text}\n\n{paragraph}"
            if current_text
            else paragraph
        )

        if len(candidate) > TARGET_CHUNK_SIZE and current_text:
            chunks.append(
                _create_chunk(
                    document=document,
                    chunk_number=len(chunks) + 1,
                    text=current_text,
                )
            )

            overlap = current_text[-CHUNK_OVERLAP:]
            current_text = f"{overlap}\n\n{paragraph}"
        else:
            current_text = candidate

    if current_text:
        chunks.append(
            _create_chunk(
                document=document,
                chunk_number=len(chunks) + 1,
                text=current_text,
            )
        )

    return chunks


def _split_large_paragraph(
    document: Document,
    paragraph: str,
    start_chunk_number: int,
) -> list[Chunk]:
    chunks: list[Chunk] = []
    start = 0
    chunk_number = start_chunk_number

    while start < len(paragraph):
        end = min(start + TARGET_CHUNK_SIZE, len(paragraph))
        text = paragraph[start:end].strip()

        chunks.append(
            _create_chunk(
                document=document,
                chunk_number=chunk_number,
                text=text,
            )
        )

        chunk_number += 1

        if end == len(paragraph):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def _create_chunk(
    document: Document,
    chunk_number: int,
    text: str,
) -> Chunk:
    return Chunk(
        chunk_id=f"{document.filename}-p{document.page_number}-c{chunk_number}",
        source=document.source,
        title=document.title,
        filename=document.filename,
        page_number=document.page_number,
        text=text,
    )