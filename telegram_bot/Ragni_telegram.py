import os
import telebot
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama

telegram_token = os.getenv("TELEGRAM_TOKEN")

chat_model = ChatOllama(model="llama3")


template = """You are an intelligent companion called Ragni and only answer questions about fantasy books.
You have an extrovert personality and answers the questions cheerfully.
If the question is not related to these themes, just answer expressing that you only know about those two themes and dont answer to that question.
The user who is asking you is called {name}, use his or her name when asnwering.
Give the answer in the same language as the question.
User: {question}

Ragni:"""

prompt = PromptTemplate.from_template(template)

llm_chain = prompt | chat_model

bot = telebot.TeleBot(telegram_token)


@bot.message_handler(commands=['chat'])
def send_welcome(message):
    msg = message.text[6:]
    name = message.from_user.first_name
    print(name+": "+msg)
    response = llm_chain.invoke({"name":name,"question":msg})
    bot.reply_to(message, response.content)


bot.infinity_polling()
