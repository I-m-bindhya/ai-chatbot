from config import SYSTEM_PROMPT


class ChatService:

    def __init__(self, provider, memory):

        self.provider = provider
        self.memory = memory
    
    def create_new_chat(self):
        return self.memory.create_conversation()
    
    def rename_chat(self, conversation_id, title):
        return self.memory.update_conversation_title(conversation_id, title)
    
    def list_chats(self):
        return self.memory.load_conversations()
    
    def load_messages(self, conversation_id):
        return self.memory.load_messages(conversation_id)


    def chat(self, conversation_id,  user_input):

        if user_input.lower() == "/clear":
            self.memory.clear_messages(conversation_id)
            return "conversation removed. let start fresh"

        self.memory.save_message( conversation_id, "user", user_input)
        messages = self.memory.load_messages(conversation_id)
        messages.insert(0, { 'role': 'system', 'content': SYSTEM_PROMPT })

        reply = self.provider.chat(messages)

        self.memory.save_message(conversation_id, "assistant", reply)

        if(len(messages) == 2):
            title = self.provider.generate_title(user_input)
            self.rename_chat(conversation_id, title)

        return reply