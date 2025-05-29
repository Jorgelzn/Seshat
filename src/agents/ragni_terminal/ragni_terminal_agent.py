from langgraph.graph import StateGraph, START, END
from src.models.graph_state import GraphState
from src.models.llm_data import LLMData
from src.nodes import neo4j_nodes
from src.nodes.llm_nodes import standard_deepseek_prompt

# RAGNI TERMINAL GRAPH
ragni_graph = StateGraph(GraphState)

ragni_graph.add_node("deepseek_response", standard_deepseek_prompt)

ragni_graph.add_edge(START, "deepseek_response")
ragni_graph.add_edge("deepseek_response", END)

neo_app = ragni_graph.compile()


print("""\nHi !! Im Ragni ^o^ \n
Im here to provide assistance over your Neo4j Database
What would you like to do? \n
If you want to quit just write quit, bye or exit""")

message = "solve me the following ecuation 7*(4+2*2)"
graph_state = GraphState(llm_data=LLMData(llm_input=message))

result_state = neo_app.invoke(graph_state)
print(graph_state.llm_data.llm_output)

