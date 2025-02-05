from typing import Optional

from pydantic import BaseModel


class Neo4jData(BaseModel):
    cypher_result: Optional[str] = "None"