# AI Bootcamp - Day Notes
## Topic: AI Agent Architecture & Clean Architecture

---

# 1. AI Agent

## Definition

An AI Agent is an LLM-powered software component that can:

- Reason
- Plan
- Execute tools
- Observe tool results
- Continue reasoning
- Produce the final response

Unlike a chatbot, an AI Agent can perform actions to accomplish a user's goal.

---

# 2. AI Chatbot vs AI Agent

## AI Chatbot

- Generates text only
- Usually one LLM call
- Cannot perform actions
- Ends after generating a response

Example:

User:
> Explain Python decorators.

↓

LLM

↓

Answer

---

## AI Agent

- Reasons
- Calls tools
- Executes APIs
- Can perform multiple iterations
- Produces the final answer after completing the task

Example:

User:
> Rename my chat and show all conversations.

↓

LLM

↓

rename_chat()

↓

Tool Result

↓

LLM

↓

list_chats()

↓

Tool Result

↓

LLM

↓

Final Answer

---

# 3. Agent Loop

The Agent repeatedly performs the following cycle:

Reason

↓

Plan

↓

Tool Call

↓

Observe Result

↓

Reason Again

↓

Repeat until no tool is required

This is called the **Agent Loop**.

---

# 4. Why ChatService Became Too Large

Our ChatService was responsible for:

- Memory
- Prompt Building
- Provider Calls
- Tool Execution
- Agent Loop
- Tool Reasoning
- Response Generation

This violates the **Single Responsibility Principle (SRP)**.

---

# 5. Refactoring to Clean Architecture

Old Architecture

API

↓

ChatService

├── Memory

├── Prompt Builder

├── Tool Loop

├── Provider

└── Tool Execution

---

New Architecture

API

↓

ChatService

↓

AIAgent

↓

Provider

↓

LLM

---

# 6. Responsibility of ChatService

ChatService should only manage conversations.

Responsibilities:

- Save user message
- Load chat history
- Save assistant response
- Generate chat title
- Create/Delete/Rename conversations
- Call the Agent

It should NOT contain AI reasoning logic.

---

# 7. Responsibility of AIAgent

The Agent owns the complete reasoning workflow.

Responsibilities:

- Build prompts
- Call the LLM
- Decide whether a tool is needed
- Execute tool calls
- Observe tool results
- Continue reasoning
- Return the final response

The Agent owns the entire **Reason → Act → Observe** loop.

---

# 8. Why execute_tool_call() Belongs in Agent

Tool execution is part of the Agent's reasoning cycle.

Reason

↓

Tool Call

↓

Execute Tool

↓

Observe Result

↓

Continue Reasoning

Therefore, `execute_tool_call()` belongs in the Agent rather than ChatService.

---

# 9. Dependency Inversion Principle (DIP)

The Agent should not know which LLM provider it is using.

Bad:

if provider == "ollama":
    ...

elif provider == "openai":
    ...

elif provider == "claude":
    ...

Good:

reply = provider.chat(messages)

The Agent depends only on the Provider interface.

Benefits:

- Provider-independent
- Easy to switch LLMs
- Easier testing
- Better maintainability

---

# 10. Provider-Agnostic Design

The Agent should work with any provider.

Examples:

- Ollama
- OpenAI
- Anthropic Claude
- Gemini
- Azure OpenAI

Only the Provider implementation changes.

The Agent remains unchanged.

---

# 11. Production Architecture

               REST API
                  │
                  ▼
            ChatService
                  │
                  ▼
              AIAgent
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
 Prompt Builder         Tool Executor
                  │
                  ▼
             Provider Interface
                  │
      ┌───────────┼────────────┐
      ▼           ▼            ▼
   Ollama      OpenAI       Claude

---

# 12. Interview Definition - AI Agent

**30-Second Answer**

>An AI Agent is an LLM-powered system that can reason, plan, execute external tools, observe the results, and iteratively work toward completing a user's goal. Unlike a chatbot that only generates text, an AI Agent can perform actions and make multi-step decisions before producing the final response.

---

# 13. Interview Definition - Dependency Inversion

>The Agent should depend only on a provider interface (for example, `provider.chat()`), not on specific implementations like Ollama or OpenAI. This makes the architecture provider-agnostic, extensible, and easier to maintain.

---

# 14. Key Design Principles Learned Today

- Single Responsibility Principle (SRP)
- Dependency Inversion Principle (DIP)
- Separation of Concerns
- Provider-Agnostic Architecture
- Agent-Based Design
- Multi-Step Reasoning
- Tool Execution Loop
- Clean Architecture

---

# 15. Interview Questions Covered

### Q1. What is an AI Agent?

Answered.

---

### Q2. Difference between AI Chatbot and AI Agent?

Answered.

---

### Q3. Why should execute_tool_call() belong to the Agent?

Because tool execution is part of the Agent's reasoning cycle.

---

### Q4. Why shouldn't the Agent know whether it is using OpenAI or Ollama?

To follow Dependency Inversion Principle and make the Agent provider-independent.

---

### Q5. Why shouldn't ChatService contain the AI loop?

Because ChatService manages conversations, while the Agent owns the AI workflow.

---

# 16. Architecture Takeaway

**ChatService = Conversation Manager**

- Memory
- Conversations
- Persistence

**AIAgent = Brain**

- Planning
- Reasoning
- Tool Calling
- Decision Making
- Final Response

