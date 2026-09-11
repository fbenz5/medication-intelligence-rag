from medintel.routing.query_parser import QueryParser
from medintel.routing.router import QueryRouter


def main() -> None:
    parser = QueryParser(QueryRouter())

    queries = [
        "What is the administrative status of CIS 60002283?",
        "What are the risks of domperidone?",
        "What is the reimbursement rate of CIS 60002283?",
    ]

    for query in queries:
        intent = parser.parse(query)

        print(f"\nQuery: {query}")
        print(f"Route: {intent.route.value}")
        print(f"CIS: {intent.cis}")
        print(f"Medication: {intent.medication_name}")
        print(f"Information: {intent.requested_information}")


if __name__ == "__main__":
    main()