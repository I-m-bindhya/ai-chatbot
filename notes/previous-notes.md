An LLM predicts the next token; it does not retrieve facts from a database.
A model is a trained AI program accessed through an API.
Tokens determine cost, speed, and context size.
A context window is temporary working memory for a single request.
LLM APIs are stateless.
Applications—not models—manage conversation memory.
Temperature controls response randomness.
Lower temperatures are generally better for structured outputs and code generation.
A prompt is an API contract between your application and the model. Prompt = API Specification 
The best prompt is not the longest prompt. It is the prompt with the fewest ambiguities.
The system prompt defines the model's overall behavior. The system prompt controls the style, constraints, and behavior. 
The User prompt is simply the user's request. The user prompt defines the task. 
 Assistant messages maintain conversational continuity by being included in future requests.
Memory in an AI application is created by sending previous messages—not by the model remembering them on its own.
Prompt Engineering is the process of making LLM behavior predictable. 
Prompt Engineering is API Design for AI. 
Four Principles of Production Prompt Engineering - Be Explicit, Give Constraints, Define Success, Define Failure.
An LLM API call is just another HTTP request wrapped in an SDK. An LLM is just another service your backend communicates with. 
Never hardcode secrets—use environment variables.
Always isolate project dependencies with a virtual environment.
Ollama is not a provider in the same sense as OpenAI. It's primarily a local runtime/server that serves models over an API. However, in our code architecture, we'll treat it as a "provider" behind an abstraction. That's a useful engineering simplification. 
LLM runtimes are installed once per machine. Python libraries are installed per project. 
A provider hosts or exposes AI models (OpenAI, Ollama, Anthropic).
A model performs inference by predicting the next token (GPT-4.1, Qwen2.5, Llama 3).
Ollama is a local LLM runtime, not the model itself.
The Ollama Python package is only a client SDK that communicates with the Ollama runtime.
Cloud LLMs execute on provider infrastructure; local LLMs execute on your own machine.
Installing Ollama globally is similar to installing Docker or PostgreSQL—install it once and use it across projects.
Python libraries such as openai, ollama, and fastapi belong inside the project's virtual environment.
LLM providers may differ, but the application architecture remains nearly identical.
An LLM is stateless; it has no memory between API requests.
Conversation memory is managed by the application, not by the model.
Every LLM request should include all the context required to answer correctly.
Applications create memory by rebuilding the messages list before every request.
Sending the entire conversation repeatedly increases token usage, latency, and cost.
Production applications use sliding windows, summarization, or retrieval to manage conversation history.
The backend retrieves relevant context; the model generates the response.
Local models are ideal for learning, privacy-sensitive workloads, and offline development.
Cloud models generally provide higher quality, scalability, and managed infrastructure.
AI Engineering is primarily about designing the application around the model, not just calling the model.
Golden Rule: Memory belongs to the application; intelligence emerges from combining the application with the LLM.
The messages list is the real "memory" of an AI application. 
System Prompt -> Global Settings ,  User Prompt -> Current Request, Assistant Messages -> Previous Responses 
The intelligence of a production AI application comes as much from how the backend constructs the messages list as from the model itself. 
LLM memory is simulated by sending previous messages in every request.
The messages list is the application's conversation history.
System, User, and Assistant messages together form the prompt sent to the model.
Conversation state should be isolated per user or conversation ID.
Production AI systems trim or summarize old messages to stay within the model's context window.
How does ChatGPT remember previous messages? The model itself is stateless. The backend stores the conversation history and reconstructs the messages list for each request. The model appears to remember because it receives the previous context again with every call.
How do you clear conversation memory? Conversation memory is maintained by the application, not the model. The application stores previous messages in a list. Clearing memory simply means resetting that list while keeping the system prompt so the assistant retains its intended behavior. 
A "/clear" command resets the application's conversation history, effectively starting a new chat. 
 Chat history stored only in RAM is temporary and is lost when the application exits. 
