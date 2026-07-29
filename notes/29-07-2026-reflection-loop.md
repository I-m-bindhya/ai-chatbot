1. Why is reflection useful if the same LLM performs both steps?

The model operates under different objectives in each pass. During generation it focuses on producing an answer. During reflection it evaluates that answer against the user's request and available context, looking for omissions, contradictions, or reasoning mistakes. Separating those objectives often produces higher-quality results than trying to do both simultaneously.

2. What is a Plan?

A plan is simply a sequence of smaller tasks.

3. Tool calling answers:

"What tool should I use next?"

Planning answers:

"What's the overall strategy for solving this task?"


# AI Engineering Bootcamp
# Day 2 — Advanced Agent (Completed)
**Date:** 29-Jul-2026

---

# Goal

Today's goal was to transform our chatbot into a production-style AI Agent by introducing planning, reflection, prompt architecture, and proper error handling.

---

# Architecture Before

```
User
   │
   ▼
ChatService
   │
   ▼
LLM
   │
   ▼
Answer
```

---

# Architecture After

```
                   User
                     │
                     ▼
               ChatService
                     │
                     ▼
                 AIAgent
                     │
     ┌───────────────┼────────────────┐
     ▼               ▼                ▼
Planning        PlanExecutor      Reflection
     │               │
     ▼               ▼
PromptBuilder   ToolRegistry
                     │
         ┌───────────┴────────────┐
         ▼                        ▼
    RetrievalService        ChatTools
         │
         ▼
      Qdrant
```

---

# 1. Reflection Service

## Purpose

Before returning the final answer, the AI reviews its own response.

Instead of:

```
Question
    ↓
Answer
```

we now have:

```
Question
    ↓
Answer
    ↓
Reflection
    ↓
Improved Answer
```

---

## Reflection Prompt

Reflection is just another system prompt.

Example:

```
SYSTEM_PROMPT

REFLECTION_PROMPT

Conversation

Assistant Answer
```

The LLM evaluates whether the answer is:

- Correct
- Complete
- Helpful
- Missing information

---

# 2. Planning Service

Instead of immediately calling tools, the AI first creates a plan.

Example:

User:

```
List all my conversations and analyze them.
```

Old chatbot:

```
LLM guesses what to do.
```

New Agent:

```
User
    ↓
Planning
    ↓
Execution Plan
    ↓
Plan Executor
    ↓
Tools
    ↓
Final Answer
```

---

# ExecutionPlan

```python
class PlanStep:

    id: int

    action: str

    reason: str
```

Example:

```json
{
    "steps":[
        {
            "id":1,
            "action":"list_conversations",
            "reason":"Need all conversations."
        },
        {
            "id":2,
            "action":"analyze_history",
            "reason":"Need to summarize."
        }
    ]
}
```

---

# Why Machine-Friendly Actions?

Instead of:

```
"List all conversations"
```

Use:

```
list_conversations
```

because the executor can directly match:

```python
match step.action:
```

or

```python
handlers[action]
```

Machine-friendly actions eliminate ambiguity.

---

# 3. Plan Executor

The executor converts plans into actual work.

```
ExecutionPlan

↓

PlanExecutor

↓

Execute Tool

↓

Collect Results

↓

Return Context
```

The LLM decides **what** to do.

The executor decides **how** to do it.

---

# 4. Prompt Builder V2

## Old Design

```
build_tool_prompt()

build_summary_prompt()

build_planning_prompt()

build_reflection_prompt()

build_response_prompt()
```

Lots of duplicated code.

---

## New Design

One generic builder.

```python
build(
    task_prompt,
    messages
)
```

Everything else becomes a wrapper.

```python
build_tool_prompt()

↓

build(
    TOOL_PROMPT,
    messages
)
```

Advantages:

- Less duplication
- Easier maintenance
- Cleaner architecture
- Easy to add new prompt types

---

# Prompt Separation

Permanent behavior:

```
SYSTEM_PROMPT
```

Current task:

```
PLANNING_PROMPT

REFLECTION_PROMPT

TOOL_PROMPT

SUMMARY_PROMPT
```

The builder combines them.

```
SYSTEM_PROMPT

+

TASK_PROMPT

+

Conversation
```

---

# 5. Error Handling

Every layer throws only the errors it understands.

Instead of:

```
Exception
```

Use domain-specific exceptions.

```
AgentError
    │
    ├── ProviderError
    ├── RetrievalError
    ├── ToolExecutionError
    ├── PlanningError
    └── ReflectionError
```

---

## Error Flow

Example:

```
Qdrant Down

↓

RetrievalService

↓

RetrievalError

↓

AIAgent

↓

Friendly Response
```

