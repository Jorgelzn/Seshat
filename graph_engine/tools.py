from langchain.tools import tool
from neo4j import GraphDatabase
from operator import itemgetter
from langchain.tools.render import render_text_description
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


uri = "neo4j://localhost:7687"
username = "neo4j"
password = "jorgelzn"

driver = GraphDatabase.driver(uri, auth=(username, password))
@tool
def read_persons():
    """Read Persons from database"""
    with driver.session() as session:
        query_result = session.run("MATCH (p:Person) RETURN p.name AS name")
        result = []
        for record in query_result:
            result.append(record["name"])
        return result

@tool
def place_context(place_name:str):
    """Get the information for a place node and all the nodes related to it"""
    with driver.session() as session:
        query_result = session.run("match (n:Place{name:'" + place_name.lower() + "'})-[]->(p) return n,p")
        result = []
        for record in query_result:
            result.append(dict(record['n']))
            result.append(dict(record['p']))
        return str(result)

tools = [read_persons,place_context]

def tool_chain(model_output):
    #print(model_output)
    tool_map = {tool.name: tool for tool in tools}
    chosen_tool = tool_map[model_output["name"]]
    return itemgetter("arguments") | chosen_tool


def tool_call(chat_model, user_input) -> str:
    rendered_tools = render_text_description(tools)
    tool_prompt = f"""You are an intelligent agent that has access to the following set of tools. Here are the name, description, and arguments with their type of value for each tool:

    {rendered_tools}

    Given the user input, just choose one the tools that is more suitable for the problem to solve.
    You must return only a JSON blob with 'name' and 'arguments' keys. Arguments must have each one their own key-value.
    """
    #print(tool_prompt)
    prompt = ChatPromptTemplate.from_messages(
        [("system", tool_prompt), ("user", "{input}")]
    )

    chain = prompt | chat_model | JsonOutputParser() | tool_chain

    return chain.invoke({"input": user_input})