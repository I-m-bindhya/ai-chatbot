from src.util.interface import PlanAction


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

        for step in plan.steps:

            print(f"Executing: {step.action}")

            match step.action:

                case PlanAction.RETRIEVE_MEMORY:

                    documents = self.retrieval_service.retrieve(
                        messages[-1]["content"]
                    )

                    for doc in documents:

                        messages.append({
                            "role": "system",
                            "content": doc["content"]
                        })


                case PlanAction.CALL_TOOL:

                    result = self.registry.execute(
                        step.target,
                        {
                            "conversation_id": conversation_id
                        }
                    )

                    messages.append({
                        "role": "tool",
                        "content": str(result)
                    })


                case "generate_answer":

                    # Nothing to do here.
                    # AIAgent will generate the final answer.
                    pass


                case "summarize_memory":

                    # Implement later
                    pass


                case "reflect":

                    # ReflectionService will handle this later
                    pass


                case _:

                    print(
                        f"Unknown action: {step.action}"
                    )

        return messages