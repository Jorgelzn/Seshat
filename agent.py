from langchain_community.chat_models import ChatOllama
from langchain_community.llms import Ollama
from langchain.tools import tool
from operator import itemgetter
from langchain.tools.render import render_text_description
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def add(a: int, b: int) -> int:
    """add two numbers."""
    return a + b

llm = Ollama(model="llama3")
ll_with_stop = llm.bind(stop=["Observation"])
chat_model = ChatOllama(model="llama3")
chat_model_with_stop = chat_model.bind(stop=["Observation"])

tools = [add, multiply]


def tool_chain(action):
    tool_map = {tool.name: tool for tool in tools}
    chosen_tool = tool_map[action["name"]]
    chain = itemgetter("arguments") | chosen_tool
    return chain.invoke(action)


rendered_tools = render_text_description(tools)

system_prompt = """
You are an intelligent assistant that solves the user task.
You have access to the following set of tools. Here are the names and descriptions for each tool:
{rendered_tools}
You are going to solve the task using several steps.
You must only use information from the steps.
If you have found the solution, just explain it using this structure:
Solution found: the solution.
If there is no step or you dont have enough information in the steps provided please just generate the next step using this structure:
Step: step number
Thought: Reason what you need to do in this step.
Action: Name and arguments of the tool to use as a dictionary with 'name' and 'arguments', each argument is a key-value pairs.
Observation: Output of the tool.

Please do not tell me any other thing apart from the steps or the solution.

User: {input}

<steps>
{steps}
</steps>
"""

prompt = ChatPromptTemplate.from_template(system_prompt)

steps = ""
finish = False
while not finish:

    chain = prompt | ll_with_stop
    chain_result = chain.invoke({"rendered_tools": rendered_tools, "input": "what is the result of adding 3 and 5, and then multiplying the result by 10?",  "steps": steps})

    chain_result = chain_result[:-1]
    action = ""
    if "Solution found" in chain_result:
        finish = True
    else:
        for line in chain_result.splitlines():
            if line.startswith("Action: "):
                action = line[line.find(":")+1:]
                action = action.replace("\'", "\"")
                action = json.loads(action)

        observation = tool_chain(action)
        step = chain_result+"\nObservation:"+str(observation)+"\n"
        print(step)
        steps += step

print(chain_result)