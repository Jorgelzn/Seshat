from langchain_community.chat_models import ChatOllama
import re
from pydantic import BaseModel


chat_model = ChatOllama(model="deepseek-r1:8b")


def standard_deepseek_prompt(state: type[BaseModel]) -> type[BaseModel]:

    chat_model_response = chat_model.invoke(state["llm_input"])
    response = chat_model_response.content
    output = re.split(r"</?[a-z]+>", response)  # separate text with <think> tags
    state["llm_output"] = output[2]

    return state


def llm_actuator_edge(state: type[BaseModel]):

    if state["tobedone"] in ["quit","exit","bye"]:
        return "tobedone"
    else:
        return "tobedone"
        #TODO: make the LLM choose between multiple nodes