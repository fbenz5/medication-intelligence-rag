from medintel.generation.context import EvidenceContextBuilder
from medintel.models.chunk import Chunk
from medintel.models.composition import Composition
from medintel.models.medication import Medication
from medintel.models.presentation import Presentation
from medintel.routing.intent import QueryIntent
from medintel.routing.retrieval import RetrievalResult
from medintel.routing.router import RetrievalRoute


def test_build_structured_evidence_context() -> None:
    medication = Medication(
        cis="60002283",
        name="ANASTROZOLE ACCORD 1 mg, comprimé pelliculé",
        pharmaceutical_form="comprimé",
        administration_routes="orale",
        administrative_status="Autorisation active",
        authorization_procedure="Procédure nationale",
        commercialization_status="Commercialisée",
        authorization_date=None,
        bdm_status="Présent",
        european_authorization_number="",
        marketing_authorization_holder="ACCORD HEALTHCARE",
        enhanced_monitoring="",
    )

    presentation = Presentation(
        cis="60002283",
        cip7="4949729",
        name="30 comprimé(s)",
        administrative_status="Présentation active",
        commercialization_status="Commercialisée",
        commercialization_date=None,
        cip13="3400949497294",
        collective_agreement="",
        reimbursement_rate="100%",
        price=24.34,
        public_price=None,
        dispensing_fee=None,
        reimbursement_indications="",
    )

    composition = Composition(
        cis="60002283",
        pharmaceutical_element="comprimé",
        substance_code="12345",
        substance_name="ANASTROZOLE",
        dosage="1,00 mg",
        dosage_reference="",
        component_type="Substance active",
        component_link_number="",
    )

    result = RetrievalResult(
        intent=QueryIntent(
            route=RetrievalRoute.STRUCTURED,
            cis="60002283",
            requested_information="administrative status",
        ),
        medications=[medication],
        presentations=[presentation],
        compositions=[composition],
    )

    context = EvidenceContextBuilder().build(
        query="What is the administrative status of CIS 60002283?",
        result=result,
    )

    assert len(context.evidences) == 3

    assert any(
        evidence.evidence_type == "structured_medication"
        for evidence in context.evidences
    )
    assert any(
        evidence.evidence_type == "structured_presentation"
        for evidence in context.evidences
    )
    assert any(
        evidence.evidence_type == "structured_composition"
        for evidence in context.evidences
    )

    text = context.to_text()

    assert "60002283" in text
    assert "ANASTROZOLE ACCORD" in text
    assert "BDPM" in text


def test_build_rag_evidence_context() -> None:
    chunk = Chunk(
        chunk_id="bon_usage_antiemetiques.pdf-p2-lc4",
        source="HAS",
        title="Bon usage des antiémétiques",
        filename="bon_usage_antiemetiques.pdf",
        page_number=2,
        text="Domperidone may increase the risk of cardiac adverse effects.",
    )

    result = RetrievalResult(
        intent=QueryIntent(
            route=RetrievalRoute.RAG,
            medication_name="domperidone",
            requested_information="risks",
        ),
        chunks=[(chunk, 0.9759)],
    )

    context = EvidenceContextBuilder().build(
        query="What are the risks of domperidone?",
        result=result,
    )

    assert len(context.evidences) == 1

    evidence = context.evidences[0]

    assert evidence.evidence_type == "unstructured_document"
    assert evidence.source == "HAS"
    assert evidence.page_number == 2
    assert "cardiac adverse effects" in evidence.content

    text = context.to_text()

    assert "Page: 2" in text
    assert "HAS" in text