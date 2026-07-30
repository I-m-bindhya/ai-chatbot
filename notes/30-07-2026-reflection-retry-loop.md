1. Why shouldn't every tool be exposed to the LLM?

Answer:
Because it increases prompt size, token usage, latency, and the likelihood of the model selecting an inappropriate tool. Restricting the available tools simplifies the model's decision-making.

2. What is the benefit of planning tool selection?

Answer:
The planner identifies the capabilities needed for the task, allowing the agent to expose only relevant tools. This improves efficiency, scalability, and accuracy.


3. Why separate planning from execution?

Answer:
Planning decides what should happen. Execution performs those decisions. This separation makes the system easier to maintain, test, and extend.

4. Where should tool selection happen?

Answer:
In the planning stage, before the provider is called. The planner determines which tools are relevant, and the agent exposes only those tools to the model.


5. What design pattern does this follow?

Answer:
This follows the Planner–Executor pattern, where planning produces an execution strategy and execution carries it out. Restricting tool exposure is an optimization within that architecture.


Is this mandatory?

For a production system with a handful of tools, it's a useful optimization. However, once you have dozens or hundreds of tools, dynamic tool selection becomes increasingly valuable because it keeps prompts smaller, reduces inference costs, and improves reliability. Since your goal is to build a production-quality AI engineering project, it's a worthwhile enhancement.


# AI Engineering Bootcamp
# Day 3 — Production Agent Workflow

**Date:** 30 July 2026

---

# Goal

Transform the AI Agent from a linear chatbot into a production-style workflow engine.

Today's focus:

- Reflection Retry Loop
- Smart Tool Selection
- Agent State Machine

---

# 1. Reflection Retry Loop

## Why?

LLMs sometimes produce:

- Incorrect answers
- Incomplete answers
- Hallucinations

Instead of immediately returning the first response, let the AI review its own answer.

---

## Workflow

```text
Generate Answer
        │
        ▼
 Reflection Review
        │
        ├───────────────┐
        │               │
   Approved         Not Approved
        │               │
        ▼               ▼
     Return        Improve Answer
                        │
                        ▼
                Reflection Again
```

---

## Components

### ReflectionService

Responsibilities:

- Review answer
- Generate feedback
- Improve answer

---

## Retry Loop

```text
Generate
      │
      ▼
Review
      │
      ├──── Approved ─────► Return
      │
      ▼
Improve
      │
      ▼
Review Again
```

---

## Advantages

- Higher quality answers
- Self-correction
- Production-grade reasoning

---

# 2. Smart Tool Selection

## Previous Design

Every request exposed every tool.

```text
LLM

Calculator
Weather
Memory
Chats
Search
GitHub
Filesystem
...
```

Problems:

- Large prompts
- More tokens
- Slower
- Wrong tool selection

---

## New Design

Planning decides required tools.

```text
User
 │
 ▼
Planning
 │
 ▼
Selected Tools
 │
 ▼
LLM
```

---

## ExecutionPlan

```python
class ExecutionPlan(BaseModel):

    steps: list[PlanStep]

    tools: list[str]
```

---

## Example

```json
{
    "steps":[
        {
            "id":1,
            "action":"list_conversations",
            "reason":"User requested conversations."
        }
    ],
    "tools":[
        "list_chats"
    ]
}
```

---

## ToolRegistry

Added:

```python
get_selected_tools()
```

Instead of

```python
registry.get_tools()
```

Now:

```python
registry.get_selected_tools(plan.tools)
```

---

## Benefits

- Lower token usage
- Faster inference
- Better tool accuracy
- Production scalability

---

# 3. Agent State Machine

## Previous Flow

```text
Build Context

↓

Planning

↓

Execute

↓

Tool Loop

↓

Generate

↓

Reflect

↓

Save
```

Everything existed inside one long function.

---

## New Workflow

```text
START

↓

LOAD_CONTEXT

↓

PLAN

↓

EXECUTE_PLAN

↓

TOOL_LOOP

↓

GENERATE_RESPONSE

↓

REFLECT

↓

SAVE_RESPONSE

↓

END
```

