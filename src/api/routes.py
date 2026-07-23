from fastapi import APIRouter
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

class ConversationRequest(BaseModel):
    title: str

router = APIRouter()
provider = OllamaProvider()
memory = MemoryService()
memory_manager = MemoryManager(memory)
registry = ToolRegistry()

agent = AIAgent(provider, registry, builder, adapter, memory_manager, memory)

chatbot = ChatService(provider, memory, agent)
chat_tools = ChatTools(chatbot)

registry.register(chat_tools.get_tools())


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
    return chatbot.chat(conversation_id, request.message)

@router.put("/conversations/{conversation_id}")
def rename_conversation(conversation_id, request: ConversationRequest):
    return chatbot.rename_chat(conversation_id, request.title)

@router.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id):
    return chatbot.delete_conversation(conversation_id)
