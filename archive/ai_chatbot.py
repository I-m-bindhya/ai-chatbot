from ollama import chat

print("=== AI Chatbot ===")
print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    print(f"\nAI: {response.message.content}\n")