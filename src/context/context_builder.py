class ContextBuilder:

    def __init__(self, memory_manager):
        self.memory_manager = memory_manager


    def build_context(
        self,
        conversation_id,
        user_message,
        retrieved_documents=None,
        tool_messages=None
    ):

        messages = list(
            self.memory_manager.build_context(
                conversation_id
            )
        )

        messages.append(
            {
                "role": "user",
                "content": user_message
            }
        )

        if retrieved_documents:
            messages.extend(
                retrieved_documents
            )

        if tool_messages:
            messages.extend(
                tool_messages
            )

        return messages