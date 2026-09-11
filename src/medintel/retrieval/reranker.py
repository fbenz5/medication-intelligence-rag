from FlagEmbedding import FlagReranker

from medintel.models.chunk import Chunk

MODEL_NAME = "BAAI/bge-reranker-v2-m3"


class Reranker:
    def __init__(self) -> None:
        self._model = FlagReranker(
            MODEL_NAME,
            use_fp16=True,
        )

    def rerank(
        self,
        query: str,
        chunks: list[Chunk],
        limit: int = 5,
    ) -> list[tuple[Chunk, float]]:
        pairs = [
            [query, chunk.text]
            for chunk in chunks
        ]

        scores = self._model.compute_score(
            pairs,
            normalize=True,
        )

        if isinstance(scores, float):
            scores = [scores]

        ranked_results = sorted(
            zip(chunks, scores, strict=True),
            key=lambda item: item[1],
            reverse=True,
        )

        return ranked_results[:limit]