Provider abstraction allows switching between OpenAI, Ollama, or other LLM providers with minimal code changes. 
Separating config, services, and providers makes AI applications easier to maintain and extend. 
AI chatbots are orchestrated by application code; the model only generates responses based on the messages it receives. 
 Production AI systems use persistent storage (e.g., SQLite or PostgreSQL) to implement long-term memory. 
RAM is volatile memory; data is lost when the application exits.
Persistent storage allows AI applications to retain conversation history across restarts.
SQLite is a lightweight, serverless relational database ideal for local development.
Separation of Concerns keeps business logic (ChatService) independent of storage logic (MemoryService).
Designing service interfaces before implementation promotes maintainable and extensible architecture.
 An LLM remains stateless even when the application becomes stateful through persistent memory.
 A session represents one conversation, while persistent storage can retain multiple sessions over time.
Clean architecture allows storage backends (SQLite, PostgreSQL, etc.) to be replaced with minimal code changes.
A cursor is like a remote control for the database. Python -> Cursor -> Database 
connection.commit() - permanently saves the changes
Constructors (__init__) should initialize the object, not perform significant business operations. 
AI-Chatbot project - Why did we create MemoryService instead of writing SQL directly inside ChatService? ChatService decides when to save or load messages. MemoryService decides how they are stored. This follows the Single Responsibility Principle and makes it easy to switch from SQLite to PostgreSQL, Redis, or another database without changing the chat logic. 
Where is conversation memory stored now? In a SQLite database (chat.db). When the application starts, ChatService loads all previous messages from MemoryService into memory and sends them as context to the LLM. 
Does Ollama remember conversations? No. Ollama (like OpenAI APIs) is stateless. The application is responsible for storing and resending the conversation history. 
"Why return immediately after handling /clear?" "/clear is an application command, not a prompt for the LLM. Returning immediately prevents unnecessary API/model calls, avoids token usage, reduces latency, and keeps command handling separate from AI conversation logic." 
Why should ChatService not know about SQLite? ChatService contains business logic and should not depend on a specific database. MemoryService abstracts storage, allowing us to switch from SQLite to PostgreSQL, Redis, MongoDB, etc., without changing ChatService. 
Why do we load messages into RAM if they already exist in the database? The model cannot read directly from a database. 
Why load messages during ChatService.init()? When the application starts, previous conversation history is loaded from persistent storage into RAM so future requests can continue the conversation. The database is the source of truth, while RAM provides fast access during runtime. 
Why not create one table per conversation? One table. Millions of rows. Database indexes make retrieval fast. This is called database normalization.
Conversation ID uniquely identifies one chat session. It groups all messages belonging to the same conversation, making retrieval efficient, eliminating ambiguity, and enabling multiple independent chat sessions for the same or different users. 
A foreign key guarantees: Every conversation_id inside the messages table must exist in the conversations table.
A foreign key doesn't generate IDs. It only validates: "Does this conversation already exist?" If yes, Allow insert. If not, reject insert.
Why do we use foreign keys? A foreign key maintains referential integrity by ensuring that every message references a valid conversation. It prevents orphan records, keeps the database consistent, and enables reliable joins between related tables. 
A chatbot should support multiple conversations instead of storing all messages in one history.
Each conversation should have a unique conversation_id to isolate messages.
Store conversations and messages in separate tables using a one-to-many relationship.
ChatService is stateless; it should not permanently store conversation messages in RAM.
The database becomes the single source of truth for conversation history.
Every chat() request should reload the conversation messages from the database.
The system prompt is prepended before every model request instead of being permanently stored in memory.
ChatService decides when to perform operations; MemoryService decides how they are stored.
Save the user's message before calling the LLM to avoid losing input if generation fails.
Save the assistant's reply immediately after the model responds.
conversation_id should be passed into chat(conversation_id, user_input) on every request.
New conversations should start with a default title such as "New Chat".
Conversation titles can be updated automatically after the first meaningful user message.
Title generation is a secondary task and should not delay the user's first AI response.
main.py should manage the application flow, while ChatService focuses only on chat business logic.
The overall architecture follows:
main.py → User interaction
ChatService → Chat orchestration
MemoryService → Database operations
Provider → LLM communication
Separating responsibilities makes the application easier to maintain, test, and extend.
Why did we make ChatService stateless? HTTP APIs are stateless, so our ChatService should also be stateless. Each request contains all the information needed to process it. This avoids shared in-memory state, makes horizontal scaling easier, and allows multiple users to use the service safely at the same time. 
Why FastAPI? FastAPI exposes our backend through HTTP so other applications such as web frontends, mobile apps, or external services can communicate with our chatbot. 
Prompts are application components, not just strings. The prompt is part of your software architecture. 
Code + Prompt  = Behavior . The prompt has become another layer of programming. 
 Avoid one giant system prompt
