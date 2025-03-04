import json
import os
from datetime import time
import re
from dotenv import load_dotenv
from neo4j import GraphDatabase


load_dotenv()
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def obsidian_vault_to_neo4j(vault_dir: str):
    obsidian_data = {"nodes": {"note": []}, "relationships": {"LINKED_TO": []}}
    link_pattern = re.compile(r"\[\[.*\]\]")
    for root, dirs, files in os.walk(vault_dir):

        for filename in files:
            file_path = os.path.join(root, filename)
            if ".git" not in file_path and ".obsidian" not in file_path and file_path.endswith(".md"):
                print(os.path.join(root, filename))

                with open(file_path, "r") as f:
                    content = f.read()

                obsidian_data["nodes"]["note"].append({"name": filename.split(".")[0],"content": content.replace("'","-")})

    for root, dirs, files in os.walk(vault_dir):
        for filename in files:
            file_name = filename.split(".")[0]
            curren_node_content = [node["content"]for node in obsidian_data["nodes"]["note"] if node["name"] == file_name]
            if len(curren_node_content) == 1:
                linked_nodes = link_pattern.findall(curren_node_content[0])
                for linked_node in linked_nodes:
                    linked_node = linked_node[2:-2]
                    nodes_names = [name["name"] for name in obsidian_data["nodes"]["note"]]
                    if linked_node in nodes_names:
                        obsidian_data["relationships"]["LINKED_TO"].append({
                                "id_property": "name",
                                "origin": file_name,
                                "target": linked_node,
                                "properties": {}
                              })

    with open(os.path.join(ROOT_DIR, 'src', 'data', 'obsidian.json'), "w") as f:
        f.write(json.dumps(obsidian_data))

    create_neo_rpg_db('obsidian.json')

    os.remove(os.path.join(ROOT_DIR, 'src', 'data', 'obsidian.json'))


def create_neo_rpg_db(data_file_name: str):
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

