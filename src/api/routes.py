from fastapi import APIRouter
from src.agents.profiles import CODING_PROFILE, MEMORY_PROFILE
from src.agents.agent_orchestrator import AgentOrchestrator
from src.agents.coding_agent import CodingAgent
from src.agents.memory_agent import MemoryAgent
from src.agents.router_agent import RouterAgent
from src.services.reflection_service import ReflectionService
from src.actions.action_registry import ActionRegistry
from src.actions.list_conversations_action import ListConversationsAction
from src.plan_executor.plan_executor import PlanExecutor
from src.services.planning_service import PlanningService
from src.memory.memory_important_service import MemoryImportanceService
from src.retrieval.indexing_service import IndexingService
from src.retrieval.vector_store import VectorStore
from src.retrieval.retrieval_service import RetrievalService
from src.retrieval.embedding_service import EmbeddingService
from src.retrieval.qdrant_store import QdrantStore
from src.context.context_builder import ContextBuilder
from src.memory.memory_manager import MemoryManager
from src.agents.ai_agent import AIAgent
from src.providers.ollama_provider import OllamaProvider
from src.services.chat_service import ChatService
from src.memory.memory_service import MemoryService
from pydantic import BaseModel
from src.tools.chat_tools import ChatTools
from src.tools.tool_registry import ToolRegistry

from src.prompt.prompt_builder import PromptBuilder
from src.adapter.tool_adapter import ToolAdapter

builder = PromptBuilder()
adapter = ToolAdapter()

class ChatRequest(BaseModel):
    message: str
    multi_agent: bool

class ConversationRequest(BaseModel):
    title: str

router = APIRouter()
provider = OllamaProvider()
memory_service = MemoryService()
memory_manager = MemoryManager(memory_service)
store = QdrantStore()
embedding = EmbeddingService()
retrieval_service = RetrievalService(embedding, store)
context_builder = ContextBuilder(memory_manager, retrieval_service)
registry = ToolRegistry()
indexing_service = IndexingService(embedding, store)
memory_important_service = MemoryImportanceService()
planning_service = PlanningService(provider, builder)
registry_action= ActionRegistry()
reflection_service = ReflectionService(provider, builder)
plan_executor = PlanExecutor(retrieval_service, registry_action)
agent = AIAgent(provider, registry, builder, adapter, memory_service, context_builder,indexing_service, memory_important_service, planning_service, plan_executor, reflection_service)
memory_agent = MemoryAgent(    profile=MEMORY_PROFILE,
    ai_agent=agent)
coding_agent = CodingAgent(    profile=MEMORY_PROFILE,
    ai_agent=agent)
router_agent = RouterAgent([
    memory_agent,
    coding_agent
])
orchestrator = AgentOrchestrator(router_agent)
chatbot = ChatService(provider, memory_service, agent, orchestrator)
chat_tools = ChatTools(chatbot)

registry.register(chat_tools.get_tools())


registry_action.register(
    "list_conversations",
    ListConversationsAction(memory_service)
)

@router.get("/")
def home():
    return { 'message': 'API Running Sucessfully'}

@router.post("/conversations")
def create_conversation():
    return chatbot.create_new_chat()

@router.get("/conversations")
def list_conversation():
    return chatbot.list_chats()

@router.get("/conversations/{conversation_id}/messages")
def load_messages(conversation_id: int):
    return chatbot.load_messages(conversation_id)

@router.post("/conversations/{conversation_id}/messages")
def create_messages(conversation_id: int, request: ChatRequest):
    return chatbot.chat(conversation_id, request.message, request.multi_agent)

@router.put("/conversations/{conversation_id}")
def rename_conversation(conversation_id, request: ConversationRequest):
    return chatbot.rename_chat(conversation_id, request.title)

@router.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id):
    return chatbot.delete_conversation(conversation_id)
