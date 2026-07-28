class SummaryService:

    def __init__(
        self,
        memory_service,
        provider,
        indexing_service
    ):

        self.memory_service = memory_service
        self.provider = provider
        self.indexing_service = indexing_service


    def generate_summary(
        self,
        conversation_id
    ):
        messages = self.memory_service.load_messages(conversation_id)
        summary = self.provider.generate_summary(messages)
        summary_id = self.memory_service.save_summary(conversation_id, summary)
        self.indexing_service.index(
            summary_id,
            summary,
            {
                "conversation_id": conversation_id,
                "type": "summary"
            }
        )
        return summary