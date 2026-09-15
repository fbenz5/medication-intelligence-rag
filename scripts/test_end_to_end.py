from time import perf_counter

from medintel.app import build_generation_service


def main() -> None:
    total_start = perf_counter()

    service = build_generation_service()
    initialization_time = perf_counter() - total_start

    query = "What are the cardiac risks associated with antiemetic medications?"

    print(f"\nQuestion:\n{query}\n")
    print(f"Service initialization: {initialization_time:.2f}s")

    retrieval_start = perf_counter()

    retrieval_result = service.retrieval_service.retrieve(query)

    retrieval_time = perf_counter() - retrieval_start

    print(f"Retrieval: {retrieval_time:.2f}s")
    print(f"  Structured medications: {len(retrieval_result.medications)}")
    print(f"  Presentations: {len(retrieval_result.presentations)}")
    print(f"  Compositions: {len(retrieval_result.compositions)}")
    print(f"  Retrieved chunks: {len(retrieval_result.chunks)}")

    context_start = perf_counter()

    evidence_context = service.context_builder.build(
        query=query,
        result=retrieval_result,
    )

    context_time = perf_counter() - context_start

    print(f"Context construction: {context_time:.2f}s")
    print(f"  Evidence items: {len(evidence_context.evidences)}")

    generation_start = perf_counter()

    result = service.llm_generator.generate(evidence_context)

    generation_time = perf_counter() - generation_start
    total_time = perf_counter() - total_start

    print(f"LLM generation: {generation_time:.2f}s")
    print(f"Total: {total_time:.2f}s")

    print("\nAnswer:")
    print(result.answer)

    print("\nCitations:")
    for citation in result.citations:
        print(f"- {citation}")

    print(f"\nEvidence sufficient: {result.evidence_sufficient}")


if __name__ == "__main__":
    main()