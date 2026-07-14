from ollama import chat

from config import MODEL_NAME


class OllamaProvider:

    def chat(self, messages):
        response = chat(
            model=MODEL_NAME,
            messages=messages
        )

        return response.message.content
    
    def generate_title(self, message):
        response = chat(
            model=MODEL_NAME,
            messages= [
                {
                    "role": "user",
                    "content": f"Generate a short chat title (maximum 5 words) for this message:\n\n{message}"
                }
            ]
        )

        return response.message.content