from ollama import chat

response = chat(
    model="qwen2.5:7b",
    messages=[
        {
            "role": "user",
            "content": "Say hello to a backend Python developer learning AI Engineering."
        }
    ]
)

print(response.message.content)