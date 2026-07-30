from typing import Any

from src.actions.action import Action


class SearchMemoryAction(Action):
    """Search memories or indexed content for a query."""

    name = "search_memory"
    description = "Search stored memory or retrieved context for a query."

    def __init__(self, memory_service: Any, retrieval_service: Any = None) -> None:
        self.memory_service = memory_service
        self.retrieval_service = retrieval_service

    def execute(self, **kwargs: Any) -> Any:
        query = kwargs.get("query") or kwargs.get("text") or ""

        if self.retrieval_service is not None and hasattr(self.retrieval_service, "retrieve"):
            return self.retrieval_service.retrieve(query)

        if hasattr(self.memory_service, "search"):
            return self.memory_service.search(query)

        if hasattr(self.memory_service, "search_memory"):
            return self.memory_service.search_memory(query)

        return []
