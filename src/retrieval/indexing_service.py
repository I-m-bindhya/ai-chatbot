class IndexingService:

    def __init__(
        self,
        embedding_service,
        vector_store
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store


    def index(
        self,
        point_id,
        text,
        payload
    ):

        vector = self.embedding_service.embed(
            text
        )

        self.vector_store.upsert(
            point_id,
            vector,
            payload
        )