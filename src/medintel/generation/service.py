from medintel.generation.context import EvidenceContextBuilder
from medintel.generation.llm import GeneratedAnswer, LLMGenerator
from medintel.routing.retrieval import RetrievalService


class GenerationService:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        context_builder: EvidenceContextBuilder,
        llm_generator: LLMGenerator,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.context_builder = context_builder
        self.llm_generator = llm_generator

    def answer(self, query: str) -> GeneratedAnswer:
        retrieval_result = self.retrieval_service.retrieve(query)

        evidence_context = self.context_builder.build(
            query=query,
            result=retrieval_result,
        )

        return self.llm_generator.generate(evidence_context)