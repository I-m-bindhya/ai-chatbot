class AgentOrchestrator:

    def __init__(
        self,
        router_agent
    ):
        self.router_agent = router_agent


    async def run(
        self,
        conversation_id,
        user_message
    ):

        return await self.router_agent.route(
            conversation_id,
            user_message
        )

    async def stream(
        self,
        conversation_id,
        user_message
    ):

        return await self.router_agent.stream(
            conversation_id,
            user_message
        )