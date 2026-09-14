from unittest.mock import Mock

from medintel.generation.context import Evidence, EvidenceContext
from medintel.generation.llm import GeneratedAnswer, LLMGenerator


def test_llm_generator_returns_structured_answer() -> None:
    context = EvidenceContext(
        query="What are the cardiac risks?",
        evidences=[
            Evidence(
                evidence_id="DOC-001",
                evidence_type="unstructured_document",
                content="The medicine is associated with an increased risk of arrhythmia.",
                source="HAS",
                title="Medication safety guidance",
                filename="guidance.pdf",
                page_number=2,
            )
        ],
    )

    expected = GeneratedAnswer(
        answer="The medicine is associated with an increased risk of arrhythmia.",
        citations=["DOC-001"],
        evidence_sufficient=True,
    )

    parsed_response = Mock()
    parsed_response.output_parsed = expected

    client = Mock()
    client.responses.parse.return_value = parsed_response

    generator = LLMGenerator(
        client=client,
        model="test-model",
    )

    result = generator.generate(context)

    assert result == expected
    assert result.answer
    assert result.citations == ["DOC-001"]
    assert result.evidence_sufficient is True

    client.responses.parse.assert_called_once()