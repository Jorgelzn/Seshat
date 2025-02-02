import json
import os

from neo4j import GraphDatabase

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_neo_rpg_db(state):
    driver = GraphDatabase.driver(state["uri"], auth=(state["username"], state["password"]))

    with open(os.path.join(ROOT_DIR, 'src', 'ragni_rpg', 'data', 'rpg_data.json')) as f:
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
            query_match += (f" MATCH (a{counter} {{name: '{relation['origin']}'}}), "
                            f" (b{counter} {{name: '{relation['target']}'}})")
            query_merge += f" MERGE (a{counter})-[:{relation_type} {relation_properties}]->(b{counter})"
            counter += 1
    query = query_match + query_merge

    # create relations
    with driver.session() as session:
       session.run(query)

    driver.close()

    return state


def delete_all_nodes(state):

    driver = GraphDatabase.driver(state["uri"], auth=(state["username"], state["password"]))
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    driver.close()

    return state


def get_all_persons(state):
    """Read Persons from database"""
    driver = GraphDatabase.driver(state["uri"], auth=(state["username"], state["password"]))
    with driver.session() as session:
        query_result = session.run("MATCH (p:Person) RETURN p.name AS name")
        result = []
        for record in query_result:
            result.append(record["name"])
        return result
    driver.close()

def get_place_context(state, place_name:str):
    """Get the information for a place node and all the nodes related to it"""
    driver = GraphDatabase.driver(state["uri"], auth=(state["username"], state["password"]))
    with driver.session() as session:
        query_result = session.run("match (n:Lugar{nombre:'" + place_name + "'})-[r]-(p) return n,type(r),p")
        result = []
        for record in query_result:
            result.append(dict(record['n']))
            result.append(record[1])
            result.append(dict(record['p']))
        return str(result)
    driver.close()

    return state