from pydantic import BaseModel


class Citation(BaseModel):
    evidence_id: str
    source: str | None = None
    title: str | None = None
    filename: str | None = None
    page_number: int | None = None