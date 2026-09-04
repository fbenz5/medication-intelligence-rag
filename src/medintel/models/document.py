from pydantic import BaseModel


class Document(BaseModel):
    source: str
    title: str
    filename: str
    page_number: int
    text: str