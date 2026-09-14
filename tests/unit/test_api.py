from fastapi.testclient import TestClient

from medintel.api import app
from medintel.generation.llm import GeneratedAnswer


class FakeGenerationService:
    def answer(self, query: str) -> GeneratedAnswer:
        assert query == "What are the cardiac risks?"

        return GeneratedAnswer(
            answer="The available evidence indicates an increased risk of arrhythmia.",
            citations=["chunk-1"],
            evidence_sufficient=True,
        )


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_returns_grounded_answer() -> None:
    with TestClient(app) as client:
        app.state.generation_service = FakeGenerationService()

        response = client.post(
            "/api/v1/ask",
            json={"query": "What are the cardiac risks?"},
        )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "The available evidence indicates an increased risk of arrhythmia.",
        "citations": ["chunk-1"],
        "evidence_sufficient": True,
    }