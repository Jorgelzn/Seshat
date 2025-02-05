from typing import TypedDict, Optional

from pydantic import BaseModel


class StandardChatState(BaseModel):
    llm_output: Optional[str] = None


class Neo4jBaseState(BaseModel):
    cypher_result: Optional[str] = "None"
