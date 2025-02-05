from langgraph.graph import StateGraph, START, END
from src.models.graph_state import GraphState
from src.nodes import neo4j_nodes


# OBSIDIAN AGENT GRAPH
neo_graph = StateGraph(GraphState)

neo_graph.add_node("node_context", lambda state: neo4j_nodes.get_node_neighbours(state,"Character","name","Tala"))

neo_graph.add_edge(START, "node_context")
neo_graph.add_edge("node_context", END)

neo_app = neo_graph.compile()

neo_input = GraphState()

print("""\nHi !! Im Ragni, model Obsidian ^o^ \n
Im here to provide assistance over your Obsidian Vault
What would you like to do? \n
If you want to quit just write quit, bye or exit""")

result_state = neo_app.invoke(neo_input)