from medintel.generation.citation import Citation
from medintel.generation.context import EvidenceContext


class CitationValidationError(ValueError):
    """Raised when an answer contains an invalid evidence citation."""


class CitationResolver:
    def resolve(
        self,
        evidence_ids: list[str],
        context: EvidenceContext,
    ) -> list[Citation]:
        evidence_by_id = {
            evidence.evidence_id: evidence
            for evidence in context.evidences
        }

        invalid_ids = [
            evidence_id
            for evidence_id in evidence_ids
            if evidence_id not in evidence_by_id
        ]

        if invalid_ids:
            invalid_ids = list(dict.fromkeys(invalid_ids))

            raise CitationValidationError(
                f"Answer contains invalid evidence citations: {invalid_ids}"
            )

        citations: list[Citation] = []

        for evidence_id in dict.fromkeys(evidence_ids):
            evidence = evidence_by_id[evidence_id]

            citations.append(
                Citation(
                    evidence_id=evidence.evidence_id,
                    source=evidence.source,
                    title=evidence.title,
                    filename=evidence.filename,
                    page_number=evidence.page_number,
                )
            )

        return citations