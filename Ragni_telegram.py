import os
import telebot
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceEndpoint

hf_token = os.getenv("HF_TOKEN")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token


template = """
Question: {question}

Answer:"""

prompt = PromptTemplate.from_template(template)

repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

llm = HuggingFaceEndpoint(
    repo_id=repo_id, max_length=128, temperature=0.5, token=hf_token
)
llm_chain = LLMChain(prompt=prompt, llm=llm)

telegram_token = os.getenv("TELEGRAM_TOKEN")

bot = telebot.TeleBot(telegram_token)


@bot.message_handler(commands=['chat'])
def send_welcome(message):
    msg = message.text[6:]
    print(msg)
    response = llm_chain.run(msg)
    bot.reply_to(message, response)


bot.infinity_polling()