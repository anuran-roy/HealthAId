from qdrant_client import QdrantClient

qdrant = QdrantClient(
    "http://localhost:6333"
)  # Connect to existing Qdrant instance, for production


def get_top_k():
    qdrant
