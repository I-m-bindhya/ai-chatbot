# Day 5 – Agent Profiles & True Multi-Agent Intelligence

**Date:** August 6, 2026

---

# 🎯 Objective

Today we transformed our multi-agent architecture from **routing-only** into a system where each agent has its own **identity**.

Before today:

```text
RouterAgent
      │
      ▼
MemoryAgent
      │
      ▼
AIAgent.run()

CodingAgent
      │
      ▼
AIAgent.run()
```

After today:

```text
RouterAgent
      │
      ▼
MemoryAgent
      │
      ▼
Memory Profile
      │
      ▼
AIAgent.run(profile)
```

The same execution engine now behaves differently depending on the active profile.

---

# 📚 Topics Covered

* Agent Profile Pattern
* Agent Identity
* BaseAgent Refactoring
* Prompt Separation
* Profile-driven Execution
* Tool Restriction using Profiles
* Production Architecture Improvements

---

# 1. Why Agent Profiles?

Previously, all agent behavior was hardcoded.

Example:

```python
SYSTEM_PROMPT
```

Every agent shared the same prompt.

Every agent shared the same tools.

Every agent shared the same reasoning.

This meant:

* no specialization
* duplicated code
* difficult maintenance

---

# Solution

Introduce an **AgentProfile**.

Instead of placing configuration inside the agent class:

```text
MemoryAgent

↓

Hardcoded Prompt

Hardcoded Tools
```

We moved everything into a reusable profile.

---

# 2. AgentProfile

Created:

```text
src/
└── agent_profile.py
```

Implementation:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class AgentProfile:

    name: str

    description: str

    system_prompt: str

    planning_prompt: str

    reflection_prompt: str

    allowed_tools: list[str]
```

---

# Why `@dataclass(frozen=True)`?

Benefits:

* Less boilerplate
* Immutable
* Cleaner syntax
* Easy debugging

Profiles represent configuration, so they should not change while the application is running.

---

# 3. Agent Prompts

Created:

```text
src/
└── prompt/
    └── agent_prompt.py
```

Example:

```python
MEMORY_SYSTEM_PROMPT = """
You are a Memory Agent.

Responsibilities:

- Conversation history
- Long-term memory
- Summaries
- User preferences

Never answer programming questions.
"""
```

Likewise:

```python
CODING_SYSTEM_PROMPT
```

Planning and reflection prompts were added as placeholders for future implementation.

---

# 4. Agent Profiles

Created:

```text
src/
└── agents/
    └── profiles.py
```

Example:

```python
MEMORY_PROFILE = AgentProfile(
    name="memory",
    description="Handles memory tasks.",
    system_prompt=MEMORY_SYSTEM_PROMPT,
    planning_prompt=MEMORY_PLANNING_PROMPT,
    reflection_prompt=MEMORY_REFLECTION_PROMPT,
    allowed_tools=[
        "list_chats",
        "retrieve_memory",
        "conversation_summary"
    ]
)
```

A separate profile was also created for the Coding Agent.

---

# 5. BaseAgent Refactoring

Before:

Every specialized agent implemented its own constructor and execution logic.

After:

```python
class BaseAgent(ABC):

    def __init__(
        self,
        profile,
        ai_agent
    ):
        self.profile = profile
        self.ai_agent = ai_agent

    def execute(
        self,
        conversation_id,
        user_message
    ):
        return self.ai_agent.run(
            conversation_id,
            user_message,
            profile=self.profile
        )
```

Now every specialized agent inherits the same execution pipeline.

---

# 6. MemoryAgent

The class became much smaller.

Its only responsibility is deciding whether it should handle the request.

```python
class MemoryAgent(BaseAgent):

    def can_handle(...):
        ...
