from typing import Optional
from langchain_community.chat_models import ChatOllama
from langchain_core.language_models import chat_models
from pydantic import BaseModel


class LLMData(BaseModel):
    chat_model: ChatOllama = ChatOllama(model="deepseek-r1:8b")
    llm_input: Optional[str] = ""
    llm_output: Optional[str] = ""
