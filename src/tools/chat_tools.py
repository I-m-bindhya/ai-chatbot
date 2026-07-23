class ChatTools:

    def __init__(self, chatbot):
        self.chatbot = chatbot

    def list_chats(self):
        return self.chatbot.list_chats()
    
    def create_new_chat(self):
        return self.chatbot.create_new_chat()
    
    def rename_chat(self, conversation_id: int, title: str):
        return self.chatbot.rename_chat(conversation_id, title)
    
    def delete_conversation(self, conversation_id: int):
        return self.chatbot.delete_conversation(conversation_id)
    
    def get_tools(self):
        return [
            {
                "name": "list_chats",
                "description": "Return all conversations.",
                "parameters": [],
                "function": self.list_chats
            },
            {
                "name": "create_new_chat",
                "description": "Create a new conversation.",
                "parameters": [],
                "function": self.create_new_chat
            },
            {
                "name": "rename_chat",
                "description": "Rename an existing conversation.",
                "parameters": {
                    "conversation_id": {
                        "type": "integer",
                        "description": "Conversation ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title"
                    }
                },
                "function": self.rename_chat
            },
            {
                "name": "delete_conversation",
                "description": "Delete a conversation.",
                "parameters": {
                    "conversation_id": {
                        "type": "integer",
                        "description": "Conversation ID"
                    },
                },
                "function": self.delete_conversation
            }
        ]