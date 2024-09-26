from langchain_community.chat_models import ChatOllama
from langchain.tools import tool
from operator import itemgetter
from langchain.tools.render import render_text_description
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def add(a: int, b: int) -> int:
    """add two numbers."""
    return a + b


chat_model = ChatOllama(model="llama3")

tools = [add, multiply]


def tool_chain(model_output):
    print(model_output)
    tool_map = {tool.name: tool for tool in tools}
    chosen_tool = tool_map[model_output["name"]]
    return itemgetter("arguments") | chosen_tool


rendered_tools = render_text_description(tools)

tool_prompt = f"""You are an intelligent agent that has access to the following set of tools. Here are the name, description, and arguments with their type of value for each tool:

    {rendered_tools}

    Given the user input, just choose one the tools that is more suitable for the problem to solve.
    You must return only a JSON blob with 'name' and 'arguments' keys. Arguments must have each one their own key-value.
    """

prompt = ChatPromptTemplate.from_messages(
    [("system", tool_prompt), ("user", "{input}")]
)

chain = prompt | chat_model | JsonOutputParser() | tool_chain

chain_result = chain.invoke({"input": "tell me the how much it is 3 plus 5"})

print(chain_result)