from langchain_text_splitters import RecursiveCharacterTextSplitter

from medintel.models.chunk import Chunk
from medintel.models.document import Document

TARGET_CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def chunk_document_with_langchain(document: Document) -> list[Chunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=TARGET_CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    texts = splitter.split_text(document.text)

    return [
        Chunk(
            chunk_id=f"{document.filename}-p{document.page_number}-lc{index}",
            source=document.source,
            title=document.title,
            filename=document.filename,
            page_number=document.page_number,
            text=text,
        )
        for index, text in enumerate(texts, start=1)
    ]