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
                requested_information="risks",
            ),
            chunks=[
                (
                    Chunk(
                        chunk_id="chunk-1",
                        source="HAS",
                        title="Medication safety guidance",
                        filename="guidance.pdf",
                        page_number=2,
                        text=(
                            "The medicine is associated with an increased "
                            "risk of arrhythmia."
                        ),
                    ),
                    0.95,
                )
            ],
        )


class FakeLLMGenerator:
    def generate(self, context) -> GeneratedAnswer:
        assert context.query == "What are the cardiac risks?"
        assert len(context.evidences) == 1
        assert context.evidences[0].evidence_id == "chunk-1"

        return GeneratedAnswer(
            answer=(
                "The medicine is associated with an increased "
                "risk of arrhythmia."
            ),
            citations=["chunk-1"],
            evidence_sufficient=True,
        )


def test_generation_service_connects_retrieval_context_and_llm() -> None:
    service = GenerationService(
        retrieval_service=FakeRetrievalService(),
        context_builder=EvidenceContextBuilder(),
        llm_generator=FakeLLMGenerator(),
    )

    result = service.answer("What are the cardiac risks?")

    assert result.answer == (
        "The medicine is associated with an increased "
        "risk of arrhythmia."
    )
    assert result.citations == ["chunk-1"]
    assert result.evidence_sufficient is True