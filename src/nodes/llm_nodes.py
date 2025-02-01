from langchain_community.chat_models import ChatOllama
import re

from src.models.graph_states import GraphState

chat_model = ChatOllama(model="deepseek-r1:8b")


def standard_deepseek_prompt(state: GraphState) -> GraphState:

    chat_model_response = chat_model.invoke(state["llm_input"])
    response = chat_model_response.content
    output = re.split(r"</?[a-z]+>", response)  # separate text with <think> tags
    state["llm_output"] = output[2]

    return state

