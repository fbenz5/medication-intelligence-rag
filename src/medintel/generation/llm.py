import os

from openai import OpenAI
from pydantic import BaseModel, Field

from medintel.generation.context import EvidenceContext
from medintel.generation.prompt import SYSTEM_PROMPT, build_prompt


class GeneratedAnswer(BaseModel):
    answer: str
    citations: list[str] = Field(default_factory=list)
    evidence_sufficient: bool


class LLMGenerator:
    def __init__(
        self,
        client: OpenAI | None = None,
        model: str = "gpt-5.6-terra",
    ) -> None:
        self.client = client or OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = model

    def generate(self, context: EvidenceContext) -> GeneratedAnswer:
        response = self.client.responses.parse(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=build_prompt(context),
            text_format=GeneratedAnswer,
        )

        if response.output_parsed is None:
            raise RuntimeError("The LLM did not return a structured answer.")

        return response.output_parsed