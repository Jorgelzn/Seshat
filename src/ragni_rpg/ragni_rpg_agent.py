import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from src.models.graph_states import RPGState
from src.nodes import llm_nodes, neo4j_nodes

load_dotenv()


def quit_game_node(state: RPGState):
    return state


# CHAT GRAPH
rpg_graph = StateGraph(RPGState)

rpg_graph.add_node("gm_response", llm_nodes.gm_response_rpg_prompt)
rpg_graph.add_node("world_context", neo4j_nodes.get_place_context)
rpg_graph.add_node("quit", quit_game_node)

rpg_graph.add_edge(START, "world_context")
rpg_graph.add_edge("world_context", "gm_response")
rpg_graph.add_conditional_edges("gm_response", llm_nodes.rpg_actuator_edge)
rpg_graph.add_edge("quit", END)

rpg_app = rpg_graph.compile()

rpg_input = RPGState(uri=os.getenv("NEO_URI"),
                     username=os.getenv("NEO_USER"),
                     password=os.getenv("NEO_PASS"),
                     player_info="the player is a young explorer with a crow on his shoulder",
                     story_summary="The player lives in a world of high fantasy, he starts his adventure entering in a tavern",
                     player_location="Brazen Hydra"
                     )

print("Welcome to Ragni RPG !!\nIf you want to quit just write quit, bye or exit\n\nYou start your adventure in the Brazen Hydra tavern, what do you want to do?")
rpg_app.invoke(rpg_input)

