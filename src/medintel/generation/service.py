import re

from pydantic import BaseModel, Field

from medintel.generation.citation import Citation
from medintel.generation.citation_resolver import CitationResolver
from medintel.generation.context import EvidenceContextBuilder
from medintel.generation.llm import GeneratedAnswer, LLMGenerator
from medintel.routing.retrieval import RetrievalService


class GeneratedResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    evidence_sufficient: bool


class GenerationService:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        context_builder: EvidenceContextBuilder,
        llm_generator: LLMGenerator,
        citation_resolver: CitationResolver,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.context_builder = context_builder
        self.llm_generator = llm_generator
        self.citation_resolver = citation_resolver

    def answer(self, query: str) -> GeneratedResponse:
        retrieval_result = self.retrieval_service.retrieve(query)

        evidence_context = self.context_builder.build(
            query=query,
            result=retrieval_result,
        )

        generated_answer: GeneratedAnswer = self.llm_generator.generate(
            evidence_context
        )

        citations = self.citation_resolver.resolve(
            evidence_ids=generated_answer.citations,
            context=evidence_context,
        )

        citation_numbers = {
            citation.evidence_id: index
            for index, citation in enumerate(citations, start=1)
        }

        answer = self._replace_citation_ids(
            answer=generated_answer.answer,
            citation_numbers=citation_numbers,
        )

        return GeneratedResponse(
            answer=answer,
            citations=citations,
            evidence_sufficient=generated_answer.evidence_sufficient,
        )

    @staticmethod
    def _replace_citation_ids(
        answer: str,
        citation_numbers: dict[str, int],
    ) -> str:
        def replace(match: re.Match[str]) -> str:
            evidence_id = match.group(1)
            number = citation_numbers.get(evidence_id)

            if number is None:
                return match.group(0)

            return f"[{number}]"

        return re.sub(
            r"\[([^\]]+)\]",
            replace,
            answer,
        )