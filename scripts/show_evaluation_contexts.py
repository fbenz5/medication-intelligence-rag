import json
from pathlib import Path

RESULTS_PATH = Path("data/evaluation/rag_results.json")


def main() -> None:
    with RESULTS_PATH.open("r", encoding="utf-8") as file:
        results = json.load(file)

    for index, result in enumerate(results, start=1):
        print(f"\n{'=' * 80}")
        print(f"CASE {index}")
        print(f"{'=' * 80}")
        print(f"QUESTION: {result['user_input']}\n")

        for context_index, context in enumerate(
            result["retrieved_contexts"],
            start=1,
        ):
            print(f"--- CONTEXT {context_index} ---")
            print(context)
            print()


if __name__ == "__main__":
    main()