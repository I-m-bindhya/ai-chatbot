from src.agents.base_agent import BaseAgent


class RouterAgent:

    def __init__(
        self,
        agents: list[BaseAgent]
    ):
        self.agents = agents


    async def route(
        self,
        conversation_id,
        user_message
    ):

        for agent in self.agents:

            if agent.can_handle(user_message):

                print(
                    f"Routing to {agent.__class__.__name__}"
                )

                return await agent.execute(
                    conversation_id,
                    user_message
                )

        raise ValueError(
            "No suitable agent found."
        )

    async def stream(
            self,
            conversation_id,
            user_message
        ):
    
            for agent in self.agents:
    
                if agent.can_handle(user_message):
    
                    print(
                        f"Routing to {agent.__class__.__name__}"
                    )
    
                    return await agent.stream(
                        conversation_id,
                        user_message
                    )
    
            raise ValueError(
                "No suitable agent found."
            )