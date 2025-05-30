import json
import os

import neo4j.exceptions
from dotenv import load_dotenv
from src.models.graph_state import GraphState
from src.nodes.base_nodes import standard_deepseek_prompt
from neo4j import GraphDatabase


load_dotenv()


def get_nodes_with_label(state: GraphState):
    """Get the information for a place node and all the nodes related to it"""

    classify_context = """ You are going to recive a request from the user who wants something from the neo4j graph database.
        Your task is to choose the right parameters for the following query:
        match (n:{{node_type}} {{{{{{node_id}}:'{{node_id_value}}'}}}})-[r]-(p) return n,type(r),p
        You must select the node_type, node_id, and node_id_value, returning the in the following json format:
        "{{
        "node_type":"value of the node type",
        "node_id":"value of the node id",
        "node_id_value":"value of the node id value",
        }}"
        In order to choose these values, you must use the information of the user query, if you think that you dont need one of the values, leave it blank.
        You must only return a string in a valid json format, do not add anything more, no decorators, nothing, only "{{content}}"
        example:
            user: I want to see hoy many books i have.
            your answer: "{{
                "node_type":"book",
                "node_id":"",
                "node_id_value":""
                }}"

        user: {question}
        """

    state.llm_data.llm_input = classify_context.format(question=state.user_input)
    standard_deepseek_prompt(state)
    query_data = json.loads(state.llm_data.llm_output)

    try:
        driver = GraphDatabase.driver(os.getenv("NEO_URI"), auth=(os.getenv("NEO_USER"), os.getenv("NEO_PASS")))
        with driver.session() as session:
            if query_data['node_id']:
                query_result = session.run(f"match (n:{query_data['node_type']} {{{query_data['node_id']}:'{query_data['node_id_value']}'}}) return n")
            else:
                query_result = session.run(
                    f"match (n:{query_data['node_type']}) return n")
            result = []
            for record in query_result:
                result.append(dict(record['n']))
            state.neo4j_data.cypher_result = result
        driver.close()

    except neo4j.exceptions.ServiceUnavailable as e:
        print("The databse service is unavailable")
        return state

    print(state.neo4j_data.cypher_result)
    return state

