import json
import math
import sys
from pathlib import Path

from langchain_openai import ChatOpenAI
from ragas import EvaluationDataset, evaluate
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import (
    Faithfulness,
    LLMContextPrecisionWithoutReference,
    LLMContextRecall,
    ResponseRelevancy,
)

from medintel.config import settings
from medintel.embedding.service import EmbeddingService

RESULTS_PATH = Path("data/evaluation/rag_results.json")

QUALITY_THRESHOLDS = {
    "llm_context_precision_without_reference": 0.90,
    "context_recall": 0.85,
    "faithfulness": 0.90,
    "answer_relevancy": 0.90,
}


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
            api_key=settings.openai_api_key,
        )
    )

    embedding_service = EmbeddingService()
    evaluator_embeddings = LangchainEmbeddingsWrapper(
        embedding_service._embeddings,
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
        embeddings=evaluator_embeddings,
    )

    print("\nEvaluation results:")
    print(evaluation_result)

    scores = (
        evaluation_result
        .to_pandas()
        .mean(numeric_only=True)
        .to_dict()
    )

    print("\nQuality gate:")

    quality_gate_passed = True
    evaluation_completed = True

    for metric_name, threshold in QUALITY_THRESHOLDS.items():
        score = scores.get(metric_name)

        if score is None or math.isnan(score):
            print(f"- {metric_name}: NO VALID SCORE → EVALUATION FAILED")
            evaluation_completed = False
            continue

        status = "PASS" if score >= threshold else "FAIL"

        print(
            f"- {metric_name}: "
            f"{score:.4f} >= {threshold:.2f} → {status}"
        )

        if score < threshold:
            quality_gate_passed = False

    if not evaluation_completed:
        print("\nQUALITY GATE: EVALUATION FAILED")
        sys.exit(2)

    if quality_gate_passed:
        print("\nQUALITY GATE: PASSED")
        return

    print("\nQUALITY GATE: FAILED")
    sys.exit(1)


if __name__ == "__main__":
    main()