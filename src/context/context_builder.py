class ContextBuilder:

    def __init__(self, memory_manager, retrieval_service):
        self.memory_manager = memory_manager
        self.retrieval_service = retrieval_service


    def build_context(
        self,
        conversation_id,
        user_message,
        retrieved_documents=None,
        tool_messages=None
    ):

        messages = []

        retrieved_documents = self.retrieval_service.retrieve(
            user_message
        )

        if retrieved_documents:

            for doc in retrieved_documents:

                content = doc.get(
                    "content",
                    doc.get("text")
                )

                messages.append(
                    {
                        "role": "system",
                        "content": f"Relevant memory: {content}"
                    }
                )

        messages.extend(list(
            self.memory_manager.build_context(
                conversation_id
            )
        ))

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