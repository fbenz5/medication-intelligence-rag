from medintel.ingestion.langchain_chunker import chunk_document_with_langchain
from medintel.models.document import Document


def test_langchain_chunker_respects_chunk_size() -> None:
    document = Document(
        source="HAS",
        title="Test document",
        filename="test.pdf",
        page_number=1,
        text="This is a sentence. " * 100,
    )

    chunks = chunk_document_with_langchain(document)

    assert len(chunks) > 1
    assert all(len(chunk.text) <= 1000 for chunk in chunks)


def test_langchain_chunker_preserves_document_metadata() -> None:
    document = Document(
        source="HAS",
        title="Test document",
        filename="test.pdf",
        page_number=3,
        text="This is a medical document.",
    )

    chunks = chunk_document_with_langchain(document)

    assert len(chunks) == 1

    chunk = chunks[0]

    assert chunk.source == "HAS"
    assert chunk.title == "Test document"
    assert chunk.filename == "test.pdf"
    assert chunk.page_number == 3


def test_langchain_chunker_generates_unique_chunk_ids() -> None:
    document = Document(
        source="HAS",
        title="Test document",
        filename="test.pdf",
        page_number=1,
        text="This is a sentence. " * 100,
    )

    chunks = chunk_document_with_langchain(document)

    chunk_ids = [chunk.chunk_id for chunk in chunks]

    assert len(chunk_ids) == len(set(chunk_ids))