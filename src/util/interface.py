
from pydantic import BaseModel
from typing import List

from enum import Enum

class PlanAction(str, Enum):
    RETRIEVE_MEMORY = "retrieve_memory"
    CALL_TOOL = "call_tool"
    GENERATE_ANSWER = "generate_answer"
    REFLECT = "reflect"
    SUMMARIZE_MEMORY = "summarize_memory"
    LIST_CONVERSATION = "list_conversations"


class PlanStep(BaseModel):
    id: int
    action: PlanAction
    target: str | None = None
    reason: str


class ExecutionPlan(BaseModel):
    steps: List[PlanStep]
    tools: List[str] = []

class ReflectionResult(BaseModel):
    approved: bool
    feedback: str