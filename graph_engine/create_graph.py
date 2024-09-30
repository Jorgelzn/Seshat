from neo4j import GraphDatabase
import json


def build_db():

    with open("graph_data.json") as f:
        data = json.load(f)

    query = ""
    counter = 0

    #add characters
    for personaje in data["personajes"]:
        query += f"MERGE (p{counter}:Personaje {{nombre: '{personaje['nombre_nodo']}', descripcion: '{personaje['descripcion_nodo']}'}}) "
        counter += 1

    #add places
    for lugar in data["lugares"]:
        query += f"MERGE (l{counter}:Lugar {{nombre: '{lugar['nombre_nodo']}', descripcion: '{lugar['descripcion_nodo']}'}}) "
        counter += 1

    #create nodes
    with driver.session() as session:
        session.run(query)

    query_match = ""
    query_merge = ""
    counter = 0
    #add relations
    for relacion in data["relaciones"]:
        query_match += (f" MATCH (a{counter} {{nombre: '{relacion['nombre_nodo_origen']}'}}), "
                        f" (b{counter} {{nombre: '{relacion['nombre_nodo_destino']}'}})")
        query_merge += f" MERGE (a{counter})-[:{relacion['nombre_relacion']}]->(b{counter})"
        counter += 1
    query = query_match + query_merge
    #create relations
    with driver.session() as session:
        session.run(query)


def delete_all_nodes():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")



if __name__ == "__main__":

    uri = "neo4j://localhost:7687"
    username = "neo4j"
    password = "jorgelzn"

    driver = GraphDatabase.driver(uri, auth=(username, password))

    build_db()
    #delete_all_nodes()

    driver.close()