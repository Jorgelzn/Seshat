from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
import tools
chat_model = ChatOllama(model="llama3")

world_info = tools.tool_call(chat_model, "Tell me the information about the Hydra Borracha ")
template = """You are a game director that determine what happens to a player based on its action.
You have the following info:
player info: info about the player.
world info: info about the current place the player is in
user action: action or dialogue from player.
story info: the story of the player so far.
Only answer with the response you would give to the player, try to keep short answers.
Do not invent anything, only answer with the information available in the world info.
If you dont have the information to resolve an action, just say that action is not possible.
Player info: {player_info}
World info: {world_info}
User action: {player_action}
Story info:\n{story_info}"""
prompt = PromptTemplate.from_template(template)
story = ""
print(world_info)
story_counter = []
context_limit = 99999999999999999999999999999999999999999999999
while True:
    llm_chain = prompt | chat_model
    user_input = input("text:")

    response = llm_chain.invoke({"player_info": "its a mage",
                                 "world_info": world_info,
                                 "player_action": user_input,
                                 "story_info": story})

    print(response.content)
    story_point = "user:" + user_input + "\nmaster:" + response.content + "\n"
    story_counter.append(len(story_point))
    story += story_point
    context_len = len(template)+len(world_info)+len(user_input)+len(story)
    if context_len >= context_limit:
        story = story[story_counter.pop(0):]

tools.driver.close()