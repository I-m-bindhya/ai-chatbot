from enum import Enum


class AgentState(str, Enum):

    LOAD_CONTEXT = "load_context"

    PLAN = "plan"

    EXECUTE_PLAN = "execute_plan"

    TOOL_LOOP = "tool_loop"

    GENERATE_RESPONSE = "generate_response"

    REFLECT = "reflect"

    SAVE_RESPONSE = "save_response"

    END = "end"