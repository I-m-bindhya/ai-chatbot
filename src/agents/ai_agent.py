from src.agents.agent_state import AgentState
from src.prompt.schema import CHAT_RESPONSE_SCHEMA
from src.util.exception import AgentError
from src.util.interface import ExecutionPlan
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
        plan_executor,
        reflection_service
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
        self.reflection_service = reflection_service


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


    async def run(
        self,
        conversation_id,
        user_message,
        profile
    ):
        print(profile)
        try:
            state = AgentState.LOAD_CONTEXT
            MAX_REFLECTION_RETRIES = 2
            while state != AgentState.END:

                messages = []
                plan = None
                response = None
                final_answer = None
                tool_prompt = None
                tools = None

                if state == AgentState.LOAD_CONTEXT:
                    messages = self.context_builder.build_context(
                        conversation_id,
                        user_message
                    )

                    user_message_record = {
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

                    state = AgentState.PLAN

                elif state == AgentState.PLAN:
                    plan = await self.planning_service.create_plan(
                        profile,
                        messages
                    )

                    if plan is None or not hasattr(plan, "tools"):
                        plan = ExecutionPlan(steps=[], tools=[])

                    allowed = set(profile.allowed_tools)
                    selected = [
                        tool
                        for tool in getattr(plan, "tools", [])
                        if tool in allowed
                    ]

                    print(profile.allowed_tools)
                    selected_tools = self.registry.get_selected_tools(selected)
                    tools = self.tool_adapter.adapt(selected_tools)
                    state = AgentState.EXECUTE_PLAN

                elif state == AgentState.EXECUTE_PLAN:
                    messages = self.plan_executor.execute(
                        plan,
                        messages,
                        conversation_id
                    )
                    state = AgentState.TOOL_LOOP

                elif state == AgentState.TOOL_LOOP:
                    iterations = 0

                    while iterations < 5:
                        tool_prompt = self.prompt_builder.build_prompt(
                            profile.system_prompt,
                            messages
                        )

                        response = await self.provider.chat(
                            tool_prompt,
                            tools if iterations == 0 else None
                        )

                        print('usage response', response)

                        if not response.tool_call:
                            break

                        tool_message = self.execute_tool_call(
                            response.tool_call,
                            conversation_id
                        )

                        messages.append(tool_message)
                        iterations += 1

                    state = AgentState.GENERATE_RESPONSE

                elif state == AgentState.GENERATE_RESPONSE:
                    response_prompt = self.prompt_builder.build(
                        CHAT_RESPONSE_SCHEMA,
                        messages
                    )

                    response = await self.provider.chat(
                        response_prompt
                    )
                    final_answer = response.answer
                    print("final_answer", final_answer)
                    state = AgentState.REFLECT

                elif state == AgentState.REFLECT:
                    for _ in range(MAX_REFLECTION_RETRIES + 1):
                        reflection = await self.reflection_service.review(
                            profile=profile,
                            messages=messages,
                            answer=final_answer
                        )

                        print("reflection", reflection)

                        if reflection.approved:
                            break

                        improved = await self.reflection_service.improve(
                            messages=messages,
                            answer=final_answer,
                            feedback=reflection.feedback
                        )

                        final_answer = improved.answer

                    state = AgentState.SAVE_RESPONSE

                elif state == AgentState.SAVE_RESPONSE:
                    assistant_message = {
                        "role": "assistant",
                        "content": final_answer
                    }

                    self.memory_service.save_message(
                        conversation_id,
                        **assistant_message
                    )

                    response.answer = final_answer
                    state = AgentState.END

            return response

        except AgentError as ex:

            return AIResponse(
                answer=f"Agent error: {ex}"
            )

        except Exception as ex:

            print(ex)

            return AIResponse(
                answer="Unexpected error occurred."
            )


    async def stream(
        self,
        conversation_id,
        user_message,
        profile
    ):
        print(profile)
        try:
            state = AgentState.LOAD_CONTEXT
            MAX_REFLECTION_RETRIES = 2
            while state != AgentState.END:

                messages = []
                plan = None
                response = None
                final_answer = None
                tool_prompt = None
                tools = None

                if state == AgentState.LOAD_CONTEXT:
                    messages = self.context_builder.build_context(
                        conversation_id,
                        user_message
                    )

                    user_message_record = {
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

                    state = AgentState.PLAN

                elif state == AgentState.PLAN:
                    plan = await self.planning_service.create_plan(
                        profile,
                        messages
                    )

                    if plan is None or not hasattr(plan, "tools"):
                        plan = ExecutionPlan(steps=[], tools=[])

                    allowed = set(profile.allowed_tools)
                    selected = [
                        tool
                        for tool in getattr(plan, "tools", [])
                        if tool in allowed
                    ]

                    print(profile.allowed_tools)
                    selected_tools = self.registry.get_selected_tools(selected)
                    tools = self.tool_adapter.adapt(selected_tools)
                    state = AgentState.EXECUTE_PLAN

                elif state == AgentState.EXECUTE_PLAN:
                    messages = self.plan_executor.execute(
                        plan,
                        messages,
                        conversation_id
                    )
                    state = AgentState.TOOL_LOOP

                elif state == AgentState.TOOL_LOOP:
                    iterations = 0

                    while iterations < 5:
                        tool_prompt = self.prompt_builder.build_prompt(
                            profile.system_prompt,
                            messages
                        )

                        response = await self.provider.stream_chat(
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

                    state = AgentState.GENERATE_RESPONSE

                elif state == AgentState.GENERATE_RESPONSE:
                    response_prompt = self.prompt_builder.build(
                        CHAT_RESPONSE_SCHEMA,
                        messages
                    )

                    response = await self.provider.stream_chat(
                        response_prompt
                    )
                    final_answer = response.answer
                    print("final_answer", final_answer)
                    state = AgentState.REFLECT

                elif state == AgentState.REFLECT:
                    for _ in range(MAX_REFLECTION_RETRIES + 1):
                        reflection = await self.reflection_service.review(
                            profile=profile,
                            messages=messages,
                            answer=final_answer
                        )

                        print("reflection", reflection)

                        if reflection.approved:
                            break

                        improved = await self.reflection_service.improve(
                            messages=messages,
                            answer=final_answer,
                            feedback=reflection.feedback
                        )

                        final_answer = improved.answer

                    state = AgentState.SAVE_RESPONSE

                elif state == AgentState.SAVE_RESPONSE:
                    assistant_message = {
                        "role": "assistant",
                        "content": final_answer
                    }

                    self.memory_service.save_message(
                        conversation_id,
                        **assistant_message
                    )

                    response.answer = final_answer
                    state = AgentState.END

            return response

        except AgentError as ex:

            return AIResponse(
                answer=f"Agent error: {ex}"
            )

        except Exception as ex:

            print(ex)

            return AIResponse(
                answer="Unexpected error occurred."
            )