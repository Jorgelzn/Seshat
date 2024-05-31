from langchain.tools.render import render_text_description
from langchain_community.chat_models import ChatOllama
from langchain import hub
from langchain.tools import tool
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents import AgentExecutor, load_tools
from langchain.agents.output_parsers import (
    ReActJsonSingleInputOutputParser,
)


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """add two numbers."""
    return a + b


chat_model = ChatOllama(model="llama3")

tools = load_tools([add,multiply])

# setup ReAct style prompt
prompt = hub.pull("hwchase17/react-json")
prompt = prompt.partial(
    tools=render_text_description(tools),
    tool_names=", ".join([t.name for t in tools]),
)

# define the agent
chat_model_with_stop = chat_model.bind(stop=["\nObservation"])
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    }
    | prompt
    | chat_model_with_stop
    | ReActJsonSingleInputOutputParser()
)

# instantiate AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke(
    {
        "input": "what is the result of adding 3 and 5, and then multiplying the result by 10?"
    }
)