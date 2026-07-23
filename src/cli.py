from providers.ollama_provider import OllamaProvider
from services.chat_service import ChatService
from memory.memory_service import MemoryService

provider = OllamaProvider()
memory = MemoryService()
chatbot = ChatService(provider, memory)

def show_menu():
    print("\n\n==================\n\n")
    print("AI Chatbot v2")
    print("\n\n==================\n\n")
    print("1. New Chat \n")
    print("2. List Chats \n")
    print("3. Open Chat \n")
    print("4. Exit \n")
    print("\n\n==================\n\n")


show_menu()

while True:

    question = input("Choose: ")

    if question == "4":
        break

    if question == '1':
        conversation_id = chatbot.create_new_chat()
        while True:
            new_question = input(" You: ")
            if new_question.lower() == "/exit":
                print(f"\nAI: Quiting chat\n")
                show_menu();
                break;
            answer = chatbot.chat(conversation_id, new_question)
            print(f"\nAI: {answer}\n")

    if question == '2':
        conversation_lists = chatbot.list_chats()
        print(f"\n AI: {conversation_lists} \n")

    if question == '3':
        conversation_id = input('conversion id: ')
        messages = chatbot.load_messages(conversation_id)

        for message in messages:
            print(
                f"{message['role']}: {message['content']}"
            )

        new_question = input(" You: ")
        if new_question.lower() == "/exit":
            print(f"\nAI: Quiting chat\n")
            show_menu();
            break;

        answer = chatbot.chat(conversation_id, new_question)
        print(f"\nAssistant: {answer}\n")
