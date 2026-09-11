from pydantic import BaseModel

from medintel.routing.router import RetrievalRoute


class QueryIntent(BaseModel):
    route: RetrievalRoute
    cis: str | None = None
    medication_name: str | None = None
    requested_information: str | None = None