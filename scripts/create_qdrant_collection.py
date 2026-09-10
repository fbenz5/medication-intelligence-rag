from medintel.vectorstore.qdrant import QdrantVectorStore


def main() -> None:
    vector_store = QdrantVectorStore()
    vector_store.create_collection()

    print("Qdrant collection created.")


if __name__ == "__main__":
    main()