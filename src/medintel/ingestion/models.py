from pydantic import BaseModel

from medintel.models.medication import Medication


class IngestionResult(BaseModel):
    medications: list[Medication]
    total_rows: int
    successful_rows: int
    failed_rows: int