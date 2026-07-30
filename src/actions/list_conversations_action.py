from src.actions.action import Action


class ListConversationsAction(Action):

    def __init__(
        self,
        memory_service
    ):
        self.memory_service = memory_service

    def execute(
        self,
        conversation_id
    ):

        conversations = self.memory_service.load_conversations()

        return [{
            "role": "system",
            "content": str(conversations)
        }]