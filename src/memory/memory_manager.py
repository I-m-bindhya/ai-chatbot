class MemoryManager():

    def __init__(self, memory_service):
        self.memory_service = memory_service

    def trim_context(self, messages):
        return messages[-10:]

    def build_context(self, conversation_id):
        messages = self.memory_service.load_messages(
            conversation_id
        )

        return self.trim_context(messages)
    