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

    async def create_plan(
        self,
        profile,
        messages
    ):
        prompt = self.prompt_builder.build(profile.planning_prompt, messages)

        plan_json = await self.provider.chat_raw(prompt)

        print(plan_json)

        try:
            payload = json.loads(plan_json)
        except (TypeError, ValueError, json.JSONDecodeError):
            return ExecutionPlan(
                steps=[],
                tools=[]
            )

        if not isinstance(payload, dict):
            return ExecutionPlan(
                steps=[],
                tools=[]
            )

        payload.setdefault("tools", [])
        payload.setdefault("steps", [])

        return ExecutionPlan(**payload)