from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from medintel.models.chunk import Chunk


QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "medication_documents"


class QdrantVectorStore:
    def __init__(self) -> None:
        self.client = QdrantClient(url=QDRANT_URL)

    def upsert_chunks(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError(
                "The number of chunks must match the number of embeddings."
            )

        points = [
            PointStruct(
                id=index,
                vector=embedding,
                payload={
                    "chunk_id": chunk.chunk_id,
                    "source": chunk.source,
                    "title": chunk.title,
                    "filename": chunk.filename,
                    "page_number": chunk.page_number,
                    "text": chunk.text,
                },
            )
            for index, (chunk, embedding) in enumerate(
                zip(chunks, embeddings, strict=True)
            )
        ]

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ) -> list:
        return self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            with_payload=True,
        ).points