from ollama import chat
from src.util.json_parser import AIResponse, JsonParser, ToolCall
from src.config import MODEL_NAME
from src.util.exception import ProviderError

json_parser = JsonParser()

class OllamaProvider:

    def chat(self, messages, tools=None):
        response = chat(
            model=MODEL_NAME,
            messages=messages,
            tools=tools
        )

        print("reponse from model", response)

        if response.message.tool_calls:

            tool = response.message.tool_calls[0]

            return AIResponse(
                tool_call = ToolCall(
                    tool=tool.function.name,
                    arguments=tool.function.arguments
                )
            )

        reply = response.message.content
        try:
            return json_parser.parse(reply)
        except (TypeError, ValueError):
            return AIResponse(answer=reply)


    def chat_raw(self, messages):
        try:
            response = chat(
                model=MODEL_NAME,
                messages=messages
            )

            return response.message.content
        except Exception as ex:
            raise ProviderError(str(ex))

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

        reply = response.message.content
        return reply


    def generate_summary(self, message):
        response = chat(
            model=MODEL_NAME,
            messages= [
                {
                    "role": "user",
                    "content": f"Summarize the following conversation.\n\n Keep only long-term facts.\n\n Conversations: \n {message}"
                }
            ]
        )

        reply = response.message.content
        return reply