import os

import telebot
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from src.models.graph_state import GraphState
from src.models.llm_data import LLMData
from src.nodes import llm_nodes

load_dotenv()

telegram_token = os.getenv("TELEGRAM_TOKEN")

bot_context = """You are an intelligent companion called Ragni.
You have an extrovert personality and answers the questions cheerfully.
The user who is asking you is called {name}, use his or her name when answering.
Give the answer in the same language as the question.
User: {question}
"""

# RAGNI TELEGRAM GRAPH
graph_chat = StateGraph(GraphState)

graph_chat.add_node("chatbot", llm_nodes.standard_deepseek_prompt)

graph_chat.add_edge(START, "chatbot")
graph_chat.add_edge("chatbot", END)

telegram_chat = graph_chat.compile()

# BOT START
bot = telebot.TeleBot(telegram_token)

@bot.message_handler(commands=['chat'])
def send_welcome(message):
    msg = message.text[6:]
    name = message.from_user.first_name
    print(name+": "+msg)
    telegram_chat_input = GraphState(llm_data=LLMData(llm_input=bot_context.format(name=name,question=msg)))
    telegram_chat.invoke(telegram_chat_input)
    bot.reply_to(message, telegram_chat_input.llm_data.llm_output)

bot.infinity_polling()