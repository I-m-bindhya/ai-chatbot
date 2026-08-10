from src.prompt.versions import v1


PROMPT_VERSIONS = {
    "v1": v1,
}


ACTIVE_PROMPT_VERSION = "v1"


def get_prompts():
    return PROMPT_VERSIONS[ACTIVE_PROMPT_VERSION]