Design prompts using Single Responsibility Principle.
Example: TEACHER_PROMPT, CODE_REVIEW_PROMPT, SECURITY_PROMPT, TITLE_GENERATION_PROMPT
Select prompts dynamically based on application mode.
Example: if mode == "teacher": prompt = TEACHER_PROMPT else: prompt = CODE_REVIEW_PROMPT
Prompts should be modular, reusable and easy to maintain.
AI Engineer Mindset:
Traditional Software
Code
↓
Behavior
AI Software
Code
+
Prompt
↓
Behavior
Prompt Engineering means: Designing instructions that consistently produce reliable, predictable, and useful outputs from an LLM.
Static prompts don't scale. Templates do. 
Prompt Composition - Compose multiple small, reusable prompts into one final prompt based on the application's requirements. 
AI Engineers don't send prompts to models—they assemble context for models. 
RAG - Retrieve only the most relevant information instead of sending everything. 
JSON Schema, Pydantic Models, Structured Outputs - The best context is not the biggest context. It's the most relevant context. 
101. Prompt Engineering is the process of designing prompts to produce reliable, predictable, and useful outputs from an LLM.
102. The objective of Prompt Engineering is to reduce ambiguity, improve consistency, and make AI suitable for production systems.
103. Zero-shot Prompting means providing only instructions without examples.
104. Few-shot Prompting means teaching the model the expected response format using examples before asking the actual question.
105. Low Temperature reduces randomness and produces more deterministic responses.
106. Few-shot Prompting teaches response patterns, while Temperature controls randomness.
107. Best practice: Combine Low Temperature + Few-shot Prompting when consistent formatting is required.
108. Static prompts don't scale. Prompt Templates make prompts reusable, maintainable, and dynamic.
109. Prompt Composition means assembling multiple small, reusable prompts into one final prompt based on application requirements.
110. Prompt Priority (Highest → Lowest)
System Prompt
Developer Instructions
User Prompt
Retrieved Documents (RAG)
111. AI Engineers don't simply send prompts—they assemble the right context before sending it to the model.
112. Prompt Injection is an attempt by the user to override system or developer instructions (e.g., "Ignore previous instructions.").
113. Defend against Prompt Injection by keeping system instructions separate, validating outputs, and never blindly trusting user input.
114. Structured Outputs instruct the model to return responses in a predefined JSON format instead of free-form text.
115. JSON Schema acts as a contract between the AI model and the backend application.
116. Example JSON Schema:
{
    "answer": "...",
    "topics": [],
    "confidence": "...",
    "reasoning": "..."
}
117. Pydantic validates AI responses against the expected schema before business logic consumes them.
118. BaseModel defines the expected structure of AI responses.
119. model_validate_json() parses a JSON string and validates it against a Pydantic model.
120. model_validate() validates an already parsed Python dictionary.
121. JSON Parser is responsible for parsing the AI response and validating it before returning a typed object.
122. AI Request Flow:
Client
↓
FastAPI Route
↓
ChatService
↓
Provider
↓
LLM
↓
JsonParser
↓
Pydantic Validation
↓
Typed Object
↓
API Response
123. Production AI Architecture:
FastAPI
↓
Routes
↓
ChatService
↓
Provider
↓
LLM
↓
JsonParser
↓
Pydantic
↓
Business Logic
↓
API Response
124. AI outputs should be validated before reaching business logic because LLMs are probabilistic and may generate malformed responses.
125. Separating the JsonParser from ChatService follows the Single Responsibility Principle and keeps the service layer clean.
126. Prompt engineering is about making AI reliable, not just intelligent.
127. Structured outputs make backend integration easier because every response follows the same contract.
128. Pydantic provides strong typing, validation, automatic parsing, and cleaner production code.
Why do we need Function Calling if the backend can directly call Python functions? The backend can directly call Python functions when the required action is already known. However, in conversational AI, the application often doesn't know the user's intent in advance. Function Calling allows the LLM to interpret the user's natural language, decide which backend function is appropriate, and provide the required arguments. The backend then validates and executes the function while keeping all business logic, security, and data access under application control. 
Why do we send tool definitions instead of Python functions? "The LLM cannot inspect or execute Python code. It only needs a structured description of the available capabilities, including the function name, purpose, and parameters. Based on that metadata, the LLM decides which tool to use. The backend application then executes the actual Python implementation." 
"What is Function Calling?"  "Function Calling is not the model executing Python code. The model receives only tool metadata (name, description, and parameters), decides which tool should be used based on the user's request, and returns a structured tool call. The application validates and executes that tool, then sends the result back to the model if needed." 
Function Calling allows an LLM to decide WHICH function should be executed. The application executes the function; the LLM never runs Python code directly.
LLMs receive only tool metadata (name, description, parameters). They never receive executable Python functions.
Tool metadata should have clear names, detailed descriptions, and well-defined parameter schemas so the LLM can choose the correct tool.
Tool Registry acts as a central catalog for all available tools. It stores tool metadata and executes the selected tool.
ToolAdapter converts internal Python tool definitions into an LLM-compatible format by removing Python function references.
Separation of Concerns:
     - ChatTools → Business operations
     - ToolRegistry → Register and execute tools
     - ToolAdapter → Convert tools for the LLM
     - Provider → Communicate with the AI model
     - ChatService → Orchestrate the complete workflow


