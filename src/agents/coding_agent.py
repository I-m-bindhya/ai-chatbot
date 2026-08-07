from src.agents.base_agent import BaseAgent


class CodingAgent(BaseAgent):

    def can_handle(
        self,
        user_message
    ):

        user_message = user_message.lower()

        keywords = [
            "python",
            "fastapi",
            "django",
            "api",
            "class",
            "function",
            "bug",
            "error",
            "code"
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
        print("CodingAgent selected")
        return super().execute(
            conversation_id,
            user_message
        )