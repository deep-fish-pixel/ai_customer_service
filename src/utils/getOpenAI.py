import os
from langchain_openai import ChatOpenAI

def getChatOpenAI(temperature: float = 0):
  return ChatOpenAI(
    # api_key=os.getenv("OPENAI_API_KEY"),
    # model_name="gpt-3.5-turbo",
    model="qwen-max",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("API_BASE_URL"),
    temperature=temperature
  )