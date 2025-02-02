from typing import TypedDict


class StandarChatState(TypedDict):
    llm_input: str
    llm_output: str

class StandarNeo4jState(TypedDict):
    uri: str
    username: str
    password: str