**Provider = LLM Connector**

- Sends prompts
- Receives responses

**Registry = Tool Catalog**

- Stores tools
- Executes tools

---



# AI Engineer Bootcamp
## Day 4 - Agent Memory & Context Management

---

# Learning Objectives

Today we learned how production AI systems manage memory and context.

By the end of the lesson, we achieved:

- Understand why LLMs are stateless
- Separate storage from memory strategy
- Build a MemoryManager
- Move memory ownership into AIAgent
- Understand context engineering
- Learn memory strategies
- Understand token budgeting

---

# 1. LLMs are Stateless

An LLM does **not** remember previous conversations.

Every request is independent.

```
User
  |
  v
Application
  |
Build Context
  |
  v
LLM
```

The application is responsible for providing conversation history.

---

# 2. MemoryService vs MemoryManager

## MemoryService

Responsible for persistence.

Examples:

- SQLite
- PostgreSQL
- Redis

Responsibilities:

- Save messages
- Load messages
- Create conversations
- Delete conversations

Question it answers:

> "Where is memory stored?"

---

## MemoryManager

Responsible for memory strategy.

Responsibilities:

- Load conversation history
- Select useful messages
- Trim context
- Build final context

Question it answers:

> "What information should the LLM receive?"

---

# 3. New Architecture

Before

```
ChatService
    |
MemoryService
    |
Provider
```

After

```
ChatService
      |
      v
   AIAgent
      |
+-----+-------------------+
|                         |
MemoryManager        ToolManager
      |
MemoryService
      |
SQLite
```

---

# 4. AIAgent Owns Memory

Old Flow

```
ChatService

Load Memory

Provider.chat()

Save Response
```

New Flow

```
ChatService
      |
      v
AIAgent

Load Context

Save User Message

Reason

Execute Tools

Generate Response

Save Assistant Response
```

The Agent now owns the complete AI lifecycle.

---

# 5. Context Engineering

Prompt Engineering focuses on writing better prompts.

Context Engineering focuses on building the complete input sent to the LLM.

Production Context

```
System Prompt

+

Conversation Summary

+

Recent Messages

+

Retrieved Documents

+

Tool Results

+

Current User Question
```

The prompt is only one part of the context.

---

# 6. Memory Strategies

## Sliding Window Memory

Keep only the latest messages.

Example

```
Messages 1-100

↓

Keep

91-100
```

Implementation

```python
return messages[-10:]
```

Advantages

- Easy
- Fast
- Low cost

Disadvantages

- Forgets older information

---

## Summary Memory

Old conversations are summarized.

Example

```
Summary

- User is learning AI Engineering
- Uses Python
- Built an Enterprise AI Chatbot
```

Then context becomes

```
Summary

+

Recent Messages
```

Advantages

- Long-term memory
- Lower token usage

---

## Hybrid Memory

Most production systems use

```
Summary

+

Recent Messages
```

This balances context retention and token efficiency.

---

## Retrieval Memory

Instead of loading recent messages,

retrieve the most relevant messages using semantic search.

This is implemented using

- Embeddings
- Vector Databases
- RAG

---

# 7. Token Budgeting

Models have limited context windows.

Example

```
8000 Tokens
```

Both input and output share this limit.

Example

```
Input

6000

+

Output

2000

=

8000
```

---

## Example Token Allocation

```
System Prompt      800

Conversation      1800

Retrieved Docs    1800

Tool Results       600

Current Question   400

Safety Buffer      600
```

Every component has its own budget.

---

# 8. Why Count Tokens Instead of Messages?

Bad

```
Last 10 Messages
```

Good

```
Use messages until token budget is exhausted
```

Production systems budget tokens, not message count.

---

# 9. Future MemoryManager

Current

```python
messages[-10:]
```

Future

```
Load Summary

↓

Load Recent Messages

↓

Retrieve Documents

↓

Count Tokens

↓

Build Context

↓

Send to LLM
```

MemoryManager evolves into a Context Builder.

---

# Architecture After Today's Refactoring

```
                User
                  |
             ChatService
                  |
                  v
               AIAgent
                  |
      +-----------+------------+
      |                        |
 MemoryManager          Tool Registry
      |
 MemoryService
      |
SQLite
      |
 Provider
      |
     LLM
```

---

# Interview Questions

### Why is an LLM stateless?

Because it does not retain previous requests.
The application must send conversation history with every request.

---

### MemoryService vs MemoryManager?

MemoryService stores data.

MemoryManager decides what information should be sent to the LLM.

---

### Why should AIAgent own memory?

Because memory is part of the AI reasoning lifecycle.
ChatService should only coordinate application flow.

---

### Prompt Engineering vs Context Engineering?

Prompt Engineering improves instructions.

Context Engineering manages every piece of information sent to the model.

---

### Why isn't `messages[-10:]` enough?

Because messages have different token sizes and important information may exist much earlier in the conversation.

---

### Why use token budgeting?

Because LLMs limit tokens, not message count.

---

# What We Built Today

✅ MemoryManager

✅ Agent owns context

✅ Agent owns persistence

✅ Cleaner ChatService

✅ Context Engineering

✅ Memory Strategies

✅ Token Budgeting

---

# Next Lesson

## Long-Term Memory & RAG

Topics

- Embeddings
- Vector Representation
- Similarity Search
- Vector Database
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- Integrating RAG into MemoryManager