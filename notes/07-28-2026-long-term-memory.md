1. Why do you use a similarity threshold?

"Vector databases always return the nearest neighbors, even when none are truly relevant. A similarity threshold filters out weak matches so that only high-confidence memories are added to the prompt. This reduces hallucinations and improves response accuracy."

2. Why not index every message?

Not every conversation is useful as long-term memory. Indexing greetings, acknowledgements, or casual chat increases storage, slows retrieval, and introduces irrelevant context. We use a memory importance layer to persist only meaningful user facts and preferences.

3. Why separate SQLite and Qdrant?

SQLite stores the complete conversation history and serves as the source of truth. Qdrant stores only important semantic memories used for retrieval. This keeps vector search efficient while preserving the full chat history for auditing and replay.

4. Why introduce a SummaryService instead of putting the code into ChatService?

ChatService is responsible for the chat workflow. Summarization is a separate business capability involving loading messages, generating a summary, persisting it, and indexing it. Moving that logic into SummaryService keeps responsibilities separated, improves testability, and allows the summarization strategy to evolve independently

# AI Engineering Bootcamp
## Day 8 - Long-Term Memory Improvements & Memory Summarization

---

# Goal

Today we completed the production memory architecture by improving retrieval quality and implementing conversation summarization.

---

# Topics Covered

- Improve Retrieval Quality
- Memory Importance Filtering
- Memory Summarization
- SQLite UPSERT
- Production Memory Architecture

---

# 1. Improve Retrieval Quality

## Previous Retrieval

```text
Question
    │
    ▼
Embedding
    │
    ▼
Vector Search
    │
    ▼
Top 5 Memories
```

The retrieved memories were simply the nearest vectors.

---

## RetrievalService

```python
vector = embedding_service.embed(question)

return vector_store.search(
    vector,
    limit=5
)
```

Responsibilities:

- Convert question into embedding
- Search Qdrant
- Return relevant memories

---

# 2. Memory Importance Filtering

Not every message should become long-term memory.

Examples that SHOULD NOT be stored:

- Hi
- Hello
- Thanks
- Bye
- Good Morning
- Welcome

Examples that SHOULD be stored:

- My name is Bindhya
- I bought my laptop in 2024
- My favourite language is Python
- I work as a Backend Developer

Purpose:

- Reduce vector database size
- Improve retrieval accuracy
- Reduce embedding cost
- Avoid storing noise

---

# 3. Memory Summarization

## Why?

Conversation history keeps growing forever.

Instead of sending hundreds of messages to the LLM:

```
500 Messages
```

Compress them into:

```
Conversation Summary
```

Advantages:

- Lower token usage
- Lower cost
- Faster inference
- Better long-term memory

---

# SummaryService

Responsibilities:

- Load conversation messages
- Generate summary
- Save summary
- Index summary into Qdrant

Architecture:

```
Messages
    │
    ▼
SummaryService
    │
    ▼
LLM Summary
    │
    ├── Save to SQLite
    └── Save to Qdrant
```

---

# SummaryService Implementation

```python
class SummaryService:

    def generate_summary(
        self,
        conversation_id
    ):

        messages = self.memory_service.load_messages(
            conversation_id
        )

        summary = self.provider.generate_summary(
            messages
        )

        summary_id = self.memory_service.save_summary(
            conversation_id,
            summary
        )

        self.indexing_service.index(
            summary_id,
            summary,
            {
                "conversation_id": conversation_id,
                "type": "summary"
            }
        )

        return summary
```

---

# Summary Table

```sql
CREATE TABLE summary(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    conversation_id INTEGER NOT NULL UNIQUE,

    summary TEXT NOT NULL,

    FOREIGN KEY(conversation_id)
    REFERENCES conversations(id)
)
```

Key idea:

One conversation should have one active summary.

---

# SQLite UPSERT

Instead of checking:

```python
if exists:
    update()
else:
    insert()
```

SQLite can do both in one statement.

```sql
INSERT INTO summary(
    conversation_id,
    summary
)
VALUES (?, ?)

ON CONFLICT(conversation_id)

DO UPDATE SET

summary = excluded.summary;
```

Benefits:

- Cleaner code
- Atomic operation
- Production-ready
- Avoids duplicate summaries

---

# Why UNIQUE?

```sql
conversation_id UNIQUE
```

Without UNIQUE:

```
Conversation 11

Summary 1
Summary 2
Summary 3
Summary 4
```

With UNIQUE:

```
Conversation 11

Latest Summary
```

---

# Small Improvement Identified

Current code:

```python
return self.cursor.lastrowid
```

Issue:

During UPDATE, `lastrowid` does not represent the updated summary row.

Better approach:

```python
SELECT id
FROM summary
WHERE conversation_id = ?
```

Return the actual summary ID after the UPSERT.

---

# Memory Architecture

```
User Message
      │
      ▼
SQLite Messages
      │
      ▼
Importance Filter
      │
      ▼
Embedding
      │
      ▼
Qdrant
      │
      ▼
Retrieval
      │
      ▼
Context Builder
      │
      ▼
LLM
      │
      ▼
SummaryService
      │
      ├── SQLite Summary
      └── Qdrant Summary
```

---

# Architecture Built So Far

```
API
 │
 ▼
ChatService
 │
 ├── MemoryService
 │
 ├── AIAgent
 │
 ├── ContextBuilder
 │
 ├── RetrievalService
 │
 ├── EmbeddingService
 │
 ├── IndexingService
 │
 ├── Qdrant
 │
 ├── MemoryImportanceService
 │
 └── SummaryService
```

---

# Interview Questions

### Why store summaries?

- Reduce token usage
- Preserve long-term context
- Improve retrieval
- Lower inference cost

---

### Why use UPSERT?

- Single SQL statement
- Atomic operation
- Prevent duplicate summaries
- Simpler than manual INSERT/UPDATE logic

---

### Why keep summaries in a separate table?

Because summaries are derived knowledge, not individual chat messages. Separating them improves data modeling and allows independent retrieval and maintenance.

---

# Today's Achievement

✅ Improved semantic retrieval

✅ Implemented memory importance filtering

✅ Designed SummaryService

✅ Stored summaries in SQLite

✅ Indexed summaries into Qdrant

✅ Implemented SQLite UPSERT

✅ Completed the production memory subsystem

---

# Next Session

## ReflectionService

The agent will begin evaluating its own answers before returning them.

Future flow:

```
User
 │
 ▼
LLM Draft
 │
 ▼
ReflectionService
 │
 ├── Good → Return Answer
 └── Improve → Generate Better Answer
```

This is the first major step from a chatbot toward a true AI Agent.