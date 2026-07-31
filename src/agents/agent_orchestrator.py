class AgentOrchestrator:

    def __init__(
        self,
        router_agent
    ):
        self.router_agent = router_agent


    def run(
        self,
        conversation_id,
        user_message
    ):

        return self.router_agent.route(
            conversation_id,
            user_message
        )