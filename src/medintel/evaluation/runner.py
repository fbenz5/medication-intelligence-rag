import json
from pathlib import Path

from medintel.app import build_generation_service
from medintel.generation.context import EvidenceContextBuilder

DATASET_PATH = Path("data/evaluation/rag_dataset.json")
OUTPUT_PATH = Path("data/evaluation/rag_results.json")


def load_questions() -> list[dict]:
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def run_evaluation() -> None:
    questions = load_questions()

    generation_service = build_generation_service()
    context_builder = EvidenceContextBuilder()

    results: list[dict] = []

    for index, item in enumerate(questions, start=1):
        query = item["user_input"]

        print(f"\n[{index}/{len(questions)}] {query}")

        retrieval_result = generation_service.retrieval_service.retrieve(query)

        evidence_context = context_builder.build(
            query=query,
            result=retrieval_result,
        )

        generated_answer = generation_service.llm_generator.generate(
            evidence_context
        )

        retrieved_contexts = [
            chunk.text
            for chunk, _score in retrieval_result.chunks
        ]

        results.append(
            {
                "user_input": query,
                "reference": item["reference"],
                "reference_contexts": item["reference_contexts"],
                "retrieved_contexts": retrieved_contexts,
                "response": generated_answer.answer,
                "citations": generated_answer.citations,
                "evidence_sufficient": generated_answer.evidence_sufficient,
            }
        )

        print(f"Answer: {generated_answer.answer}")
        print(f"Citations: {generated_answer.citations}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    print(f"\nEvaluation results saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    run_evaluation()