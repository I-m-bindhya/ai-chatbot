from typing import Any, Dict, Iterable

from src.actions.action import Action


class ActionRegistry:
    """Registers and executes available actions."""

    def __init__(self) -> None:
        self._actions: Dict[str, Action] = {}

    def register(self, name, action: Action) -> None:
        self._actions[str(name)] = action

    def get(self, name: str) -> Action:
        normalized_name = self._normalize_name(name)
        if normalized_name in self._actions:
            return self._actions[normalized_name]

        if name in self._actions:
            return self._actions[name]

        raise KeyError(f"Unknown action: {name}")

    def get_action(self, name: str) -> Action:
        return self.get(name)

    def execute(self, name: str, **kwargs: Any) -> Any:
        action = self.get_action(name)
        return action.execute(**kwargs)

    def _normalize_name(self, name: str) -> str:
        if hasattr(name, "value"):
            return str(name.value)
        return str(name)
