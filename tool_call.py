from langchain_community.chat_models import ChatOllama
from langchain.tools import tool
from operator import itemgetter
from langchain.tools.render import render_text_description
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
username = "neo4j"
password = "jorgelzn"

driver = GraphDatabase.driver(uri, auth=(username, password))

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def add(a: int, b: int) -> int:
    """add two numbers."""
    return a + b

@tool
def read_persons():
    """Read Persons from database"""
    with driver.session() as session:
        query_result = session.run("MATCH (p:Person) RETURN p.name AS name")
        result = []
        for record in query_result:
            result.append(record["name"])
        return result


chat_model = ChatOllama(model="llama3")

tools = [add, multiply,read_persons]


def tool_chain(model_output):
    print(model_output)
    tool_map = {tool.name: tool for tool in tools}
    chosen_tool = tool_map[model_output["name"]]
    return itemgetter("arguments") | chosen_tool


rendered_tools = render_text_description(tools)

system_prompt = f"""You are an intelligent agent that has access to the following set of tools. Here are the names and descriptions for each tool:

{rendered_tools}

Given the user input, just choose one the tools that is more suitable for the problem to solve.
Return your response as a JSON blob with 'name' and 'arguments' keys. Arguments must have each one their own key-value pair.
You must only return the tool name and arguments, nothing more.
"""

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("user", "{input}")]
)

chain = prompt | chat_model | JsonOutputParser() | tool_chain

chain_result = chain.invoke({"input": "tell me the name of all persons in database"})

print(chain_result)
driver.close()