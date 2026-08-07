import json

from src.util.exception import ProviderError
from src.util.interface import ReflectionResult


class ReflectionService:

    def __init__(
        self,
        provider,
        prompt_builder
    ):
        self.provider = provider
        self.prompt_builder = prompt_builder


    async def review(
        self,
        profile,
        messages,
        answer
    ):
        print('reflection prompt', profile.reflection_prompt)

        prompt = self.prompt_builder.build(
            profile.reflection_prompt,
            messages=messages,
            answer=answer
        )

        print('review prompt', prompt)

        try:
            plan_json = await self.provider.chat_raw(prompt)
        except ProviderError:
            return ReflectionResult(approved=True, feedback="")

        print('review response', repr(plan_json))

        if not plan_json:
            return ReflectionResult(approved=True, feedback="")

        try:
            payload = json.loads(plan_json.strip())
            if isinstance(payload, dict):
                return ReflectionResult(
                    approved=payload.get("approved", True),
                    feedback=payload.get("feedback", "")
                )
        except (TypeError, ValueError, json.JSONDecodeError):
            pass

        return ReflectionResult(approved=True, feedback="")


    async def improve(
        self,
        messages,
        answer,
        feedback
    ):

        prompt = self.prompt_builder.build_improvement_prompt(
            messages=messages,
            answer=answer,
            feedback=feedback
        )

        return await self.provider.chat(prompt)