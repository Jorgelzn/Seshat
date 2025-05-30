from src.models.graph_state import GraphState


def request_user(state: GraphState) -> GraphState:

    message = input("What does your heart desire:")
    state.user_input = message

    return state