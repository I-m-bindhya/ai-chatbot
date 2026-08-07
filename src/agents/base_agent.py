from abc import ABC, abstractmethod

class BaseAgent(ABC):

    def __init__(
        self,
        profile,
        ai_agent
    ):
        self.profile = profile
        self.ai_agent = ai_agent

    @abstractmethod
    def can_handle(
        self,
        user_message
    ):
        pass

    def execute(
        self,
        conversation_id,
        user_message
    ):
        return self.ai_agent.run(
            conversation_id=conversation_id,
            user_message=user_message,
            profile=self.profile
        )