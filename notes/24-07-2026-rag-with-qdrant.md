# AI Engineer Bootcamp Notes
## Day: RAG Memory Implementation with Qdrant

---

# 1. Goal of Today's Session

Upgrade the chatbot memory system from:

Traditional conversation memory:

```
User Message
      |
      v
SQLite
      |
      v
Recent chat history
```

to:

RAG-based semantic memory:

```
                 User Message

                      |
        -----------------------------
        |                           |
        v                           v

     SQLite                    Embedding Model
  Conversation Data                  |
                                     v
                                  Vector
                                     |
                                     v
                                  Qdrant

```

The goal:

Allow the chatbot to remember information even after hundreds of messages.

Example:

Conversation 1:

```
My name is Bindhya
```

Conversation 200:

```
What is my name?
```

The chatbot should retrieve the old information using semantic search.

---

# 2. Embeddings Concept

## What is an embedding?

An embedding is a numerical representation of text meaning.

Example:

Text:

```
My laptop was purchased in 2024
```

Embedding model converts it into:

```
[
0.023,
-0.112,
0.845,
...
]
```

The vector captures semantic meaning.

Similar meanings produce similar vectors.

Example:

```
"I bought a computer last year"

and

"My laptop was purchased in 2024"
```

will have similar vector representations.

---

# 3. Embedding Service

Created abstraction:

```python
class EmbeddingService:

    def embed(self, text):
        pass
```

The application does not depend on a specific embedding provider.

Current implementation:

```
EmbeddingService
        |
        |
        v
Ollama Embedding Model
(nomic-embed-text)
```

Future replacement:

```
EmbeddingService
        |
        |
        v
OpenAI Embedding API
```

No application changes required.

---

# 4. Ollama Embedding Setup

Installed:

```
ollama
```

Downloaded embedding model:

```
ollama pull nomic-embed-text
```

Embedding flow:

```
Text

 |

EmbeddingService

 |

Ollama

 |

Vector

 |

Qdrant
```

---

# 5. Vector Database Integration

Implemented:

```
VectorStore
```

as an abstraction.

Example:

```python
from abc import ABC, abstractmethod


class VectorStore(ABC):

    @abstractmethod
    def upsert(self):
        pass


    @abstractmethod
    def search(self):
        pass
```

Purpose:

The application should depend on an interface, not Qdrant directly.

Architecture:

```
RetrievalService

       |
       |
       v

VectorStore Interface

       |
       |
       v

QdrantStore Implementation
```

---

# 6. Abstract Class Mistake

Error:

```
Can't instantiate abstract class VectorStore
```

Cause:

Wrong:

```python
vector_store = VectorStore()
```

VectorStore is only a contract.

Correct:

```python
vector_store = QdrantStore()
```

Lesson:

Interfaces define behavior.
Implementations perform the work.

---

# 7. Indexing Service

Created:

```
IndexingService
```

Responsibility:

Convert text into embeddings and store them.

Flow:

```
Message

 |

IndexingService

 |

EmbeddingService

 |

Vector

 |

Qdrant
```

Code idea:

```python
class IndexingService:

    def __init__(
        self,
        embedding_service,
        vector_store
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store


    def index(
        self,
        point_id,
        text,
        payload
    ):

        vector = self.embedding_service.embed(text)

        self.vector_store.upsert(
            point_id,
            vector,
            payload
        )
```

---

# 8. Message ID Design

Important decision:

Use SQLite message ID as Qdrant point ID.

Architecture:

```
                 Message

                    |
        --------------------------
        |                        |
        v                        v

     SQLite                 Qdrant

   message_id=101       point_id=101

```

Benefits:

- Easy tracing
- Easy deletion
- Data consistency

SQLite remains the source of truth.

---

# 9. ChatService Responsibility

Indexing belongs in ChatService.

Reason:

ChatService manages message lifecycle.

Flow:

```
User Message

      |
      v

ChatService

      |
      +---- Save to SQLite
      |
      +---- Create Embedding
      |
      +---- Store in Qdrant
      |
      +---- Send to Agent
```

---

# 10. ContextBuilder Responsibility

ContextBuilder should NOT save data.

Its responsibility:

Build final LLM context.

Flow:

```
ContextBuilder

      |
      +---- Recent messages
      |
      +---- Retrieved memories
      |
      v

LLM Context
```

---

# 11. RAG Retrieval Flow

Final architecture:

```
User Question

       |
       v

ContextBuilder

       |
       |
       +------ SQLite
       |
       |
       +------ Qdrant Search
                    |
                    |
                    v
              Relevant Memory


       |
       v

AIAgent

       |
       v

LLM
```

---

# 12. Payload Schema Problem

Initially Qdrant had inconsistent payloads.

Old:

```json
{
 "text": "My name is Bindhya"
}
```

New:

```json
{
 "content": "My name is Bindhya",
 "role": "user",
 "message_id": 101
}
```

Problem:

Different consumers expect different fields.

Production rule:

A vector collection should have a consistent schema.

---

# 13. Context Format Conversion

Qdrant format:

```json
{
 "content":"My name is Bindhya"
}
```

cannot directly go to LLM.

LLM expects:

```json
{
 "role":"system",
 "content":"Relevant memory: My name is Bindhya"
}
```

Therefore:

ContextBuilder acts as an adapter.

Architecture:

```
Qdrant Payload

      |

      v

ContextBuilder

      |

      v

LLM Message Format
```

---

# 14. Important Debugging Lesson

Error:

```
ValidationError:
role field required
```

Cause:

Sent this:

```python
{
"text":"My name is Bindhya"
}
```

to Ollama.

Ollama requires:

```python
{
"role":"user",
"content":"text"
}
```

Always convert storage data into LLM message format.

---

# 15. Current Project Architecture

```
                 User

                  |
                  v

             ChatService

                  |
        ---------------------
        |                   |

 MemoryService       IndexingService

        |                   |

     SQLite          EmbeddingService

                            |

                         Ollama

                            |

                         Vector

                            |

                         Qdrant


                  |
                  v

             ContextBuilder

                  |
                  v

               AIAgent

                  |
                  v

                 LLM
```

---

# Completed Today

✅ Ollama embedding integration

✅ Real vector generation

✅ Qdrant connection

✅ VectorStore abstraction

✅ IndexingService

✅ Semantic retrieval

✅ ContextBuilder integration

✅ LLM message formatting

---

# Next Session Topics

## 1. Improve Retrieval Quality

Current:

```
Search all vectors
```

Need:

```
Search only:

conversation_id = X
user_id = Y
```

Concept:

Qdrant filtering.

---

## 2. Memory Strategy

Not every message should become permanent memory.

Learn:

- short-term memory
- long-term memory
- memory summarization
- memory importance scoring

---

## 3. Production RAG Pipeline

Final flow:

```
Question

 |

Retrieve

 |

Rank

 |

Build Context

 |

Generate Answer

```

---

## Key Interview Points

### Why use vector database?

"Traditional databases perform exact matching. Vector databases enable semantic similarity search by comparing embeddings."

---

### Why abstraction for vector storage?

"To avoid coupling the application to a specific vector database implementation."

---

### Why ContextBuilder?

"It separates storage representation from LLM message format and controls the context sent to the model."

---

End of Session Notes