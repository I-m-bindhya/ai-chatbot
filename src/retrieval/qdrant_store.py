from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
)

from src.retrieval.vector_store import VectorStore


class QdrantStore(VectorStore):

    COLLECTION_NAME = "chat_memory"

    def __init__(self):

        self.client = QdrantClient(
            host="localhost",
            port=6333
        )

        self._create_collection()

    def _create_collection(self):

        collections = self.client.get_collections()

        exists = any(
            collection.name == self.COLLECTION_NAME
            for collection in collections.collections
        )

        if exists:
            return

        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE
            )
        )

    def search(
        self,
        vector,
        limit=5
    ):

        response = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=vector,
            limit=limit
        )

        return [
            point.payload
            for point in response.points
        ]

    def upsert(
        self,
        point_id,
        vector,
        payload
    ):

        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            ]
        )