from qdrant_client import QdrantClient

from .vector_store import VectorStore


class QdrantStore(VectorStore):

    def __init__(
        self,
        host="localhost",
        port=6333,
        collection_name="documents"
    ):

        self.client = QdrantClient(
            host=host,
            port=port
        )

        self.collection_name = collection_name


    def upsert(
        self,
        vector,
        payload
    ):
        pass


    def search(
        self,
        vector,
        limit=5
    ):
        pass