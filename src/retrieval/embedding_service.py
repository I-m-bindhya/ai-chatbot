import ollama


class EmbeddingService:

    def __init__(
        self,
        model="nomic-embed-text"
    ):
        self.model = model


    def embed(
        self,
        text
    ):

        response = ollama.embeddings(
            model=self.model,
            prompt=text
        )

        return response["embedding"]