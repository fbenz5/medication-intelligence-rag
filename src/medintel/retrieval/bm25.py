from rank_bm25 import BM25Okapi

from medintel.models.chunk import Chunk
from medintel.retrieval.text_normalizer import normalize_text


class BM25Retriever:
    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks

        tokenized_chunks = [
            normalize_text(chunk.text).split()
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(tokenized_chunks)

    def search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[tuple[Chunk, float]]:
        query_tokens = normalize_text(query).split()

        scores = self.bm25.get_scores(query_tokens)

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True,
        )[:limit]

        return [
            (self.chunks[index], float(scores[index]))
            for index in ranked_indices
        ]