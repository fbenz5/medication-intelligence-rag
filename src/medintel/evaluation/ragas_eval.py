import json
from pathlib import Path

from langchain_openai import ChatOpenAI
from ragas import EvaluationDataset, evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import (
    Faithfulness,
    LLMContextPrecisionWithoutReference,
    LLMContextRecall,
    ResponseRelevancy,
)

from medintel.config import settings

RESULTS_PATH = Path("data/evaluation/rag_results.json")


def load_results() -> list[dict]:
    with RESULTS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_dataset(results: list[dict]) -> EvaluationDataset:
    samples = []

    for result in results:
        samples.append(
            {
                "user_input": result["user_input"],
                "retrieved_contexts": result["retrieved_contexts"],
                "response": result["response"],
                "reference": result["reference"],
            }
        )

    return EvaluationDataset.from_list(samples)


def main() -> None:
    results = load_results()
    dataset = build_dataset(results)

    evaluator_llm = LangchainLLMWrapper(
        ChatOpenAI(
            model=settings.eval_model,
        )
    )

    metrics = [
        LLMContextPrecisionWithoutReference(),
        LLMContextRecall(),
        Faithfulness(),
        ResponseRelevancy(),
    ]

    print(f"Evaluating {len(results)} RAG cases...")
    print(f"Evaluator model: {settings.eval_model}")
    print("Metrics:")

    for metric in metrics:
        print(f"- {metric.name}")

    evaluation_result = evaluate(
        dataset=dataset,
        metrics=metrics,
        llm=evaluator_llm,
    )

    print("\nEvaluation results:")
    print(evaluation_result)


if __name__ == "__main__":
    main()