from medintel.models.chunk import Chunk
from medintel.models.composition import Composition
from medintel.models.medication import Medication
from medintel.models.presentation import Presentation
from medintel.routing.query_parser import QueryParser
from medintel.routing.retrieval import RetrievalService
from medintel.routing.router import QueryRouter, RetrievalRoute
from medintel.structured.composition_repository import CompositionRepository
from medintel.structured.presentation_repository import PresentationRepository
from medintel.structured.repository import MedicationRepository


class FakeHybridRetriever:
    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[tuple[Chunk, float]]:
        chunk = Chunk(
            chunk_id="test-chunk",
            source="HAS",
            title="Test document",
            filename="test.pdf",
            page_number=2,
            text="Domperidone cardiac risk evidence.",
        )
        return [(chunk, 0.95)]


def build_retrieval_service() -> RetrievalService:
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

    domperidone = Medication(
        cis="63630635",
        name="DOMPERIDONE ALMUS 10 mg, comprimé pelliculé",
        pharmaceutical_form="comprimé",
        administration_routes="orale",
        administrative_status="Autorisation active",
        authorization_procedure="Procédure nationale",
        commercialization_status="Commercialisée",
        authorization_date=None,
        bdm_status="Présent",
        european_authorization_number="",
        marketing_authorization_holder="ALMUS",
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

    medication_repository = MedicationRepository(
        [medication, domperidone],
    )

    presentation_repository = PresentationRepository(
        [presentation],
    )

    composition_repository = CompositionRepository(
        [composition],
    )

    query_parser = QueryParser(
        router=QueryRouter(),
        repository=medication_repository,
    )

    return RetrievalService(
        query_parser=query_parser,
        medication_repository=medication_repository,
        presentation_repository=presentation_repository,
        composition_repository=composition_repository,
        hybrid_retriever=FakeHybridRetriever(),
    )


def test_structured_retrieval() -> None:
    service = build_retrieval_service()

    result = service.retrieve(
        "What is the administrative status of CIS 60002283?"
    )

    assert result.intent.route == RetrievalRoute.STRUCTURED
    assert result.intent.cis == "60002283"

    assert len(result.medications) == 1
    assert result.medications[0].cis == "60002283"

    assert len(result.presentations) == 1
    assert len(result.compositions) == 1

    assert result.chunks == []


def test_rag_retrieval() -> None:
    service = build_retrieval_service()

    result = service.retrieve(
        "What are the risks of domperidone?"
    )

    assert result.intent.route == RetrievalRoute.RAG
    assert result.intent.medication_name == "domperidone"

    assert result.medications == []
    assert result.presentations == []
    assert result.compositions == []

    assert len(result.chunks) == 1


def test_both_retrieval() -> None:
    service = build_retrieval_service()

    result = service.retrieve(
        "What is the reimbursement rate of domperidone "
        "and what are its cardiac risks?"
    )

    assert result.intent.route == RetrievalRoute.BOTH
    assert result.intent.medication_name == "domperidone"
    assert result.intent.requested_information == "reimbursement, risks"

    assert len(result.medications) == 1
    assert result.medications[0].cis == "63630635"

    assert result.chunks == [
        result.chunks[0],
    ]