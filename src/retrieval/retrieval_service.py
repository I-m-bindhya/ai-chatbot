class RetrievalService:

    def __init__(
        self,
        embedding_service,
        vector_store
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store


    def retrieve(
        self,
        question,
        limit=5
    ):

        vector = self.embedding_service.embed(
            question
        )

        return self.vector_store.search(
            vector,
            limit
        )