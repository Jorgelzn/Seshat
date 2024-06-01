import os
import telebot
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceEndpoint


hf_token = os.getenv("HF_TOKEN")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token
telegram_token = os.getenv("TELEGRAM_TOKEN")
repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

llm = HuggingFaceEndpoint(repo_id=repo_id,temperature=0.5)


template = """You are an intelligent bird companion called Ragni and only answer questions about fantasy books.
If the question is not related to these themes, just answer expressing that you only know about those two themes and dont answer to that question.
The user who is asking you is called {name}, use his or her name to answer the question.
User: {question}

Ragni:"""

prompt = PromptTemplate.from_template(template)

llm_chain = prompt | llm

bot = telebot.TeleBot(telegram_token)


@bot.message_handler(commands=['chat'])
def send_welcome(message):
    msg = message.text[6:]
    name = message.from_user.first_name
    print(name+": "+msg)
    response = llm_chain.invoke({"name":name,"question":msg})
    bot.reply_to(message, response)


bot.infinity_polling()
