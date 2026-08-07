import logging

class ChatService:

    logger = logging.getLogger(__name__)

    def __init__(self, provider, memory, agent, orchestrator, profile):
        self.provider = provider
        self.memory = memory
        self.agent = agent
        self.orchestrator = orchestrator
        self.profile = profile

    def create_new_chat(self):
        return self.memory.create_conversation()

    def rename_chat(self, conversation_id, title):
        return self.memory.update_conversation_title(
            conversation_id,
            title
        )

    def delete_conversation(self, conversation_id):
        return self.memory.clear_messages(conversation_id)

    def list_chats(self):
        return self.memory.load_conversations()

    def load_messages(self, conversation_id):
        return self.memory.load_messages(conversation_id)
    
    async def chat(self, conversation_id, user_input, multi_agent, background_tasks):

        self.logger.info("Execution Chat service", extra={
            "conversation_id": conversation_id
        })
        if user_input.lower() == "/clear":
            self.memory.clear_messages(conversation_id)
            return "conversation removed. let's start fresh"

        is_first_message = (
            len(self.memory.load_messages(conversation_id)) == 0
        )

        if multi_agent:
            final_reply = await self.orchestrator.run(
                conversation_id,
                user_input
            )
        else:
            final_reply = await self.agent.run(
                conversation_id,
                user_input,
                self.profile
            )

            if is_first_message:
                background_tasks.add_task(
                    self.generate_chat_title,
                    conversation_id,
                    user_input
                )

        return final_reply


    async def stream(self, conversation_id, user_input, multi_agent, background_tasks):
    
            if user_input.lower() == "/clear":
                self.memory.clear_messages(conversation_id)
                return "conversation removed. let's start fresh"
    
            is_first_message = (
                len(self.memory.load_messages(conversation_id)) == 0
            )
    
            if multi_agent:
                final_reply = await self.orchestrator.stream(
                    conversation_id,
                    user_input
                )
            else:
                final_reply = await self.agent.stream(
                    conversation_id,
                    user_input,
                    self.profile
                )
    
            if is_first_message:
                background_tasks.add_task(
                    self.generate_chat_title,
                    conversation_id,
                    user_input
                )
            return final_reply


    async def generate_chat_title(
        self,
        conversation_id,
        user_input
    ):
        title = await self.provider.generate_title(
            user_input
        )

        self.rename_chat(
            conversation_id,
            title
        )