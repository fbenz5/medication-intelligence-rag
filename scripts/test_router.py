from medintel.routing.router import QueryRouter


def main() -> None:
    router = QueryRouter()

    queries = [
        "What is the administrative status of CIS 60002283?",
        "What are the risks of domperidone?",
        "What is the reimbursement rate and what are the cardiac risks?",
        "Tell me about this medication.",
    ]

    for query in queries:
        route = router.route(query)

        print(f"\nQuery: {query}")
        print(f"Route: {route.value}")


if __name__ == "__main__":
    main()