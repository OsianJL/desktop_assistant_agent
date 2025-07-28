import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

DEFAULT_FOLDER_BASE = "/mnt/c/Users/osian/Desktop"

def load_env():
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("No se encontró la clave OPENAI_API_KEY en el archivo .env")

def get_openai_model():
    api_key = os.getenv("OPENAI_API_KEY")
    return ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=api_key)
