from pathlib import Path

from medintel.generation.context import EvidenceContextBuilder
from medintel.generation.llm import LLMGenerator
from medintel.generation.service import GenerationService
from medintel.ingestion.chunk_store import load_chunks
from medintel.retrieval.hybrid import HybridRetriever
from medintel.routing.query_parser import QueryParser
from medintel.routing.retrieval import RetrievalService
from medintel.routing.router import QueryRouter
from medintel.structured.composition_loader import load_composition_repository
from medintel.structured.loader import load_medication_repository
from medintel.structured.presentation_loader import load_presentation_repository

PROCESSED_DATA_PATH = Path("data/processed")


def build_generation_service() -> GenerationService:
    chunks = load_chunks(PROCESSED_DATA_PATH / "chunks.jsonl")

    medication_repository = load_medication_repository()
    presentation_repository = load_presentation_repository()
    composition_repository = load_composition_repository()

    query_router = QueryRouter()

    query_parser = QueryParser(
        router=query_router,
        repository=medication_repository,
    )

    hybrid_retriever = HybridRetriever(chunks)

    retrieval_service = RetrievalService(
        query_parser=query_parser,
        medication_repository=medication_repository,
        presentation_repository=presentation_repository,
        composition_repository=composition_repository,
        hybrid_retriever=hybrid_retriever,
    )

    context_builder = EvidenceContextBuilder()
    llm_generator = LLMGenerator()

    return GenerationService(
        retrieval_service=retrieval_service,
        context_builder=context_builder,
        llm_generator=llm_generator,
    )