from collections import defaultdict

from medintel.models.chunk import Chunk

DEFAULT_K = 60


def reciprocal_rank_fusion(
    ranked_results: list[list[Chunk]],
    k: int = DEFAULT_K,
    limit: int = 5,
) -> list[tuple[Chunk, float]]:
    scores: dict[str, float] = defaultdict(float)
    chunks: dict[str, Chunk] = {}

    for results in ranked_results:
        for rank, chunk in enumerate(results, start=1):
            scores[chunk.chunk_id] += 1 / (k + rank)
            chunks[chunk.chunk_id] = chunk

    ranked_chunk_ids = sorted(
        scores,
        key=scores.get,
        reverse=True,
    )[:limit]

    return [
        (chunks[chunk_id], scores[chunk_id])
        for chunk_id in ranked_chunk_ids
    ]