from pydantic import BaseModel


class Chunk(BaseModel):
    chunk_id: str
    source: str
    title: str
    filename: str
    page_number: int
    text: str