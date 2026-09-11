import re

from medintel.routing.intent import QueryIntent
from medintel.routing.router import QueryRouter
from medintel.structured.repository import MedicationRepository

CIS_PATTERN = re.compile(r"\b(?:cis\s*)?(\d{8})\b", re.IGNORECASE)

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "at",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "what",
    "which",
    "with",
}

INFORMATION_PATTERNS = {
    "administrative status": [
        "administrative status",
        "administrative state",
    ],
    "commercialization status": [
        "commercialization status",
        "commercialization",
        "commercialized",
    ],
    "reimbursement": [
        "reimbursement rate",
        "reimbursement",
    ],
    "price": [
        "public price",
        "price",
    ],
    "composition": [
        "composition",
        "active substance",
        "active ingredient",
    ],
    "risks": [
        "cardiac risks",
        "cardiac risk",
        "risks",
        "risk",
    ],
    "adverse effects": [
        "adverse effects",
        "adverse effect",
        "side effects",
        "side effect",
    ],
    "contraindications": [
        "contraindications",
        "contraindication",
    ],
    "interactions": [
        "drug interactions",
        "drug interaction",
        "interactions",
        "interaction",
    ],
    "efficacy": [
        "efficacy",
    ],
    "recommendations": [
        "recommendations",
        "recommendation",
    ],
}


class QueryParser:
    def __init__(
        self,
        router: QueryRouter,
        repository: MedicationRepository,
    ) -> None:
        self.router = router
        self.repository = repository

    def parse(self, query: str) -> QueryIntent:
        route = self.router.route(query)

        cis_match = CIS_PATTERN.search(query)
        cis = cis_match.group(1) if cis_match else None

        medication_name = None

        if cis is None:
            medication_name = self._find_medication_name(query)

        requested_information = self._find_requested_information(query)

        return QueryIntent(
            route=route,
            cis=cis,
            medication_name=medication_name,
            requested_information=requested_information,
        )

    def _find_medication_name(self, query: str) -> str | None:
        query_tokens = {
            token
            for token in re.findall(
                r"\b[a-zA-ZÀ-ÿ0-9-]+\b",
                query.lower(),
            )
            if token not in STOP_WORDS and len(token) >= 4
        }

        if not query_tokens:
            return None

        medication_token_matches: dict[str, int] = {}

        for medication in self.repository.get_all_medications():
            medication_tokens = set(
                re.findall(
                    r"\b[a-zA-ZÀ-ÿ0-9-]+\b",
                    medication.name.lower(),
                )
            )

            for token in query_tokens & medication_tokens:
                medication_token_matches[token] = (
                    medication_token_matches.get(token, 0) + 1
                )

        if not medication_token_matches:
            return None

        return max(
            medication_token_matches,
            key=medication_token_matches.get,
        )

    def _find_requested_information(self, query: str) -> str | None:
        normalized_query = query.lower()

        matches: list[str] = []

        for information, patterns in INFORMATION_PATTERNS.items():
            if any(pattern in normalized_query for pattern in patterns):
                matches.append(information)

        if not matches:
            return None

        return ", ".join(matches)