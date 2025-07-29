from langchain.agents import initialize_agent, Tool, AgentExecutor  # type: ignore
from langchain.agents.agent_types import AgentType
from langchain.tools import BaseTool
from tools.hello_tool import say_hello
from tools.organize_by_year import organize_music_by_year
from tools.flatten_and_clean_folders import flatten_and_clean_folders
from config.settings import get_openai_model
from typing import List

def create_agent() -> AgentExecutor:
    tools: List[BaseTool] = [
        Tool(
            name="Saludo",
            func=say_hello,
            description="Devuelve un saludo simple. Úsalo cuando te pidan saludar."
        ),
        Tool(
            name="OrganizadorMúsicaPorAño",
            func=organize_music_by_year,
            description="Organiza archivos en una carpeta según su año de modificación. Requiere el nombre o ruta absoluta de la carpeta."
        ),
        Tool(
    name="flatten_and_clean_folders",
    func=flatten_and_clean_folders,
    description=(
        "Mueve todos los archivos de subcarpetas a la carpeta raíz y luego elimina todas las carpetas internas. "
        "Usa el nombre de subcarpeta como prefijo si hay conflictos de nombres. "
        "Recibe una ruta absoluta o un nombre de carpeta relativa a DEFAULT_FOLDER_BASE."
    ),
),

    ]
    llm = get_openai_model()
    return initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
