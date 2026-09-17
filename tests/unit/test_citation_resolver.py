import pytest

from medintel.generation.citation_resolver import (
    CitationResolver,
    CitationValidationError,
)
from medintel.generation.context import Evidence, EvidenceContext


def build_context() -> EvidenceContext:
    return EvidenceContext(
        query="What are the cardiac risks?",
        evidences=[
            Evidence(
                evidence_id="chunk-1",
                evidence_type="document",
                content="Cardiac risk evidence.",
                source="HAS",
                title="Bon usage des antiémétiques",
                filename="antiemetiques.pdf",
                page_number=12,
            ),
            Evidence(
                evidence_id="chunk-2",
                evidence_type="document",
                content="Additional evidence.",
                source="ANSM",
                title="Medication safety information",
                filename="safety.pdf",
                page_number=5,
            ),
        ],
    )


def test_resolves_evidence_id_to_source_metadata() -> None:
    context = build_context()

    citations = CitationResolver().resolve(
        evidence_ids=["chunk-1"],
        context=context,
    )

    assert len(citations) == 1
    assert citations[0].evidence_id == "chunk-1"
    assert citations[0].source == "HAS"
    assert citations[0].title == "Bon usage des antiémétiques"
    assert citations[0].page_number == 12


def test_resolves_multiple_citations() -> None:
    context = build_context()

    citations = CitationResolver().resolve(
        evidence_ids=["chunk-1", "chunk-2"],
        context=context,
    )

    assert [citation.evidence_id for citation in citations] == [
        "chunk-1",
        "chunk-2",
    ]


def test_removes_duplicate_citations() -> None:
    context = build_context()

    citations = CitationResolver().resolve(
        evidence_ids=["chunk-1", "chunk-1"],
        context=context,
    )

    assert [citation.evidence_id for citation in citations] == ["chunk-1"]


def test_rejects_unknown_citation() -> None:
    context = build_context()

    with pytest.raises(
        CitationValidationError,
        match="chunk-999",
    ):
        CitationResolver().resolve(
            evidence_ids=["chunk-999"],
            context=context,
        )