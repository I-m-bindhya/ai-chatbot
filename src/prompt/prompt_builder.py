from src.prompt.schema import CHAT_RESPONSE_SCHEMA
from src.config import SYSTEM_PROMPT

class PromptBuilder():
    def build_tool_prompt(self, message):
        prompt = [{
            'role': 'SYSTEM',
            'content': SYSTEM_PROMPT
        }]

        prompt.extend(message)

        return prompt
    
    def build_response_prompt(self, messages):

        prompt = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "system",
                "content": CHAT_RESPONSE_SCHEMA
            }
        ]

        prompt.extend(messages)

        return prompt