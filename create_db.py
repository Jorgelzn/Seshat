from neo4j import GraphDatabase


uri = "neo4j://localhost:7687"
username = "neo4j"
password = "jorgelzn"

driver = GraphDatabase.driver(uri, auth=(username, password))

def create_person(name):
    with driver.session() as session:
        session.run("CREATE (p:Person {name: $name})", name=name)

def delete_all_nodes():
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")


create_person("Alice")
delete_all_nodes()

driver.close()