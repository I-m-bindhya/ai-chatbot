from src.util.exception import AgentError
from src.util.json_parser import AIResponse


class AIAgent:

    def __init__(
        self,
        provider,
        registry,
        prompt_builder,
        tool_adapter,
        memory_service,
        context_builder,
        indexing_service,
        memory_important_service,
        planning_service,
        plan_executor
    ):
        self.provider = provider
        self.registry = registry
        self.prompt_builder = prompt_builder
        self.tool_adapter = tool_adapter
        self.memory_service = memory_service
        self.context_builder = context_builder
        self.indexing_service = indexing_service
        self.memory_important_service = memory_important_service
        self.planning_service = planning_service
        self.plan_executor = plan_executor


    def execute_tool_call(
        self,
        tool_call,
        conversation_id
    ):

        arguments = dict(tool_call.arguments)

        result = self.registry.execute(
            tool_call.tool,
            arguments
        )

        return {
            "role": "tool",
            "content": str(result)
        }


    def run(
        self,
        conversation_id,
        user_message
    ):
        try:
            messages = self.context_builder.build_context(
                conversation_id,
                user_message
            )

            user_message_record  = {
                "role": "user",
                "content": user_message
            }      

            message_id = self.memory_service.save_message(
                conversation_id,
                **user_message_record 
            )

            if self.memory_important_service.should_store(user_message):
                self.indexing_service.index(
                    message_id,
                    user_message,
                    {
                        "conversation_id": conversation_id,
                        "message_id": message_id,
                        "role": "user",
                        "content": user_message
                    }
                )

            tools = self.tool_adapter.adapt(
                self.registry.get_tools()
            )

            plan = self.planning_service.create_plan(messages)
            print(plan)

            messages = self.plan_executor.execute(
                plan,
                messages,
                conversation_id
            )

            iterations = 0


            while iterations < 5:

                tool_prompt = self.prompt_builder.build_tool_prompt(
                    messages
                )


                response = self.provider.chat(
                    tool_prompt,
                    tools if iterations == 0 else None
                )


                if not response.tool_call:
                    break


                tool_message = self.execute_tool_call(
                    response.tool_call,
                    conversation_id
                )


                messages.append(tool_message)

                iterations += 1



            response_prompt = self.prompt_builder.build_response_prompt(
                messages
            )

            draft_response = self.provider.chat(
                response_prompt
            )
            print("draft_response", draft_response)

            try:
                reflection = self.reflection_service.review(
                    messages,
                    draft_response.answer
                )

                print("reflection", reflection)

                final_answer = reflection.answer

            except Exception:
                final_answer = draft_response.answer

            
            assistant_message = {
                "role": "assistant",
                "content": final_answer
            }


            self.memory_service.save_message(
                conversation_id,
                **assistant_message
            )


            return final_answer

        except AgentError as ex:

            return AIResponse(
                answer=f"Agent error: {ex}"
            )

        except Exception as ex:

            print(ex)

            return AIResponse(
                answer="Unexpected error occurred."
            )