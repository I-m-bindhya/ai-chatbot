from src.agents.agent_profile import AgentProfile

from src.prompt.agent_prompt import (
    MEMORY_SYSTEM_PROMPT,
    MEMORY_PLANNING_PROMPT,
    MEMORY_REFLECTION_PROMPT,
    CODING_SYSTEM_PROMPT,
    CODING_PLANNING_PROMPT,
    CODING_REFLECTION_PROMPT,
)


MEMORY_PROFILE = AgentProfile(
    name="memory",
    description="Handles memory and conversation tasks.",
    system_prompt=MEMORY_SYSTEM_PROMPT,
    planning_prompt=MEMORY_PLANNING_PROMPT,
    reflection_prompt=MEMORY_REFLECTION_PROMPT,
    allowed_tools=[
        "list_chats",
        "retrieve_memory",
        "conversation_summary",
    ],
)


CODING_PROFILE = AgentProfile(
    name="coding",
    description="Handles software development tasks.",
    system_prompt=CODING_SYSTEM_PROMPT,
    planning_prompt=CODING_PLANNING_PROMPT,
    reflection_prompt=CODING_REFLECTION_PROMPT,
    allowed_tools=[
        "python_executor",
        "code_search",
        "documentation",
    ],
)   