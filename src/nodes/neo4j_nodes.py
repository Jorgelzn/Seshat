import json
import os

from neo4j import GraphDatabase

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_neo_rpg_db(uri,username,password):
    driver = GraphDatabase.driver(uri, auth=(username, password))

    with open(os.path.join(ROOT_DIR, 'src', 'rpg', 'data', 'rpg_data.json')) as f:
        data = json.load(f)

    query = ""
    counter = 0

    # add characters
    for personaje in data["personajes"]:
        query += f"MERGE (p{counter}:Personaje {{nombre: '{personaje['nombre_nodo']}', descripcion: '{personaje['descripcion_nodo']}'}}) "
        counter += 1

    # add places
    for lugar in data["lugares"]:
        query += f"MERGE (l{counter}:Lugar {{nombre: '{lugar['nombre_nodo']}', descripcion: '{lugar['descripcion_nodo']}'}}) "
        counter += 1

    # create nodes
    with driver.session() as session:
        session.run(query)

    query_match = ""
    query_merge = ""
    counter = 0
    # add relations
    for relacion in data["relaciones"]:
        query_match += (f" MATCH (a{counter} {{nombre: '{relacion['nombre_nodo_origen']}'}}), "
                        f" (b{counter} {{nombre: '{relacion['nombre_nodo_destino']}'}})")
        query_merge += f" MERGE (a{counter})-[:{relacion['nombre_relacion']}]->(b{counter})"
        counter += 1
    query = query_match + query_merge
    # create relations
    with driver.session() as session:
        session.run(query)

    driver.close()


def delete_all_nodes(state,uri,username,password):
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    driver.close()


def get_all_persons(state,uri,username,password):
    """Read Persons from database"""
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        query_result = session.run("MATCH (p:Person) RETURN p.name AS name")
        result = []
        for record in query_result:
            result.append(record["name"])
        return result
    driver.close()

def get_place_context(state,uri,username,password, place_name:str):
    """Get the information for a place node and all the nodes related to it"""
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        query_result = session.run("match (n:Lugar{nombre:'" + place_name + "'})-[r]-(p) return n,type(r),p")
        result = []
        for record in query_result:
            result.append(dict(record['n']))
            result.append(record[1])
            result.append(dict(record['p']))
        return str(result)
    driver.close()