AI Function Calling Flow:
     User Request
          ↓
     ChatService
          ↓
     PromptBuilder
          ↓
     ToolAdapter
          ↓
     AI Provider
          ↓
     LLM decides tool
          ↓
     ToolRegistry.execute()
          ↓
     ChatTools
          ↓
     ChatService
          ↓
     MemoryService / Database


The LLM returns a structured tool call (tool name + arguments). The application validates and executes it safely.
The Tool Registry should not create ChatService or ChatTools. Dependencies should be injected from the application bootstrap.
Dependency Injection keeps components reusable, testable, and loosely coupled by passing required objects through constructors instead of creating them internally.
A Tool Registry stores executable function references, while a Tool Adapter exposes only metadata to the LLM.
Good AI architecture isolates responsibilities so that replacing one AI provider (OpenAI, Ollama, Anthropic, Gemini) requires minimal changes to the rest of the system.
Function Calling is not about executing code inside the model. It is about the model making decisions while the application performs the execution.
Production AI systems separate tool selection, tool execution, prompt construction, response validation, and business logic into independent layers.
User -> LLM -> Needs a tool?  - Yes - Application executes tool - Tool Result - LLM reasons on the result - Final Answer. This "reason → act → observe → reason again" cycle is the foundation of many AI agent systems. 
Why do we send the tool result back to the LLM instead of directly to the user? Because tool outputs are raw structured data. The LLM combines that data with the user's original request and conversation context to produce a relevant, natural-language response. This separation lets tools focus on data retrieval and actions, while the LLM focuses on reasoning and communication. 
What is an AI Agent? An AI Agent is a software component that uses an LLM to reason, make decisions, and execute actions through external tools until it completes a user's goal. Unlike a simple chatbot that only generates text, an AI Agent can plan multiple steps, call APIs or functions, observe the results, and continue reasoning before producing the final answer. 
An AI Agent is an LLM-powered system that can reason, execute tools, observe outcomes, and iteratively work toward completing a user's goal. 
AI Chatbot	                              -       AI Agent
Generates text responses      -	Executes actions to achieve goals
Usually one LLM call	        -  Can perform multiple reasoning iterations
Cannot interact with external  -  Uses tools, APIs, databases, and functions
systems on its own	
Responds based on its          -   Plans, acts, observes, and reasons before
   knowledge and context	           responding
