from typing import Any

from src.actions.action import Action


class SummarizeAction(Action):
    """Summarize a block of text or conversation content."""

    name = "summarize"
    description = "Create a short summary for a piece of content."

    def __init__(self, summarizer_service: Any = None) -> None:
        self.summarizer_service = summarizer_service

    def execute(self, **kwargs: Any) -> Any:
        text = kwargs.get("text") or kwargs.get("content") or ""

        if self.summarizer_service is not None:
            if hasattr(self.summarizer_service, "summarize"):
                return self.summarizer_service.summarize(text)
            if hasattr(self.summarizer_service, "summarize_text"):
                return self.summarizer_service.summarize_text(text)

        if len(text) > 200:
            return text[:200] + "..."
        return text
