from typing import Optional
from src.models.llm_data import LLMData
from src.models.neo4j_data import Neo4jData
from pydantic import BaseModel

class GraphState(BaseModel):
    user_input: Optional[str] = ""
    llm_data: Optional[LLMData] = LLMData()
    neo4j_data: Optional[Neo4jData] = Neo4jData()