Mostly conversational	        -    Goal-oriented and task-oriented
The Agent should not know whether it is using Ollama, OpenAI, Claude, or Gemini. It should depend only on a common provider interface such as provider.chat(). This keeps the Agent provider-agnostic, making it easy to swap or add LLM providers without changing the Agent's business logic
Short Term Memory - Working Memory, Conversation Memory
Long-Term Memory  - User preferences and facts. 
"Why did you introduce MemoryManager instead of directly loading messages from MemoryService inside ChatService?" MemoryService handles persistence, while MemoryManager handles memory strategy. MemoryManager decides what information should be sent to the LLM based on context limitations, relevance, and future memory policies. This keeps storage concerns separate from AI context management. 
Single Responsibility Principle:
ChatService → Application orchestration
AIAgent → AI reasoning lifecycle
MemoryManager → Context strategy
MemoryService → Persistence
Provider → LLM communication
ToolRegistry → Tool execution
Prompt Engineering - Focuses on writing a better prompt.
Context Engineering - Focuses on everything the model receives.
┌─────────────────────────────┐
│ System Instructions         │
├─────────────────────────────┤
│ User Profile                │
├─────────────────────────────┤
│ Conversation Summary        │
├─────────────────────────────┤
│ Recent Messages             │
├─────────────────────────────┤
│ Retrieved Documents (RAG)   │
├─────────────────────────────┤
│ Tool Results                │
├─────────────────────────────┤
│ Current User Question       │
└─────────────────────────────┘
               │
               ▼
              LLM
"What's the difference between Prompt Engineering and Context Engineering?" Prompt engineering focuses on crafting the instruction given to the model. Context engineering is the broader practice of selecting, organizing, and managing all information sent to the LLM—such as system prompts, conversation history, retrieved knowledge, tool outputs, and user state—to maximize response quality within the model's context window. 
Sliding Window Memory – why messages[-10:] eventually becomes insufficient.
Summary Memory – compressing long conversations into concise summaries.
Hybrid Memory – combining summaries with recent messages.
Token Budgeting – selecting context based on token limits instead of message count.
| Strategy       | Best For             | Limitation                            |
| -------------- | -------------------- | ------------------------------------- |
| Sliding Window | Short conversations  | Forgets older information             |
| Summary        | Long conversations   | May lose fine details                 |
| Hybrid         | Production chatbots  | Slightly more complex                 |
| Retrieval      | Knowledge assistants | Requires embeddings and vector search |


"Why isn't storing the last 10 messages enough for a production chatbot?" Because important information may have occurred much earlier in the conversation. A fixed sliding window eventually discards those details. Production systems typically use summaries, retrieval mechanisms, or hybrid memory strategies to preserve important context while staying within the model's context window. 
Why do production AI systems use token budgeting instead of limiting the number of messages? Because messages vary significantly in size. A single message may contain hundreds or thousands of tokens, while another contains only a few. Since LLMs enforce limits on tokens rather than message count, production systems budget context using token counts to stay within the model's context window while maximizing useful information. 
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
