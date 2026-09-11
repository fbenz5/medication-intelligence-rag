from enum import StrEnum


class RetrievalRoute(StrEnum):
    STRUCTURED = "structured"
    RAG = "rag"
    BOTH = "both"


class QueryRouter:
    STRUCTURED_KEYWORDS = {
        "cis",
        "cip",
        "reimbursement",
        "price",
        "commercialized",
        "commercialization",
        "administrative status",
        "pharmaceutical form",
        "authorization",
        "composition",
        "active substance",
    }

    RAG_KEYWORDS = {
        "risk",
        "risks",
        "adverse effect",
        "adverse effects",
        "side effect",
        "side effects",
        "contraindication",
        "contraindications",
        "interaction",
        "interactions",
        "efficacy",
        "recommendation",
        "recommendations",
        "symptom",
        "symptoms",
        "clinical",
    }

    def route(self, query: str) -> RetrievalRoute:
        normalized_query = query.lower()

        structured = any(
            keyword in normalized_query
            for keyword in self.STRUCTURED_KEYWORDS
        )

        rag = any(
            keyword in normalized_query
            for keyword in self.RAG_KEYWORDS
        )

        if structured and rag:
            return RetrievalRoute.BOTH

        if structured:
            return RetrievalRoute.STRUCTURED

        return RetrievalRoute.RAG