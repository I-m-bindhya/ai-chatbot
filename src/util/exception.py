class AgentError(Exception):
    """Base class for all agent errors."""
    print("error", Exception)
    pass


class ProviderError(AgentError):
    pass


class ToolExecutionError(AgentError):
    pass


class RetrievalError(AgentError):
    pass


class PlanningError(AgentError):
    pass


class ReflectionError(AgentError):
    pass