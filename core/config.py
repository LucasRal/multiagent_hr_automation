from langchain_openai import ChatOpenAI
from langchain.callbacks import StreamingStdOutCallbackHandler
import os
from dotenv import load_dotenv

load_dotenv()

def create_llm():
    return ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.7,
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()]
    )
