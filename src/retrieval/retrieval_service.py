from src.util.exception import RetrievalError


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
        conversation_id,
        question,
        limit=5
    ):

        vector = self.embedding_service.embed(
            question
        )

        try: 
            results = self.vector_store.search(
                conversation_id,
                vector,
                limit
            )

        except Exception as ex:
            raise RetrievalError(str(ex))

        MIN_SCORE = 0.80

        filtered = []

        for result in results:
            if result["score"] >= MIN_SCORE:
                filtered.append(result["payload"])

        return filtered