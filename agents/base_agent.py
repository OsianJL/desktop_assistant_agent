from langchain.agents import initialize_agent, Tool
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from tools.hello_tool import say_hello
from tools.organize_by_year import organize_music_by_year
from config.settings import get_openai_model

def create_agent():
    tools = [
        Tool(
            name="Saludo",
            func=say_hello,
            description="Devuelve un saludo simple. Úsalo cuando te pidan saludar."
        ),
        Tool(
            name="OrganizadorMúsicaPorAño",
            func=organize_music_by_year,
            description="Organiza archivos en una carpeta según su año de modificación. Requiere el nombre o ruta absoluta de la carpeta."
        )
    ]
    llm = get_openai_model()
    return initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
