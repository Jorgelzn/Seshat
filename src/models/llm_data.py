from typing import Optional

from pydantic import BaseModel


class LLMData(BaseModel):
    llm_input: Optional[str] = ""
    llm_output: Optional[str] = ""