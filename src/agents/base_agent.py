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

    async def execute(
        self,
        conversation_id,
        user_message
    ):
        return await self.ai_agent.run(
            conversation_id=conversation_id,
            user_message=user_message,
            profile=self.profile
        )


    async def stream(
        self,
        conversation_id,
        user_message
    ):
        return await self.ai_agent.stream(
            conversation_id=conversation_id,
            user_message=user_message,
            profile=self.profile
        )