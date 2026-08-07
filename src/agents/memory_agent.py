from src.agents.agent_profile import AgentProfile
from src.agents.base_agent import BaseAgent


class MemoryAgent(BaseAgent):

    def can_handle(
        self,
        user_message
    ):
        user_message = user_message.lower()

        keywords = [
            "conversation",
            "memory",
            "remember",
            "history",
            "chat",
            "summary"
        ]

        return any(
            word in user_message
            for word in keywords
        )

    def execute(
        self,
        conversation_id,
        user_message
    ):
        print("MemoryAgent selected")
        return super().execute(
            conversation_id,
            user_message
        )