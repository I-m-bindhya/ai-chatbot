from pydantic import BaseModel, Field

class ToolCall(BaseModel):
    tool: str
    arguments: dict

class AIResponse(BaseModel):
    answer: str | None = None
    topics: list[str] = Field(default_factory=list)
    confidence: str | None = None
    reasoning: str | None = None
    tool_call: ToolCall | None = None

class JsonParser():
    def parse(self, response: str) -> AIResponse:
        print("json parser", response)
        return AIResponse.model_validate_json(response)