---

## AgentState

```python
class AgentState(str, Enum):

    LOAD_CONTEXT = "load_context"

    PLAN = "plan"

    EXECUTE_PLAN = "execute_plan"

    TOOL_LOOP = "tool_loop"

    GENERATE_RESPONSE = "generate_response"

    REFLECT = "reflect"

    SAVE_RESPONSE = "save_response"

    END = "end"
```

---

## State Loop

```python
while state != AgentState.END:

    if state == AgentState.LOAD_CONTEXT:
        ...

    elif state == AgentState.PLAN:
        ...

    elif state == AgentState.EXECUTE_PLAN:
        ...

    elif state == AgentState.TOOL_LOOP:
        ...

    elif state == AgentState.GENERATE_RESPONSE:
        ...

    elif state == AgentState.REFLECT:
        ...

    elif state == AgentState.SAVE_RESPONSE:
        ...
```

---

## Why State Machines?

Instead of writing

```python
if ...
elif ...
elif ...
elif ...
```

the workflow becomes explicit.

Benefits:

- Easier debugging
- Easier testing
- Easier scaling
- Easier retries
- Easier checkpoints

---

# Architecture After Today

```text
                 User
                   │
                   ▼
            Context Builder
                   │
                   ▼
           Planning Service
                   │
                   ▼
            Execution Plan
           ┌────────┴────────┐
           ▼                 ▼
    Plan Executor     Tool Selection
           │                 │
           └────────┬────────┘
                    ▼
               Tool Loop
                    ▼
          Response Generator
                    ▼
          Reflection Service
                    ▼
             Memory Service
           ┌────────┴────────┐
           ▼                 ▼
       SQLite            Qdrant
```

---

# Files Added / Updated

## New

```
src/agents/agent_state.py
```

---

## Updated

```
AIAgent
PlanningService
ToolRegistry
PromptBuilder
ReflectionService
ExecutionPlan
```

---

# Production Concepts Learned

- Reflection Loop
- Retry Strategy
- Workflow Engine
- State Machine
- Tool Selection
- Planner → Executor Pattern
- Agent Orchestration

---

# Interview Questions

## 1. Why should an AI agent use a Reflection Loop?

**Answer**

To review and improve its own response before returning it to the user, reducing hallucinations and improving answer quality.

---

## 2. Why shouldn't every tool be exposed to the LLM?

**Answer**

Exposing all tools increases prompt size, token usage, latency, and the likelihood of selecting the wrong tool. Limiting the tool set simplifies the model's decision.

---

## 3. What is Smart Tool Selection?

**Answer**

The planner determines which tools are required for the current task, and the agent exposes only those tools to the LLM.

---

## 4. What is a State Machine?

**Answer**

A State Machine models the agent as a sequence of well-defined states, where each state performs a single responsibility and transitions to the next state.

---

## 5. Why are State Machines useful in AI agents?

**Answer**

They make workflows easier to understand, debug, test, extend, and recover from failures compared to large procedural methods.

---

## 6. Difference between Planner and Executor?

| Planner | Executor |
|----------|----------|
| Decides what to do | Performs the work |
| Produces execution steps | Executes execution steps |
| High-level reasoning | Operational logic |

---

## 7. Why separate planning from execution?

**Answer**

It follows the Separation of Concerns principle, making the system easier to maintain, extend, and test. The planner focuses on reasoning, while the executor focuses on carrying out the plan.

---

# Key Takeaways

- Reflection improves answer quality through self-review.
- Planning should determine the minimum required tool set.
- State Machines produce cleaner and more maintainable workflows.
- Separating planning, execution, and orchestration leads to production-ready AI agent architectures.

---

# Today's Achievement

✅ Reflection Retry Loop

✅ Smart Tool Selection

✅ Agent State Machine

You now have a **production-style AI agent workflow** with planning, selective tool exposure, state-driven orchestration, memory, retrieval, and reflection.