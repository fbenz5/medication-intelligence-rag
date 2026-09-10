from langchain_huggingface import HuggingFaceEmbeddings


MODEL_NAME = "BAAI/bge-m3"


class EmbeddingService:
    def __init__(self) -> None:
        self._embeddings = HuggingFaceEmbeddings(
            model_name=MODEL_NAME,
            encode_kwargs={"normalize_embeddings": True},
        )

    def embed_text(self, text: str) -> list[float]:
        return self._embeddings.embed_query(text)

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return self._embeddings.embed_documents(texts)