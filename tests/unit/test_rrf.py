from medintel.models.chunk import Chunk
from medintel.retrieval.rrf import reciprocal_rank_fusion


def create_chunk(chunk_id: str) -> Chunk:
    return Chunk(
        chunk_id=chunk_id,
        source="HAS",
        title="Test document",
        filename="test.pdf",
        page_number=1,
        text=f"Text for {chunk_id}",
    )


def test_rrf_rewards_chunks_present_in_multiple_rankings() -> None:
    chunk_a = create_chunk("a")
    chunk_b = create_chunk("b")
    chunk_c = create_chunk("c")

    results = reciprocal_rank_fusion(
        ranked_results=[
            [chunk_a, chunk_b],
            [chunk_b, chunk_c],
        ],
        limit=3,
    )

    ranked_chunks = [chunk.chunk_id for chunk, _score in results]

    assert ranked_chunks[0] == "b"