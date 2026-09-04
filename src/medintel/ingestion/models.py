from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class IngestionError(BaseModel):
    row_number: int
    error: str


class IngestionResult[T](BaseModel):
    items: list[T]
    total_rows: int
    successful_rows: int
    failed_rows: int
    errors: list[IngestionError]