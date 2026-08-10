1. Why do we version prompts?

Prompts are part of the application's behavior. Changing a prompt can change model output just like changing code can change application behavior. Versioning allows us to track, compare, roll back, and evaluate prompt changes safely.

2. Why use exponential backoff?

Exponential backoff prevents clients from repeatedly hitting a temporarily unavailable service. Increasing the delay between attempts reduces load on the provider and gives transient failures time to recover.

3. Why add jitter?

Jitter introduces randomness into retry delays so many clients don't retry simultaneously, which helps prevent synchronized retry spikes or thundering-herd problems.

4. Why is context optimization important?

LLM context windows are finite, and larger prompts increase latency and token cost. Context optimization selects the most relevant information instead of sending the entire conversation, improving relevance, latency, and cost.

5. Why use retrieval instead of sending the entire history?

Retrieval allows the system to selectively bring relevant historical information into the context while keeping the prompt within a predictable budget.

6. Why use caching in an LLM application?

Caching reduces repeated LLM calls, which improves latency and reduces token usage and infrastructure cost. However, the cache key must account for the model, prompt version, context, tools, and other inputs that can affect the generated response.

7. Why use TTL?

TTL prevents stale responses from remaining in the cache indefinitely and provides a controlled freshness window.

8. Cache key generation is a caching concern; cache storage is a cache implementation concern; ChatService should orchestrate, not construct cache internals.


# Day 5 — Production AI Patterns

## 🎯 Goal

Build production-oriented AI patterns that improve:

* Reliability
* Context efficiency
* Latency
* Cost
* Maintainability

**Deliverable:** Production AI patterns implemented in the AI-SEP project.

---

# 1. Prompt Versioning

## Why Prompt Versioning?

Prompts are part of the application's behavior.

If we change a prompt from version 1 to version 2, the application's output can change.

Therefore, prompts should be treated like code.

### Key idea

```text
Prompt
  ↓
Version
  ↓
LLM
  ↓
Response
```

Instead of scattering prompts throughout the application, we use `PromptBuilder` to centralize prompt construction.

### Benefits

* Easier testing
* Easier rollback
* Reproducibility
* Debugging
* Prompt experimentation
* Production traceability

---

# 2. Retry Strategies

LLM/API calls can fail because of:

* Network failures
* Temporary provider errors
* Timeouts
* Rate limits
* Service availability problems

A production application should not immediately fail on every temporary error.

## Retry Pattern

```text
LLM Request
    ↓
Failure?
 ┌──┴──┐
 No    Yes
 ↓      ↓
Return  Retry
         ↓
      Backoff
         ↓
      Retry
```

## Exponential Backoff

Conceptually:

```text
Retry 1 → wait 1s
Retry 2 → wait 2s
Retry 3 → wait 4s
Retry 4 → wait 8s
```

Retries should have a maximum limit.

### Important

Do not blindly retry every error.

Permanent errors should fail immediately.

---

# 3. Context Optimization

The LLM receives context as part of its input.

More context means:

* More prompt tokens
* More computation
* Higher latency
* Higher cost

Therefore, context should be controlled.

Our architecture:

```text
ContextBuilder
      ↓
MemoryManager
      ↓
MemoryService
      ↓
Recent conversation context
```

---

## MemoryManager

Our current implementation trims conversation history:

```python
from src.config import MAX_CONTEXT_MESSAGES


class MemoryManager:

    def __init__(self, memory_service):
        self.memory_service = memory_service

    def trim_context(self, messages):
        return messages[-MAX_CONTEXT_MESSAGES:]

    def build_context(self, conversation_id):
        messages = self.memory_service.load_messages(
            conversation_id
        )

        return self.trim_context(messages)
```

Configuration:

```python
MAX_CONTEXT_MESSAGES = 10
```

### Important limitation

This is **message-based context optimization**, not token-based optimization.

For example:

```text
10 small messages → 500 tokens
10 large messages → 8,000 tokens
```

Both contain 10 messages.

A future advanced implementation can use a token budget.

---

# 4. Retrieval-Based Context

Our `ContextBuilder` already integrates retrieval.

```text
User Question
      ↓
RetrievalService
      ↓
Relevant memories
      ↓
ContextBuilder
      ↓
LLM
```

Instead of sending the entire historical conversation:

```text
Entire History
      ↓
     LLM
```

we prefer:

```text
User Question
      ↓
Relevant Information
      ↓
     LLM
```

This improves both context quality and cost efficiency.

---

# 5. Caching

Caching prevents unnecessary repeated LLM calls.

## Without Cache

```text
User
 ↓
LLM
 ↓
Response
```

Every request invokes the model.

## With Cache

```text
User
 ↓
Cache
 ├── HIT → Response
 │
 └── MISS
       ↓
      LLM
       ↓
     Cache
       ↓
    Response
```

### Benefits

* Lower latency
* Fewer LLM calls
* Lower token usage
* Lower infrastructure cost

---

# 6. Cache Abstraction

We created a cache interface:

```python
from abc import ABC, abstractmethod


class Cache(ABC):

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value, ttl=None):
        pass

    @abstractmethod
    def delete(self, key):
        pass
```

This keeps the application independent of the cache implementation.

---

# 7. MemoryCache

For development and testing, we implemented an in-memory cache.

```text
Cache
  ↑
MemoryCache
```

The cache supports:

* `get()`
* `set()`
* `delete()`
* TTL expiration

### TTL

TTL means **Time To Live**.

Example:

```python
cache.set(
    key,
    value,
    ttl=300
)
```

The value expires after 300 seconds.

---

# 8. Cache Key Generation

We created a separate cache-key utility instead of putting key-generation logic inside `MemoryCache` or `ChatService`.

