from src.prompt.schema import IMPROVEMENT_PROMPT, PLANNING_PROMPT, REFLECTION_PROMPT, TOOL_PROMPT, SUMMARY_PROMPT
from src.config import SYSTEM_PROMPT

class PromptBuilder():

    def build(
        self,
        task_prompt: str,
        messages: list[dict]
    ):

        return [
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

    def build_tool_prompt(
        self,
        messages
    ):
        return self.build(
            TOOL_PROMPT,
            messages
        )


    def build_planning_prompt(
        self,
        messages
    ):
        return self.build(
            PLANNING_PROMPT,
            messages
        )


    def build_reflection_prompt(
        self,
        messages,
        answer
    ):

        prompt = self.build(
            REFLECTION_PROMPT,
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
            IMPROVEMENT_PROMPT,
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
            SUMMARY_PROMPT,
            messages
        )