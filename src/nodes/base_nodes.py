from src.models.graph_state import GraphState
import re


def request_user(state: GraphState) -> GraphState:

    message = input("What is your request:")
    state.user_input = message

    return state


def standard_deepseek_prompt(state: GraphState) -> GraphState:
    chat_model_response = state.llm_data.chat_model.invoke(state.llm_data.llm_input)
    response = chat_model_response.content
    output = re.split(r"</?[a-z]+>", response)  # separate text with <think> tags
    state.llm_data.llm_output = output[2]
    return state

def standard_chatbot(state: GraphState) -> GraphState:
    state.llm_data.llm_input = state.user_input
    standard_deepseek_prompt(state)
    print(state.llm_data.llm_output)
    return state


def classification_edge(state: GraphState):
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

    state.llm_data.llm_input = classify_context.format(question=state.user_input)
    standard_deepseek_prompt(state)

    return state.llm_data.llm_output.replace("\n","")