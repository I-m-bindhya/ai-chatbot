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