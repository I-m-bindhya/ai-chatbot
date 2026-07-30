CHAT_RESPONSE_SCHEMA = """
Return ONLY valid JSON.

{
    "answer": "string",
    "confidence": "high | medium | low",
    "topics": [
        "string"
    ]
    "reasoning": "string"
}

Do not return markdown.
DO have a single line of reasoning field in it
Do not wrap in ```json.
Return only JSON.
"""



REFLECTION_PROMPT = """
You are reviewing an AI answer.

Return ONLY valid JSON.

{
  "approved": true,
  "feedback": ""
}

If the answer is incorrect:

{
  "approved": false,
  "feedback": "Explain what should be improved."
}

Do not write markdown.
Do not use ```json.
Do not add explanations.
"""

IMPROVEMENT_PROMPT = """
The previous answer has issues.

Feedback:

{feedback}

Rewrite the answer.

Do not mention the feedback.

Return only the improved answer.
"""

PLANNING_PROMPT = """
You are an AI planner.

Analyze the conversation.

Return a JSON object with a field named "steps".

Each step must contain:

- id
- action
- reason


The allowed actions are:

- retrieve_memory
- call_tool
- generate_answer
- reflect
- summarize_memory
- list_conversations

Never invent new action names.

Available Tools

list_chats
search_memory

When a tool is needed, include its name in the tools array.

Example:

{
  "steps":[
      {
          "id":1,
          "action":"list_conversations",
          "reason":"User requested conversations."
      }
  ],
    "tools":[
        "list_chats"
    ]
}

Do not answer the user's question.

Only return the execution plan.
"""


SUMMARY_PROMPT = """"""
TOOL_PROMPT = """"""