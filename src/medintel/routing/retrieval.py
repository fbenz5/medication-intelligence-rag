from medintel.models.chunk import Chunk
from medintel.models.medication import Medication
from medintel.retrieval.hybrid import HybridRetriever
from medintel.routing.intent import QueryIntent
from medintel.routing.query_parser import QueryParser
from medintel.routing.router import RetrievalRoute
from medintel.structured.repository import MedicationRepository


class RetrievalResult:
    def __init__(
        self,
        intent: QueryIntent,
        medications: list[Medication] | None = None,
        chunks: list[tuple[Chunk, float]] | None = None,
    ) -> None:
        self.intent = intent
        self.medications = medications or []
        self.chunks = chunks or []


class RetrievalService:
    def __init__(
        self,
        query_parser: QueryParser,
        repository: MedicationRepository,
        hybrid_retriever: HybridRetriever,
    ) -> None:
        self.query_parser = query_parser
        self.repository = repository
        self.hybrid_retriever = hybrid_retriever

    def retrieve(self, query: str) -> RetrievalResult:
        intent = self.query_parser.parse(query)

        medications: list[Medication] = []
        chunks: list[tuple[Chunk, float]] = []

        if intent.route in {
            RetrievalRoute.STRUCTURED,
            RetrievalRoute.BOTH,
        }:
            if intent.cis:
                medication = self.repository.get_medication(intent.cis)

                if medication:
                    medications.append(medication)

            elif intent.medication_name:
                medications = self.repository.search_by_name(
                    intent.medication_name
                )

        if intent.route in {
            RetrievalRoute.RAG,
            RetrievalRoute.BOTH,
        }:
            chunks = self.hybrid_retriever.search(
                query=query,
                limit=5,
            )

        return RetrievalResult(
            intent=intent,
            medications=medications,
            chunks=chunks,
        )