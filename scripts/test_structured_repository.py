from pathlib import Path

from medintel.ingestion.chunk_store import load_chunks
from medintel.retrieval.hybrid import HybridRetriever
from medintel.routing.query_parser import QueryParser
from medintel.routing.retrieval import RetrievalService
from medintel.routing.router import QueryRouter
from medintel.structured.composition_loader import load_composition_repository
from medintel.structured.loader import load_medication_repository
from medintel.structured.presentation_loader import load_presentation_repository

CHUNKS_PATH = Path("data/processed/chunks.jsonl")


def main() -> None:
    medication_repository = load_medication_repository()
    presentation_repository = load_presentation_repository()
    composition_repository = load_composition_repository()

    chunks = load_chunks(CHUNKS_PATH)
    hybrid_retriever = HybridRetriever(chunks)

    query_parser = QueryParser(
        router=QueryRouter(),
        repository=medication_repository,
    )

    retrieval_service = RetrievalService(
        query_parser=query_parser,
        medication_repository=medication_repository,
        presentation_repository=presentation_repository,
        composition_repository=composition_repository,
        hybrid_retriever=hybrid_retriever,
    )

    queries = [
        "What is the administrative status of CIS 60002283?",
        "What are the risks of domperidone?",
        "What is the reimbursement rate of domperidone and what are its cardiac risks?",
    ]

    for query in queries:
        result = retrieval_service.retrieve(query)

        print("\n" + "=" * 60)
        print(f"Query: {query}")
        print(f"Route: {result.intent.route.value}")
        print(f"CIS: {result.intent.cis}")
        print(f"Medication: {result.intent.medication_name}")
        print(f"Requested information: {result.intent.requested_information}")

        if result.medications:
            print("\nStructured medications:")

            for medication in result.medications[:3]:
                print(f"- {medication.cis}: {medication.name}")

        if result.presentations:
            print("\nPresentations:")

            for presentation in result.presentations[:5]:
                print(
                    f"- {presentation.cip7}: "
                    f"{presentation.name} | "
                    f"Price: {presentation.price} | "
                    f"Reimbursement: {presentation.reimbursement_rate}"
                )

        if result.compositions:
            print("\nComposition:")

            for composition in result.compositions[:5]:
                print(
                    f"- {composition.substance_name} | "
                    f"Dosage: {composition.dosage} | "
                    f"Element: {composition.pharmaceutical_element}"
                )

        if result.chunks:
            print("\nRAG results:")

            for rank, (chunk, score) in enumerate(result.chunks, start=1):
                print(
                    f"- {rank}. "
                    f"page={chunk.page_number}, "
                    f"score={score:.4f}, "
                    f"chunk={chunk.chunk_id}"
                )


if __name__ == "__main__":
    main()