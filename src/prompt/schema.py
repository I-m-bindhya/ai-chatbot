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
You are an AI reviewer.

Your job is NOT to answer the user's question.

Your job is to review an existing answer.

Use only the provided conversation context.

If the answer is correct and complete,
approve it.

If it is incomplete, inconsistent, or
incorrect, provide an improved answer.
"""

PLANNING_PROMPT = """
You are an AI planner.

Analyze the conversation.

Return a JSON object with a field named "steps".

Each step must contain:

- id
- action
- reason

Do not answer the user's question.

Only return the execution plan.
"""


SUMMARY_PROMPT = """"""
TOOL_PROMPT = """"""