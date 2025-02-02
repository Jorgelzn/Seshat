from langchain_community.chat_models import ChatOllama
import re

from src.models.graph_states import StandarChatState,RPGState

chat_model = ChatOllama(model="deepseek-r1:8b")


def standard_deepseek_prompt(state: StandarChatState) -> StandarChatState:

    chat_model_response = chat_model.invoke(state["llm_input"])
    response = chat_model_response.content
    output = re.split(r"</?[a-z]+>", response)  # separate text with <think> tags
    state["llm_output"] = output[2]

    return state


def gm_response_rpg_prompt(state: RPGState) -> RPGState:
    state["player_action"] = input("Player:")
    GM_PROMPT = """You are a game director that determine what happens to a player based on its actions.
    You must act as if you where the narrator and npcs of the story.
    If the player wants to talk or do something to the npcs, you must act as them, and interact with the player.
    And if the player wants to perform an action in the world, tell him what happens next.
    You have the following info:
    Player description: information about the player.
    world information: information about the current place.
    Player action: action or dialogue from player.
    Story summary: the story of the player so far.
    Only answer with the response you would give to the player, try to keep short answers.
    Do not invent anything, only answer with the information available in the world info.
    If you dont have the information to resolve an action, just say that action is not possible.
    Player description: {player_info}
    Player action: {player_action}
    World information: {world_info}
    Story summary: {story_info}""".format(player_info=state["player_info"],
                                          player_action=state["player_action"],
                                          world_info=state["world_info"],
                                          story_info=state["story_summary"])

    chat_model_response = chat_model.invoke(GM_PROMPT)
    response = chat_model_response.content
    output = re.split(r"</?[a-z]+>", response)  # separate text with <think> tags
    state["llm_output"] = output[2]
    print(state["llm_output"])
    update_story_prompt = """
    Given the current action and the previous story of an rpg player, you must perform a short summary of the whole story so far.
    Make it as short as possible taking into account all the relevant moments.
    Current Action: {current_action}
    Story summary: {story_info}
    Answer only with the story summary, nothing more.
    """.format(current_action=state["llm_output"],story_info=state["story_summary"])

    chat_model_response = chat_model.invoke(update_story_prompt)
    response = chat_model_response.content
    output = re.split(r"</?[a-z]+>", response)  # separate text with <think> tags
    state["story_summary"] = output[2]

    return state

def rpg_actuator_edge(state: RPGState):
    if state["player_action"] in ["quit","exit","bye"]:
        return "quit"
    else:
        return "gm_response"
        #TODO: make the LLM choose between multiple actions