---

## Provider Example

```
Ollama Down

↓

ProviderError

↓

AgentError

↓

AIResponse
```

---

## Why Custom Exceptions?

Advantages:

- Easier debugging
- Better logging
- Clear ownership
- Cleaner architecture
- Easier retries later

---

# Design Principle Learned

Lower layers

↓

Raise Exceptions

Higher layers

↓

Handle Exceptions

---

# Current Agent Pipeline

```
User Message
      │
      ▼
Context Builder
      │
      ▼
Planning
      │
      ▼
Execution Plan
      │
      ▼
Plan Executor
      │
      ▼
Tool Calls
      │
      ▼
Response Generation
      │
      ▼
Reflection
      │
      ▼
Final Answer
```

---

# What We Built So Far (Entire Bootcamp)

## Foundation

- Provider abstraction
- Memory Service
- SQLite
- Chat Service
- Agent
- Tool Registry
- Tool Adapter

---

## Memory

- Long-term memory
- Semantic search
- Qdrant
- Embeddings
- Memory importance
- Conversation summaries

---

## Retrieval

- Embedding Service
- Retrieval Service
- Vector Store
- Context Builder

---

## Advanced Agent

- Planning
- Reflection
- Prompt Builder V2
- Plan Executor
- Error Handling

---

# Interview Questions

## Beginner

### Q1. Why do we need a PromptBuilder?

**Answer**

To centralize prompt creation, reduce duplication, and make prompts reusable and maintainable.

---

### Q2. Why separate SYSTEM_PROMPT from PLANNING_PROMPT?

**Answer**

`SYSTEM_PROMPT` defines the assistant's permanent behavior, while task prompts define the current task (planning, reflection, tool use, summarization). Separating them makes prompts modular and easier to maintain.

---

### Q3. What is an Execution Plan?

**Answer**

A structured list of actions the agent should perform before generating the final answer.

---

### Q4. Why use machine-friendly actions?

Instead of:

```
"List all conversations"
```

Use:

```
list_conversations
```

because code can execute deterministic action names.

---

### Q5. What is the responsibility of PlanExecutor?

It executes the plan created by the planner by invoking tools or actions and collecting the results.

---

# Intermediate

### Q6. Why shouldn't the LLM directly execute tools?

Because planning and execution are separate concerns. The LLM decides *what* should happen, while the application controls *how* it happens. This improves reliability, security, and testability.

---

### Q7. Why use custom exceptions?

They provide domain-specific context, simplify debugging, and allow different recovery strategies for provider, retrieval, or tool failures.

---

### Q8. Where should exceptions be handled?

Exceptions should be raised where they occur and handled at the orchestration layer (`AIAgent`), which decides how to recover or respond.

---

### Q9. Why not catch `Exception` everywhere?

It hides the real cause of failures, creates duplicated error handling, and makes debugging much harder.

---

### Q10. Why is PromptBuilder considered scalable?

Because new prompt types can be added by creating new prompt templates without duplicating prompt construction logic.

---

# Senior-Level Questions

### Q11. Why separate planning from execution?

Because planners determine intent, while executors perform deterministic actions. This separation makes the system easier to extend, test, and secure.

---

### Q12. How would you implement retries?

Retries belong in infrastructure layers such as the provider or retrieval service, not inside business logic like `AIAgent`, because those layers understand transient failures.

---

### Q13. What is the Single Responsibility Principle in today's architecture?

Each component has one responsibility:

- PlanningService → Create plans
- PlanExecutor → Execute plans
- PromptBuilder → Build prompts
- RetrievalService → Retrieve memories
- ToolRegistry → Execute tools
- AIAgent → Orchestrate the workflow

---

### Q14. Why are layered exceptions important?

They preserve context, improve logging, and allow different recovery strategies while keeping business logic clean.

---

# Key Takeaways

- Planning should happen before execution.
- Reflection improves answer quality.
- Prompt construction should be reusable.
- Prompt templates should be separated from builder logic.
- Exceptions should be domain-specific.
- Orchestrators coordinate; services perform specialized tasks.
- Good architecture separates **what to do** from **how to do it**.

---

# Day 2 Status

✅ Reflection Service

✅ Planning Service

✅ ExecutionPlan

✅ Plan Executor

✅ Prompt Builder V2

✅ Production-style Error Handling

---

# Next Session Preview

- Reflection retry loop (self-correction)
- Action Registry (replace `match`)
- Better tool selection
- Production logging
- Observability
- Agent evaluation

The next step is to make the agent not only structured, but capable of improving its own behavior.