```

Execution is inherited from `BaseAgent`.

---

# 7. CodingAgent

Exactly the same design.

Only the routing logic differs.

Everything else is shared.

---

# 8. AIAgent Changes

Old:

```python
run(
    conversation_id,
    user_message
)
```

New:

```python
run(
    conversation_id,
    user_message,
    profile
)
```

The execution engine now knows which profile is active.

---

# 9. Prompt Builder

Instead of building prompts with one global system prompt, prompts are now created using the active profile.

Conceptually:

```python
build_prompt(
    profile.system_prompt,
    messages
)
```

This allows different agents to receive different instructions while sharing the same execution pipeline.

---

# 10. Planning Service

Planning now receives the active profile.

Conceptually:

```python
planning_service.create_plan(
    profile,
    messages
)
```

This prepares the system for agent-specific planning prompts.

---

# 11. Reflection Service

Reflection also becomes profile-aware.

Conceptually:

```python
reflection_service.review(
    profile,
    messages,
    answer
)
```

Different agents will eventually review answers using different criteria.

---

# 12. Tool Restrictions

Instead of exposing every tool to every agent:

```python
profile.allowed_tools
```

defines the tools available to that agent.

Example:

Memory Agent:

```text
list_chats
retrieve_memory
conversation_summary
```

Coding Agent:

```text
python_executor
code_search
documentation
```

This improves safety and specialization.

---

# 13. Verification

Verified successfully.

Console output:

```text
Routing to MemoryAgent

MemoryAgent selected

AgentProfile(
    name='memory',
    ...
)

conversation id 11
```

This confirmed:

* Router selected the correct agent.
* BaseAgent execution worked.
* Profile was injected successfully.
* Profile information reached the execution pipeline.

---

# Current Architecture

```text
                  API
                   │
                   ▼
             ChatService
                   │
                   ▼
        AgentOrchestrator
                   │
                   ▼
            RouterAgent
          ┌────────┴────────┐
          ▼                 ▼
    MemoryAgent      CodingAgent
          │                 │
          ▼                 ▼
    AgentProfile      AgentProfile
          │                 │
          └────────┬────────┘
                   ▼
               AIAgent.run()
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
 Planning    Reflection    Tool Loop
```

---

# Design Principles Learned

## Single Responsibility Principle (SRP)

* Router routes.
* Profile stores configuration.
* AIAgent executes.
* Specialized agents decide ownership.

---

## Open / Closed Principle (OCP)

Adding a new agent now requires:

1. Create a profile.
2. Create a small agent.
3. Register it.

No changes to the execution engine.

---

## Dependency Inversion Principle (DIP)

Agents depend on abstractions and shared execution rather than duplicating implementation.

---

# Interview Questions

## 1. What problem does an AgentProfile solve?

**Answer**

It separates an agent's identity and configuration from its execution logic, avoiding hardcoded prompts, tools, and behavior.

---

## 2. Why use `@dataclass(frozen=True)`?

**Answer**

It creates an immutable configuration object with minimal boilerplate, making profiles safer and easier to maintain.

---

## 3. Why move `execute()` into `BaseAgent`?

**Answer**

Because all specialized agents currently share the same execution pipeline. Only the routing logic differs.

---

## 4. Why pass the profile into `AIAgent.run()`?

**Answer**

It allows the execution engine to change prompts, planning, reflection, and available tools based on the active agent.

---

## 5. Why should tools be restricted by profile?

**Answer**

Each agent should only access tools relevant to its responsibilities, improving specialization and reducing unnecessary tool exposure.

---

## 6. How does this design support the Open/Closed Principle?

**Answer**

New agents can be added by creating a new profile and agent class without modifying the existing execution engine.

---

# Key Takeaways

* Agent identity should be represented as configuration, not hardcoded logic.
* `AgentProfile` becomes the single source of truth for prompts and tool permissions.
* `BaseAgent` now provides a shared execution pipeline.
* Specialized agents are lightweight and focused on routing decisions.
* `AIAgent` is now profile-driven, making one execution engine reusable for multiple agent types.
* The architecture is easier to extend and closer to production AI platforms.

---

# Tomorrow's Agenda

* Replace keyword-based routing with intelligent routing.
* Introduce an LLM-powered `RouterAgent`.
* Compare rule-based routing vs. model-based routing.
* Build a scalable routing strategy for future agents.

---

# Deliverable

By the end of today's session, the project achieved **true profile-driven multi-agent execution**, where agent behavior is determined by its profile rather than by duplicated code or shared hardcoded configuration.
