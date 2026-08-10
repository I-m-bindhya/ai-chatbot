import hashlib
import json


def make_cache_key(
    model,
    messages,
    tools=None,
    prompt_version=None
):
    payload = {
        "model": model,
        "messages": messages,
        "tools": tools,
        "prompt_version": prompt_version
    }

    raw = json.dumps(
        payload,
        sort_keys=True,
        default=str
    )

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()