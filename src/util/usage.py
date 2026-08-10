from pydantic import BaseModel


class TokenUsage(BaseModel):
    model: str

    prompt_tokens: int

    completion_tokens: int

    total_tokens: int

    latency_ms: float

    prompt_version: str



    def merge_usage(total: TokenUsage, current: TokenUsage):
        if not current:
            return

        total.prompt_tokens += current.prompt_tokens
        total.completion_tokens += current.completion_tokens
        total.total_tokens += current.total_tokens
        total.latency_ms += current.latency_ms
        total.prompt_version = current.prompt_version