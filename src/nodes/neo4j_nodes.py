import json
import os
from typing import Type

from dotenv import load_dotenv
from src.models.graph_state import GraphState

from neo4j import GraphDatabase


load_dotenv()
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_neo_rpg_db(data_file_name:str):
    driver = GraphDatabase.driver(os.getenv("NEO_URI"), auth=(os.getenv("NEO_USER"), os.getenv("NEO_PASS")))

    with open(os.path.join(ROOT_DIR, 'src', 'data', data_file_name)) as f:
        data = json.load(f)

    query = ""
    counter = 0

    # add nodes
    for node_type, node_list in data["nodes"].items():
        for node in node_list:
            properties = ""
            for node_property, property_value in node.items():
                properties += f"{node_property}: '{property_value}', "
            properties = properties[:-2]
            query += f"MERGE (p{counter}:{node_type} {{{properties}}}) "
            counter += 1

    # create nodes
    with driver.session() as session:
        session.run(query)

    # add relations
    query_match = ""
    query_merge = ""
    counter = 0
    for relation_type, relation_list in data["relationships"].items():
        for relation in relation_list:
            relation_properties = ""
            if len(relation["properties"]) > 0:
                for relation_property, relation_property_value in relation["properties"].items():
                    relation_properties += f"{relation_property}: '{relation_property_value}', "
                relation_properties = f"{{{relation_properties[:-2]}}}"
            query_match += (f" MATCH (a{counter} {{{relation['id_property']}: '{relation['origin']}'}}), "
                            f" (b{counter} {{{relation['id_property']}: '{relation['target']}'}})")
            query_merge += f" MERGE (a{counter})-[:{relation_type} {relation_properties}]->(b{counter})"
            counter += 1
    query = query_match + query_merge

    # create relations
    with driver.session() as session:
       session.run(query)

    driver.close()



def delete_all_nodes():

    driver = GraphDatabase.driver(os.getenv("NEO_URI"), auth=(os.getenv("NEO_USER"), os.getenv("NEO_PASS")))
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    driver.close()


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

