from medintel.generation.citation_resolver import CitationResolver
from medintel.generation.context import EvidenceContextBuilder
from medintel.generation.llm import GeneratedAnswer
from medintel.generation.service import GenerationService
from medintel.models.chunk import Chunk
from medintel.routing.intent import QueryIntent
from medintel.routing.retrieval import RetrievalResult
from medintel.routing.router import RetrievalRoute


class FakeRetrievalService:
    def retrieve(self, query: str) -> RetrievalResult:
        return RetrievalResult(
            intent=QueryIntent(
                route=RetrievalRoute.RAG,
            ),
            chunks=[
                (
                    Chunk(
                        chunk_id="chunk-1",
                        source="HAS",
                        title="Test document",
                        filename="test.pdf",
                        page_number=1,
                        text="Test evidence.",
                    ),
                    1.0,
                )
            ],
        )


class FakeLLMGenerator:
    def generate(self, context):
        return GeneratedAnswer(
            answer="Test answer.",
            citations=["chunk-1"],
            evidence_sufficient=True,
        )


def test_generation_service_connects_retrieval_context_and_llm() -> None:
    service = GenerationService(
        retrieval_service=FakeRetrievalService(),
        context_builder=EvidenceContextBuilder(),
        llm_generator=FakeLLMGenerator(),
        citation_resolver=CitationResolver(),
    )

    result = service.answer("Test question")

    assert result.answer == "Test answer."
    assert len(result.citations) == 1
    assert result.citations[0].evidence_id == "chunk-1"
    assert result.citations[0].source == "HAS"
    assert result.evidence_sufficient is True