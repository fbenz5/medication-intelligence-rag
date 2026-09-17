from fastapi.testclient import TestClient

from medintel.api import app
from medintel.generation.citation import Citation
from medintel.generation.service import GeneratedResponse


class FakeGenerationService:
    def answer(self, query: str) -> GeneratedResponse:
        return GeneratedResponse(
            answer="Test answer.",
            citations=[
                Citation(
                    evidence_id="chunk-1",
                    source="HAS",
                    title="Test document",
                    filename="test.pdf",
                    page_number=12,
                )
            ],
            evidence_sufficient=True,
        )


def test_health() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_returns_structured_citations() -> None:
    app.state.generation_service = FakeGenerationService()

    client = TestClient(app)

    response = client.post(
        "/api/v1/ask",
        json={"query": "What are the cardiac risks?"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == "Test answer."
    assert data["evidence_sufficient"] is True
    assert data["citations"] == [
        {
            "evidence_id": "chunk-1",
            "source": "HAS",
            "title": "Test document",
            "filename": "test.pdf",
            "page_number": 12,
        }
    ]