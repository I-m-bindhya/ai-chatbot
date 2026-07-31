from src.agents.base_agent import BaseAgent


class CodingAgent(BaseAgent):

    def __init__(
        self,
        ai_agent
    ):
        self.ai_agent = ai_agent


    def can_handle(
        self,
        user_message
    ):

        text = user_message.lower()

        keywords = [
            "python",
            "java",
            "code",
            "bug",
            "function",
            "class",
            "fastapi",
            "django"
        ]

        return any(
            word in text
            for word in keywords
        )


    def execute(
        self,
        conversation_id,
        user_message
    ):

        return self.ai_agent.run(
            conversation_id,
            user_message
        )