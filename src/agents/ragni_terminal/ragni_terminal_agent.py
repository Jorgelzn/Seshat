from langgraph.graph import StateGraph, START, END
from src.models.graph_state import GraphState
from src.nodes.llm_nodes import standard_deepseek_prompt,llm_classifier_edge
from src.nodes.neo4j_nodes import get_node_neighbours
from src.nodes.base_nodes import request_user

# RAGNI TERMINAL GRAPH
ragni_graph = StateGraph(GraphState)

ragni_graph.add_node("request_user", request_user)
ragni_graph.add_node("standard_deepseek_prompt", standard_deepseek_prompt)
ragni_graph.add_node("get_node_neighbours", get_node_neighbours)

ragni_graph.add_edge(START, "request_user")
ragni_graph.add_conditional_edges(
    "request_user",
    llm_classifier_edge,
    {
        "chatbot": "standard_deepseek_prompt",
        "graph": "get_node_neighbours",
        "end": END
    }
)

ragni_graph.add_edge("standard_deepseek_prompt", "request_user")
ragni_graph.add_edge("get_node_neighbours", "request_user")


neo_app = ragni_graph.compile()

print("""\nHi !! Im Ragni ^v^ \n
Im here to provide assistance over your Neo4j Database
What would you like to do? \n""")

neo_app.invoke(GraphState())


