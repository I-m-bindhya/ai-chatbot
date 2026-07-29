
from pydantic import BaseModel

from enum import Enum

class PlanAction(str, Enum):
    RETRIEVE_MEMORY = "retrieve_memory"
    CALL_TOOL = "call_tool"
    GENERATE_ANSWER = "generate_answer"
    REFLECT = "reflect"
    SUMMARIZE_MEMORY = "summarize_memory"


class PlanStep(BaseModel):
    id: int
    action: PlanAction
    target: str | None = None
    reason: str


class ExecutionPlan(BaseModel):
    steps: list[PlanStep]