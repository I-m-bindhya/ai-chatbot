from src.config import SYSTEM_PROMPT
from src.prompt.prompt_registry import get_prompts

class PromptBuilder():


    def __init__(self):
        self.prompt = get_prompts();

    def build(
        self,
        task_prompt: str,
        messages: list[dict],
        answer: str | None = None
    ):

        prompt = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "system",
                "content": task_prompt
            },
            *messages
        ]

        if answer is not None:
            prompt.append({
                "role": "assistant",
                "content": answer
            })

        return prompt

    def build_prompt(
        self,
        system_prompt,
        messages
    ):
        return [
            {
                "role": "system",
                "content": system_prompt
            },
            *messages
        ]


    def build_planning_prompt(
        self,
        messages
    ):
        return self.build(
            self.prompt.PLANNING_PROMPT,
            messages
        )


    def build_reflection_prompt(
        self,
        messages,
        answer
    ):

        prompt = self.build(
            self.prompt.REFLECTION_PROMPT,
            messages
        )

        prompt.append({
            "role": "assistant",
            "content": answer
        })

        return prompt


    def build_improvement_prompt(
        self,
        messages,
        answer,
        feedback
    ):

        prompt = self.build(
            self.prompt.IMPROVEMENT_PROMPT,
            messages
        )

        prompt.extend([
            {
                "role": "assistant",
                "content": answer
            },
            {
                "role": "system",
                "content": f"Feedback: {feedback}"
            }
        ])

        return prompt


    def build_summary_prompt(
        self,
        messages
    ):
        return self.build(
            self.prompt.SUMMARY_PROMPT,
            messages
        )