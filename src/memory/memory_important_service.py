class MemoryImportanceService:

    IGNORE_MESSAGES = {
        "hi",
        "hello",
        "thanks",
        "thank you",
        "welcome",
        "how are you?",
        "greetings",
        "good morning",
        "good evening",
        "good night",
        "bye",
        "see you"
    }

    def should_store(
        self,
        message
    ):
        normalized = message.strip().lower()

        return normalized not in self.IGNORE_MESSAGES