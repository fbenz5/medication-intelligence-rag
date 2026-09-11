from pydantic import BaseModel, Field

from medintel.routing.retrieval import RetrievalResult


class Evidence(BaseModel):
    evidence_id: str
    evidence_type: str
    content: str
    source: str | None = None
    title: str | None = None
    filename: str | None = None
    page_number: int | None = None


class EvidenceContext(BaseModel):
    query: str
    evidences: list[Evidence] = Field(default_factory=list)

    def to_text(self) -> str:
        sections: list[str] = []

        for evidence in self.evidences:
            header = f"[{evidence.evidence_id}] {evidence.evidence_type}"

            metadata: list[str] = []

            if evidence.source:
                metadata.append(f"Source: {evidence.source}")

            if evidence.title:
                metadata.append(f"Title: {evidence.title}")

            if evidence.filename:
                metadata.append(f"File: {evidence.filename}")

            if evidence.page_number is not None:
                metadata.append(f"Page: {evidence.page_number}")

            section = "\n".join(
                [
                    header,
                    *metadata,
                    f"Content: {evidence.content}",
                ]
            )

            sections.append(section)

        return "\n\n".join(sections)


class EvidenceContextBuilder:
    def build(
        self,
        query: str,
        result: RetrievalResult,
    ) -> EvidenceContext:
        evidences: list[Evidence] = []

        evidences.extend(self._build_medication_evidence(result))
        evidences.extend(self._build_presentation_evidence(result))
        evidences.extend(self._build_composition_evidence(result))
        evidences.extend(self._build_chunk_evidence(result))

        return EvidenceContext(
            query=query,
            evidences=evidences,
        )

    def _build_medication_evidence(
        self,
        result: RetrievalResult,
    ) -> list[Evidence]:
        return [
            Evidence(
                evidence_id=f"medication-{index}",
                evidence_type="structured_medication",
                content=(
                    f"CIS: {medication.cis}\n"
                    f"Name: {medication.name}\n"
                    f"Pharmaceutical form: {medication.pharmaceutical_form}\n"
                    f"Administration routes: {medication.administration_routes}\n"
                    f"Administrative status: {medication.administrative_status}\n"
                    f"Authorization procedure: {medication.authorization_procedure}\n"
                    f"Commercialization status: {medication.commercialization_status}\n"
                    f"Authorization date: {medication.authorization_date}\n"
                    f"BDM status: {medication.bdm_status}\n"
                    f"European authorization number: "
                    f"{medication.european_authorization_number}\n"
                    f"Marketing authorization holder: "
                    f"{medication.marketing_authorization_holder}\n"
                    f"Enhanced monitoring: {medication.enhanced_monitoring}"
                ),
                source="BDPM",
            )
            for index, medication in enumerate(result.medications, start=1)
        ]

    def _build_presentation_evidence(
        self,
        result: RetrievalResult,
    ) -> list[Evidence]:
        return [
            Evidence(
                evidence_id=f"presentation-{index}",
                evidence_type="structured_presentation",
                content=(
                    f"CIS: {presentation.cis}\n"
                    f"CIP7: {presentation.cip7}\n"
                    f"Name: {presentation.name}\n"
                    f"Administrative status: {presentation.administrative_status}\n"
                    f"Commercialization status: {presentation.commercialization_status}\n"
                    f"Commercialization date: {presentation.commercialization_date}\n"
                    f"CIP13: {presentation.cip13}\n"
                    f"Collective agreement: {presentation.collective_agreement}\n"
                    f"Reimbursement rate: {presentation.reimbursement_rate}\n"
                    f"Price: {presentation.price}\n"
                    f"Public price: {presentation.public_price}\n"
                    f"Dispensing fee: {presentation.dispensing_fee}\n"
                    f"Reimbursement indications: {presentation.reimbursement_indications}"
                ),
                source="BDPM",
            )
            for index, presentation in enumerate(result.presentations, start=1)
        ]

    def _build_composition_evidence(
        self,
        result: RetrievalResult,
    ) -> list[Evidence]:
        return [
            Evidence(
                evidence_id=f"composition-{index}",
                evidence_type="structured_composition",
                content=(
                    f"CIS: {composition.cis}\n"
                    f"Pharmaceutical element: {composition.pharmaceutical_element}\n"
                    f"Substance code: {composition.substance_code}\n"
                    f"Substance name: {composition.substance_name}\n"
                    f"Dosage: {composition.dosage}\n"
                    f"Dosage reference: {composition.dosage_reference}\n"
                    f"Component type: {composition.component_type}\n"
                    f"Component link number: {composition.component_link_number}"
                ),
                source="BDPM",
            )
            for index, composition in enumerate(result.compositions, start=1)
        ]

    def _build_chunk_evidence(
        self,
        result: RetrievalResult,
    ) -> list[Evidence]:
        return [
            Evidence(
                evidence_id=f"chunk-{index}",
                evidence_type="unstructured_document",
                content=chunk.text,
                source=chunk.source,
                title=chunk.title,
                filename=chunk.filename,
                page_number=chunk.page_number,
            )
            for index, (chunk, _score) in enumerate(result.chunks, start=1)
        ]