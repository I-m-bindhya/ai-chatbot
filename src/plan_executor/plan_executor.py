from src.util.interface import PlanAction, ExecutionPlan


class PlanExecutor:

    def __init__(
        self,
        retrieval_service,
        registry
    ):
        self.retrieval_service = retrieval_service
        self.registry = registry


    def execute(
        self,
        plan,
        messages,
        conversation_id
    ):
        print("plan", plan)

        if plan is None or not hasattr(plan, "steps"):
            return messages

        for step in plan.steps:
            action = self.registry.get(step.action)
            print('action', action)
            result = action.execute(conversation_id)
            messages.extend(result)

        return messages