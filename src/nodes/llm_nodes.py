from langchain_community.chat_models import ChatOllama
import re
from src.models.graph_state import GraphState


chat_model = ChatOllama(model="deepseek-r1:8b")


def standard_deepseek_prompt(state: GraphState) -> GraphState:

    chat_model_response = chat_model.invoke(state.user_input)
    response = chat_model_response.content
    output = re.split(r"</?[a-z]+>", response)  # separate text with <think> tags
    state.llm_data.llm_output = output[2]
    print(state.llm_data.llm_output)

    return state


def llm_classifier_edge(state: GraphState):
    classify_context = """ You are given a request from a user.
    You must understand what the user wants and decide which node could help the user.
    Here you have the nodes with their description:
    - chatbot: uses a llm to answer questions in natural language
    - graph: access a graph database to request information
    - end: finish the interaction with the user.
    you must only answer with the name of the node, please do not generate anything more, only the name
    example:
        user: I want to see hoy many recipes i have.
        your answer: graph
    
    user: {question}
    """

    chat_model_response = chat_model.invoke(classify_context.format(question=state.user_input))
    response = chat_model_response.content
    output = re.split(r"</?[a-z]+>", response)  # separate text with <think> tags
    state.llm_data.llm_output = output[2].replace("\n","")
    return state.llm_data.llm_output

