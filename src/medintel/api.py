from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

from medintel.app import build_generation_service
from medintel.generation.citation import Citation
from medintel.generation.service import GeneratedResponse, GenerationService


class AskRequest(BaseModel):
    query: str = Field(min_length=1)


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]
    evidence_sufficient: bool


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.generation_service = build_generation_service()
    yield


app = FastAPI(
    title="Medication Intelligence API",
    version="0.1.0",
    description="Evidence-grounded medication intelligence API.",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/ask", response_model=AskResponse)
def ask(request: Request, payload: AskRequest) -> AskResponse:
    generation_service: GenerationService = request.app.state.generation_service

    result: GeneratedResponse = generation_service.answer(payload.query)

    return AskResponse(
        answer=result.answer,
        citations=result.citations,
        evidence_sufficient=result.evidence_sufficient,
    )