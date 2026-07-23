class AIAgent:

    def __init__(
        self,
        provider,
        registry,
        prompt_builder,
        tool_adapter,
        memory_service,
        context_builder
    ):
        self.provider = provider
        self.registry = registry
        self.prompt_builder = prompt_builder
        self.tool_adapter = tool_adapter
        self.memory_service = memory_service
        self.context_builder = context_builder


    def execute_tool_call(
        self,
        tool_call,
        conversation_id
    ):

        arguments = dict(tool_call.arguments)

        arguments["conversation_id"] = conversation_id

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

        messages = self.context_builder.build_context(
            conversation_id,
            user_message
        )

        user_message_record  = {
            "role": "user",
            "content": user_message
        }      

        self.memory_service.save_message(
            conversation_id,
            **user_message_record 
        )

        tools = self.tool_adapter.adapt(
            self.registry.get_tools()
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


        final_response = self.provider.chat(
            response_prompt
        )

        print("final_response", final_response)
        
        assistant_message = {
            "role": "assistant",
            "content": final_response.answer
        }


        self.memory_service.save_message(
            conversation_id,
            **assistant_message
        )


        return final_response