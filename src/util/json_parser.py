from pydantic import BaseModel, Field
from src.util.usage import TokenUsage

class ToolCall(BaseModel):
    tool: str
    arguments: dict

class AIResponse(BaseModel):
    answer: str | None = None
    usage: TokenUsage | None = None
    topics: list[str] = Field(default_factory=list)
    confidence: str | None = None
    reasoning: str | None = None
    tool_call: ToolCall | None = None

class JsonParser():
    def parse(self, response: str) -> AIResponse:
        print("json parser", response)
        return AIResponse.model_validate_json(response)