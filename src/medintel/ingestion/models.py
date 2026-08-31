from pydantic import BaseModel

from medintel.models.medication import Medication


class IngestionError(BaseModel):
    row_number: int
    error: str


class IngestionResult(BaseModel):
    medications: list[Medication]
    total_rows: int
    successful_rows: int
    failed_rows: int
    errors: list[IngestionError]