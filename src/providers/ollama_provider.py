from ollama import chat, AsyncClient
from src.util.json_parser import AIResponse, JsonParser, ToolCall
from src.config import MODEL_NAME
from src.util.exception import ProviderError
import time

from src.util.usage import TokenUsage

client = AsyncClient()

json_parser = JsonParser()

class OllamaProvider:

    async def chat(self, messages, tools=None):
        start_time = time.perf_counter()
        response = await client.chat(
            model=MODEL_NAME,
            messages=messages,
            tools=tools
        )
        latency_ms = (
            time.perf_counter() - start_time
        ) * 1000

        prompt_tokens = (
            response.prompt_eval_count or 0
        )

        completion_tokens = (
            response.eval_count or 0
        )

        total_tokens = (
            prompt_tokens + completion_tokens
        )

        request_usage = TokenUsage(
            model=MODEL_NAME,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            latency_ms=latency_ms
        )

        print("reponse from model", response)

        if response.message.tool_calls:

            tool = response.message.tool_calls[0]

            return AIResponse(
                tool_call = ToolCall(
                    tool=tool.function.name,
                    arguments=tool.function.arguments
                ),
                usage=request_usage
            )

        reply = response.message.content
        try:
            parsed = json_parser.parse(reply)

            parsed.usage = request_usage

            return parsed
        except (TypeError, ValueError):
            return AIResponse(answer=reply, usage=request_usage)


    async def chat_raw(self, messages):
        try:
            response = await client.chat(
                model=MODEL_NAME,
                messages=messages
            )

            return response.message.content
        except Exception as ex:
            raise ProviderError(str(ex))

    async def generate_title(self, message):
        response = await client.chat(
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


    async def generate_summary(self, message):
        response = await client.chat(
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

    async def stream_chat(
        self,
        messages
    ):

        response = await client.chat(
            model=MODEL_NAME,
            messages=messages,
            stream=True
        )

        async for chunk in response:
            yield chunk.message.content