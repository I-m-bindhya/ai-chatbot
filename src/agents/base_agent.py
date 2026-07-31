from abc import ABC, abstractmethod


class BaseAgent(ABC):

    @abstractmethod
    def can_handle(
        self,
        user_message: str
    ) -> bool:
        pass


    @abstractmethod
    def execute(
        self,
        conversation_id: int,
        user_message: str
    ):
        pass