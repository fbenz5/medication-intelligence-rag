from pathlib import Path

from medintel.ingestion.chunk_store import load_chunks
from medintel.retrieval.hybrid import HybridRetriever
from medintel.routing.query_parser import QueryParser
from medintel.routing.retrieval import RetrievalService
from medintel.routing.router import QueryRouter, RetrievalRoute
from medintel.structured.composition_loader import load_composition_repository
from medintel.structured.loader import load_medication_repository
from medintel.structured.presentation_loader import load_presentation_repository

CHUNKS_PATH = Path("data/processed/chunks.jsonl")


def build_retrieval_service() -> RetrievalService:
    medication_repository = load_medication_repository()
    presentation_repository = load_presentation_repository()
    composition_repository = load_composition_repository()

    chunks = load_chunks(CHUNKS_PATH)
    hybrid_retriever = HybridRetriever(chunks)

    query_parser = QueryParser(
        router=QueryRouter(),
        repository=medication_repository,
    )

    return RetrievalService(
        query_parser=query_parser,
        medication_repository=medication_repository,
        presentation_repository=presentation_repository,
        composition_repository=composition_repository,
        hybrid_retriever=hybrid_retriever,
    )


def test_structured_retrieval() -> None:
    service = build_retrieval_service()

    result = service.retrieve(
        "What is the administrative status of CIS 60002283?"
    )

    assert result.intent.route == RetrievalRoute.STRUCTURED
    assert result.intent.cis == "60002283"

    assert len(result.medications) == 1
    assert result.medications[0].cis == "60002283"

    assert len(result.presentations) == 2
    assert len(result.compositions) >= 1

    assert result.chunks == []


def test_rag_retrieval() -> None:
    service = build_retrieval_service()

    result = service.retrieve("What are the risks of domperidone?")

    assert result.intent.route == RetrievalRoute.RAG
    assert result.intent.medication_name == "domperidone"

    assert result.medications == []
    assert result.presentations == []
    assert result.compositions == []

    assert len(result.chunks) > 0


def test_both_retrieval() -> None:
    service = build_retrieval_service()

    result = service.retrieve(
        "What is the reimbursement rate of domperidone "
        "and what are its cardiac risks?"
    )

    assert result.intent.route == RetrievalRoute.BOTH
    assert result.intent.medication_name == "domperidone"
    assert result.intent.requested_information == "reimbursement, risks"

    assert len(result.medications) > 0
    assert len(result.presentations) > 0
    assert len(result.compositions) > 0
    assert len(result.chunks) > 0