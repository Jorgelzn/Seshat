from typing import Optional

from pydantic import BaseModel


class LLMData(BaseModel):
    llm_output: Optional[str] = ""