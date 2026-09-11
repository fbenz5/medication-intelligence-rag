from pathlib import Path

from medintel.ingestion.chunk_store import load_chunks
from medintel.retrieval.hybrid import HybridRetriever
from medintel.routing.query_parser import QueryParser
from medintel.routing.retrieval import RetrievalService
from medintel.routing.router import QueryRouter
from medintel.structured.loader import load_medication_repository

CHUNKS_PATH = Path("data/processed/chunks.jsonl")


def main() -> None:
    repository = load_medication_repository()
    chunks = load_chunks(CHUNKS_PATH)
    hybrid_retriever = HybridRetriever(chunks)

    query_parser = QueryParser(
        router=QueryRouter(),
        repository=repository,
    )

    retrieval_service = RetrievalService(
        query_parser=query_parser,
        repository=repository,
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
        print(
            f"Requested information: "
            f"{result.intent.requested_information}"
        )

        if result.medications:
            print("\nStructured results:")
            for medication in result.medications[:3]:
                print(f"- {medication.cis}: {medication.name}")

        if result.chunks:
            print("\nRAG results:")
            for rank, (chunk, score) in enumerate(
                result.chunks,
                start=1,
            ):
                print(
                    f"- {rank}. "
                    f"page={chunk.page_number}, "
                    f"score={score:.4f}, "
                    f"chunk={chunk.chunk_id}"
                )


if __name__ == "__main__":
    main()