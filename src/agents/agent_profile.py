from dataclasses import dataclass


@dataclass(frozen=True)
class AgentProfile:

    name: str

    description: str

    system_prompt: str

    planning_prompt: str

    reflection_prompt: str

    allowed_tools: list[str]