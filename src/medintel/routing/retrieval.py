from pydantic import BaseModel, Field

from medintel.models.chunk import Chunk
from medintel.models.composition import Composition
from medintel.models.medication import Medication
from medintel.models.presentation import Presentation
from medintel.retrieval.hybrid import HybridRetriever
from medintel.routing.intent import QueryIntent
from medintel.routing.query_parser import QueryParser
from medintel.routing.router import RetrievalRoute
from medintel.structured.composition_repository import CompositionRepository
from medintel.structured.presentation_repository import PresentationRepository
from medintel.structured.repository import MedicationRepository


class RetrievalResult(BaseModel):
    intent: QueryIntent
    medications: list[Medication] = Field(default_factory=list)
    presentations: list[Presentation] = Field(default_factory=list)
    compositions: list[Composition] = Field(default_factory=list)
    chunks: list[tuple[Chunk, float]] = Field(default_factory=list)


class RetrievalService:
    def __init__(
        self,
        query_parser: QueryParser,
        medication_repository: MedicationRepository,
        presentation_repository: PresentationRepository,
        composition_repository: CompositionRepository,
        hybrid_retriever: HybridRetriever,
    ) -> None:
        self.query_parser = query_parser
        self.medication_repository = medication_repository
        self.presentation_repository = presentation_repository
        self.composition_repository = composition_repository
        self.hybrid_retriever = hybrid_retriever

    def retrieve(self, query: str) -> RetrievalResult:
        intent = self.query_parser.parse(query)

        medications: list[Medication] = []
        presentations: list[Presentation] = []
        compositions: list[Composition] = []
        chunks: list[tuple[Chunk, float]] = []

        if intent.route in {RetrievalRoute.STRUCTURED, RetrievalRoute.BOTH}:
            if intent.cis:
                medication = self.medication_repository.get_medication(intent.cis)

                if medication:
                    medications.append(medication)

                presentations = self.presentation_repository.get_by_cis(intent.cis)
                compositions = self.composition_repository.get_by_cis(intent.cis)

            elif intent.medication_name:
                medications = self.medication_repository.search_by_name(
                    intent.medication_name
                )

                for medication in medications:
                    presentations.extend(
                        self.presentation_repository.get_by_cis(medication.cis)
                    )
                    compositions.extend(
                        self.composition_repository.get_by_cis(medication.cis)
                    )

        if intent.route in {RetrievalRoute.RAG, RetrievalRoute.BOTH}:
            chunks = self.hybrid_retriever.search(
                query=query,
                limit=5,
            )

        return RetrievalResult(
            intent=intent,
            medications=medications,
            presentations=presentations,
            compositions=compositions,
            chunks=chunks,
        )