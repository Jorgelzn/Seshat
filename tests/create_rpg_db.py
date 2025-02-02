import os

from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from src.nodes import neo4j_nodes
from src.models.graph_states import StandarNeo4jState


load_dotenv()

graph = StateGraph(StandarNeo4jState)

graph.add_node("delete_db", neo4j_nodes.delete_all_nodes)
graph.add_node("create_db", neo4j_nodes.create_neo_rpg_db)

graph.add_edge(START, "delete_db")
graph.add_edge("delete_db", "create_db")
graph.add_edge("create_db", END)

app = graph.compile()

db_input = StandarNeo4jState(uri=os.getenv("NEO_URI"),
                             username=os.getenv("NEO_USER"),
                             password=os.getenv("NEO_PASS"))

response = app.invoke(db_input)