Architecture:

```text
src/
└── cache/
    ├── cache.py
    ├── memory_cache.py
    └── cache_key.py
```

The key can be generated from:

* Model
* Messages
* Tools
* Prompt version

Example:

```python
import hashlib
import json


def make_cache_key(
    model,
    messages,
    tools=None,
    prompt_version=None
):
    payload = {
        "model": model,
        "messages": messages,
        "tools": tools,
        "prompt_version": prompt_version
    }

    raw = json.dumps(
        payload,
        sort_keys=True,
        default=str
    )

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()
```

### Why separate this?

`MemoryCache` should know:

> How to store and retrieve values.

`cache_key.py` should know:

> How to identify a cached request.

`ChatService` should not know cache implementation details.

---

# 9. Cache Testing

We installed and used `pytest`.

Basic cache behavior tested:

```text
GET → MISS
   ↓
SET
   ↓
GET → HIT
   ↓
DELETE
   ↓
GET → MISS
```

We also tested TTL:

```text
SET
 ↓
Wait
 ↓
Expired
 ↓
MISS
```

And cache-key consistency:

```text
Same input
    ↓
Same key
```

```text
Different input
    ↓
Different key
```

---

# 10. Cost Optimization

LLM cost is influenced by:

```text
Prompt Tokens
       +
Completion Tokens
       ↓
Total Token Usage
```

Our `TokenUsage` implementation tracks:

```python
TokenUsage(
    model=MODEL_NAME,
    prompt_tokens=...,
    completion_tokens=...,
    total_tokens=...,
    latency_ms=...
)
```

Even when using Ollama locally, these metrics are valuable because they represent:

* Computation
* Latency
* Resource consumption
* Scalability

---

# 11. Cost Optimization Techniques

## A. Reduce Context

```text
Less context
    ↓
Fewer prompt tokens
    ↓
Lower computation
```

Our `MemoryManager` helps with this.

---

## B. Retrieval Instead of Full History

```text
Entire history
      ↓
     ❌

Relevant memories
      ↓
     ✅
```

---

## C. Cache Repeated Requests

```text
Cache HIT
    ↓
No LLM call
```

---

## D. Limit Completion Tokens

Different tasks need different output sizes.

```text
Title generation → Small
Classification    → Small
Planning          → Small
Normal response   → Medium
Deep analysis     → Large
```

---

## E. Select Relevant Tools

Our planner already does:

```python
selected_tools = self.registry.get_selected_tools(
    plan.tools
)
```

Instead of sending every available tool to the LLM, we provide only relevant tools.

This reduces prompt size.

---

## F. Model Routing

Production systems can use different models for different tasks.

```text
                 Router
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
    Small Model Medium Model Large Model
    Simple task Normal task  Complex task
```

Your existing Router Agent and Agent Profiles provide a foundation for this architecture.

---

# 12. Token Budget

A production AI system can define a request budget:

```text
Maximum Request Budget
          │
    ┌─────┼─────┐
    ↓     ↓     ↓
 System Context Completion
```

Example:

```text
Total budget = 8,000 tokens

System      = 1,000
Context     = 4,000
Tools       = 1,000
Completion  = 2,000
```

The exact numbers depend on the application and model.

---

# 13. Cost Optimization Loop

Optimization should be measurable.

```text
Measure
   ↓
Identify expensive operation
   ↓
Optimize
   ↓
Measure again
```

Useful metrics include:

* Average prompt tokens
* Average completion tokens
* Total tokens
* Average latency
* Cache hit rate
* LLM calls per request
* Retrieval size

---

# 14. Final Day 5 Architecture

```text
                       AI AGENT
                           │
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
   Prompt Versioning   Context           Cache
                      Optimization
          │                │                │
          └────────────────┼────────────────┘
                           ↓
                       Provider
                           │
                 ┌─────────┴─────────┐
                 ↓                   ↓
              Retry              Token Usage
             Strategy             Tracking
```

---

# 15. Day 5 Checklist

| Topic                | Status                 |
| -------------------- | ---------------------- |
| Prompt Versioning    | ✅ Complete             |
| Retry Strategies     | ✅ Complete             |
| Context Optimization | ✅ Complete             |
| Caching              | ✅ Implemented & Tested |
| Cost Optimization    | ✅ Complete             |

## 🎯 Day 5 Deliverable

**Production AI Patterns — Completed**

The AI-SEP project now has production-oriented patterns for:

* Reliable model calls
* Controlled context
* Retrieval
* Caching
* Token accounting
* Cost optimization
* Prompt maintainability

---

# 🧠 Interview Takeaways

### Q: Why is context optimization important?

> Large context increases token consumption, latency, and computational cost. We should send only the information relevant to the current task.

### Q: Why use caching with LLMs?

> Caching avoids repeated model calls for identical or safely reusable requests, reducing latency and token consumption.

### Q: Why shouldn't cache-key generation live inside MemoryCache?

> `MemoryCache` should handle storage mechanics. Key generation is a separate concern, allowing the cache implementation to be replaced without changing business logic.

### Q: How do you optimize LLM cost?

> Control context size, retrieve only relevant information, cache reusable results, limit completion tokens, select only required tools, use appropriate models for different tasks, and monitor token usage.

### Q: What metrics would you monitor?

> Prompt tokens, completion tokens, total tokens, latency, cache hit rate, model usage, and LLM calls per request.

---

# 🚀 Next Session — Day 6: Deployment

We will move from **production AI patterns** to **production deployment**.

Topics:

1. Docker
2. Docker Compose
3. Environment configuration
4. Production setup

**Deliverable:** A deployable AI-SEP application.
