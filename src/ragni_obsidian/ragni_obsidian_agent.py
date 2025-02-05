from langgraph.graph import StateGraph, START, END
from src.models.graph_states import Neo4jBaseState
from src.nodes import llm_nodes, neo4j_nodes


# NEO AGENT GRAPH
neo_graph = StateGraph(Neo4jBaseState)

neo_graph.add_node("node_context", lambda state: neo4j_nodes.get_node_neighbours(state,"Character","name","Tala"))

neo_graph.add_edge(START, "node_context")
neo_graph.add_edge("node_context", END)

neo_app = neo_graph.compile()

neo_input = Neo4jBaseState()

print("""\nHi !! Im Ragni model Neo4j 'o' \n
Im here to provide assistance over your Neo4j Database
What would you like to do? \n
If you want to quit just write quit, bye or exit""")

result_state = neo_app.invoke(neo_input)