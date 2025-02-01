import os

from dotenv import load_dotenv
from langchain_community.chat_models import ChatOllama
from langgraph.graph import StateGraph, START, END

from src.models.graph_states import GraphState

load_dotenv()

telegram_token = os.getenv("TELEGRAM_TOKEN")

template = """You are a game director that determine what happens to a player based on its action.
You have the following info:
player info: info about the player.
world info: info about the current place the player is in
user action: action or dialogue from player.
story info: the story of the player so far.
Only answer with the response you would give to the player, try to keep short answers.
Do not invent anything, only answer with the information available in the world info.
If you dont have the information to resolve an action, just say that action is not possible.
Player info: {player_info}
World info: {world_info}
User action: {player_action}
Story info:\n{story_info}"""

# CHAT GRAPH
graph_chat = StateGraph(GraphState)

graph_chat.add_node("chatbot", llm_nodes.standard_deepseek_prompt)

graph_chat.add_edge(START, "chatbot")
graph_chat.add_edge("chatbot", END)

telegram_chat = graph_chat.compile()

while True:
    user_input = input("text:")

    if user_input in ["bye","end","quit","exit"]:
        break

print("Agent terminated")