
class ChatService:

    def __init__(self, provider, memory, agent):
        self.provider = provider
        self.memory = memory
        self.agent = agent

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
    
    def chat(self, conversation_id, user_input):

        if user_input.lower() == "/clear":
            self.memory.clear_messages(conversation_id)
            return "conversation removed. let's start fresh"

        is_first_message = (
            len(self.memory.load_messages(conversation_id)) == 0
        )

        final_reply = self.agent.run(
            conversation_id,
            user_input
        )

        if is_first_message:
            title = self.provider.generate_title(user_input)
            self.rename_chat(conversation_id, title)

        return final_reply