from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from medintel.config import settings
from medintel.models.chunk import Chunk


class QdrantVectorStore:
    VECTOR_SIZE = 1024

    def __init__(self) -> None:
        self.client = QdrantClient(url=settings.qdrant_url)

    def create_collection(self) -> None:
        collections = self.client.get_collections().collections

        if any(
            collection.name == settings.qdrant_collection
            for collection in collections
        ):
            return

        self.client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(
                size=self.VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

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
            collection_name=settings.qdrant_collection,
            points=points,
        )

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ) -> list:
        return self.client.query_points(
            collection_name=settings.qdrant_collection,
            query=query_vector,
            limit=limit,
            with_payload=True,
        ).points