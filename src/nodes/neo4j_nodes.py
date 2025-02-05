import os
from dotenv import load_dotenv
from src.models.graph_state import GraphState

from neo4j import GraphDatabase


load_dotenv()


def get_node_neighbours(state: GraphState, node_type: str, node_id: str,node_id_value: str):
    """Get the information for a place node and all the nodes related to it"""
    driver = GraphDatabase.driver(os.getenv("NEO_URI"), auth=(os.getenv("NEO_USER"), os.getenv("NEO_PASS")))
    with driver.session() as session:
        query_result = session.run(f"match (n:{node_type} {{{node_id}:'{node_id_value}'}})-[r]-(p) return n,type(r),p")
        result = []
        for record in query_result:
            result.append(dict(record['n']))
            result.append(record[1])
            result.append(dict(record['p']))
        state.neo4j_data.cypher_result = result
    driver.close()

    return state

