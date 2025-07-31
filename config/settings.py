import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

DEFAULT_FOLDER_BASE = "/mnt/c/Users/osian/Desktop"


def load_env():
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in .env file")


def get_openai_model():
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in .env file")

    return ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
    )
