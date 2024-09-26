from neo4j import GraphDatabase
import json


def build_db():

    with open("graph_data.json") as f:
        data = json.load(f)

    query = "CREATE"
    counter = 0

    #add characters
    for personaje in data["personajes"]:
        query += f" (p{counter}:Personaje {{nombre: '{personaje['nombre_nodo']}', descripcion: '{personaje['descripcion_nodo']}'}}), "
        counter += 1

    #add places
    for lugar in data["lugares"]:
        query += f" (l{counter}:Lugar {{nombre: '{lugar['nombre_nodo']}', descripcion: '{lugar['descripcion_nodo']}'}}), "
        counter += 1

    #create nodes
    with driver.session() as session:
        session.run(query[:-2])

    query = ""
    counter = 0
    #add relations
    for relacion in data["relaciones"]:
        query += (f" MATCH (a{counter} {{nombre: '{relacion['nombre_nodo_origen']}'}}),"
                  f" (b{counter} {{nombre: '{relacion['nombre_nodo_destino']}'}})"
                  f" CREATE (a{counter})-[:{relacion['nombre_relacion']}]->(b{counter}), ")
        counter += 1
    #create relations
    with driver.session() as session:
        session.run(query[:-2])


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