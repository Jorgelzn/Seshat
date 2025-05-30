from langgraph.graph import StateGraph, START, END
from src.models.graph_state import GraphState
from src.nodes.base_nodes import request_user, standard_chatbot,classification_edge
from src.nodes.neo4j_nodes import get_nodes_with_label

# RAGNI TERMINAL GRAPH
ragni_graph = StateGraph(GraphState)

ragni_graph.add_node("request_user", request_user)
ragni_graph.add_node("standard_chatbot", standard_chatbot)
ragni_graph.add_node("get_nodes_with_label", get_nodes_with_label)

ragni_graph.add_edge(START, "request_user")
ragni_graph.add_conditional_edges(
    "request_user",
    classification_edge,
    {
        "chatbot": "standard_chatbot",
        "graph": "get_nodes_with_label",
        "end": END
    }
)

ragni_graph.add_edge("standard_chatbot", "request_user")
ragni_graph.add_edge("get_nodes_with_label", "request_user")


neo_app = ragni_graph.compile()

print("""\nHi !! Im Ragni ^v^
Im here to provide assistance with your knowledge base\n""")

neo_app.invoke(GraphState())


