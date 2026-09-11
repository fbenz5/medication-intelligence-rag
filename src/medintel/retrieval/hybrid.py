from medintel.embedding.service import EmbeddingService
from medintel.models.chunk import Chunk
from medintel.retrieval.bm25 import BM25Retriever
from medintel.retrieval.reranker import Reranker
from medintel.retrieval.rrf import reciprocal_rank_fusion
from medintel.vectorstore.qdrant import QdrantVectorStore

DENSE_LIMIT = 20
BM25_LIMIT = 20
RERANK_LIMIT = 5


class HybridRetriever:
    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self.chunks_by_id = {
            chunk.chunk_id: chunk
            for chunk in chunks
        }

        self.embedding_service = EmbeddingService()
        self.vector_store = QdrantVectorStore()
        self.bm25_retriever = BM25Retriever(chunks)
        self.reranker = Reranker()

    def search(
        self,
        query: str,
        limit: int = RERANK_LIMIT,
    ) -> list[tuple[Chunk, float]]:
        query_vector = self.embedding_service.embed_text(query)

        dense_results = self.vector_store.search(
            query_vector=query_vector,
            limit=DENSE_LIMIT,
        )

        dense_chunks = [
            self.chunks_by_id[point.payload["chunk_id"]]
            for point in dense_results
        ]

        bm25_results = self.bm25_retriever.search(
            query=query,
            limit=BM25_LIMIT,
        )

        bm25_chunks = [
            chunk
            for chunk, _score in bm25_results
        ]

        fused_results = reciprocal_rank_fusion(
            ranked_results=[
                dense_chunks,
                bm25_chunks,
            ],
            limit=DENSE_LIMIT + BM25_LIMIT,
        )

        candidate_chunks = [
            chunk
            for chunk, _score in fused_results
        ]

        return self.reranker.rerank(
            query=query,
            chunks=candidate_chunks,
            limit=limit,
        )