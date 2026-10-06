import logging
import time

from openai import OpenAI
from pydantic import BaseModel, Field

from medintel.config import settings
from medintel.generation.context import EvidenceContext
from medintel.generation.prompt import SYSTEM_PROMPT, build_prompt

logger = logging.getLogger("medintel.llm")


MODEL_PRICING_USD_PER_1M_TOKENS = {
    "gpt-5.6-terra": {
        "input": 2.00,
        "output": 12.00,
    },
    "gpt-5.6-sol": {
        "input": 4.00,
        "output": 20.00,
    },
    "gpt-5.6-luna": {
        "input": 0.20,
        "output": 1.20,
    },
}


class GeneratedAnswer(BaseModel):
    answer: str
    citations: list[str] = Field(default_factory=list)
    evidence_sufficient: bool


class LLMGenerator:
    def __init__(
        self,
        client: OpenAI | None = None,
        model: str | None = None,
    ) -> None:
        self.client = client or OpenAI(api_key=settings.openai_api_key)
        self.model = model or settings.openai_model

    def generate(self, context: EvidenceContext) -> GeneratedAnswer:
        start_time = time.perf_counter()

        response = self.client.responses.parse(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=build_prompt(context),
            text_format=GeneratedAnswer,
        )

        latency_ms = (time.perf_counter() - start_time) * 1000

        if response.output_parsed is None:
            logger.error(
                "llm_generation_failed",
                extra={
                    "model": self.model,
                    "latency_ms": round(latency_ms, 2),
                },
            )
            raise RuntimeError("The LLM did not return a structured answer.")

        usage = response.usage

        input_tokens = usage.input_tokens if usage else 0
        output_tokens = usage.output_tokens if usage else 0
        total_tokens = usage.total_tokens if usage else 0

        pricing = MODEL_PRICING_USD_PER_1M_TOKENS.get(self.model)

        cost_usd = None

        if pricing is not None:
            cost_usd = (
                input_tokens / 1_000_000 * pricing["input"]
                + output_tokens / 1_000_000 * pricing["output"]
            )

        logger.info(
            "llm_generation_completed",
            extra={
                "model": self.model,
                "latency_ms": round(latency_ms, 2),
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "cost_usd": round(cost_usd, 6) if cost_usd is not None else None,
            },
        )

        return response.output_parsed