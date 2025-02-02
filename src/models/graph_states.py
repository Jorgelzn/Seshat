from typing import TypedDict, Optional


class StandarChatState(TypedDict):
    llm_input: str
    llm_output: str

class StandarNeo4jState(TypedDict):
    uri: str
    username: str
    password: str  # Should be outside state because static, more for config

class RPGState(TypedDict):
    uri: str
    username: str
    password: str

    player_action: str
    player_info: str
    player_location: str
    story_summary: str
    world_info: str

    llm_output: str