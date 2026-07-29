class ReflectionService:

    def __init__(
        self,
        provider,
        prompt_builder
    ):
        self.provider = provider
        self.prompt_builder = prompt_builder

    def review(
        self,
        user_message,
        messages,
        answer
    ):

        prompt = self.prompt_builder.build_reflection_prompt(
            user_message,
            messages,
            answer
        )

        return self.provider.chat(prompt)