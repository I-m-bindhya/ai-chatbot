from abc import ABC, abstractmethod


class VectorStore(ABC):

    @abstractmethod
    def upsert(
        self,
        point_id,
        vector,
        payload
    ):
        pass


    @abstractmethod
    def search(
        self,
        vector,
        limit=5
    ):
        pass