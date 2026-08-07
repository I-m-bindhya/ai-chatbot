import json

from src.util.interface import ExecutionPlan


class PlanningService:

    def __init__(
        self,
        provider,
        prompt_builder
    ):
        self.provider = provider
        self.prompt_builder = prompt_builder

    def create_plan(
        self,
        profile,
        messages
    ):
        prompt = self.prompt_builder.build(profile.planning_prompt, messages)

        plan_json = self.provider.chat_raw(prompt)

        print(plan_json)

        return ExecutionPlan(
            **json.loads(plan_json)
        )