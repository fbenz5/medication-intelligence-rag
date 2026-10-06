import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field

from medintel.app import build_generation_service
from medintel.generation.citation import Citation
from medintel.generation.service import GeneratedResponse, GenerationService

logger = logging.getLogger("medintel.api")


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


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    response = None

    try:
        response = await call_next(request)

        return response

    except Exception:
        logger.exception(
            "request_failed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
            },
        )
        raise

    finally:
        latency_ms = (time.perf_counter() - start_time) * 1000

        logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code if response else 500,
                "latency_ms": round(latency_ms, 2),
            },
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