from langchain.agents import initialize_agent, Tool, AgentExecutor  # type: ignore
from langchain.agents.agent_types import AgentType
from langchain.tools import BaseTool
from tools.hello_tool import say_hello
from tools.organize_by_year import organize_music_by_year
from tools.flatten_and_clean_folders import flatten_and_clean_folders
from tools.delete_empty_subdirs import delete_empty_subdirs  # 👈 nuevo import
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
            name="DesorganizadorDeCarpetas",
            func=flatten_and_clean_folders,
            description=(
                "Mueve todos los archivos de subcarpetas a la carpeta raíz. "
                "Si hay conflictos de nombre, añade prefijos únicos para evitar sobrescrituras. "
                "No elimina ninguna carpeta. "
                "Recibe una ruta absoluta o un nombre de carpeta relativa a DEFAULT_FOLDER_BASE."
            ),
        ),
        Tool(
            name="BorradorDeCarpetasVacias",
            func=delete_empty_subdirs,
            description=(
                "Elimina todas las subcarpetas vacías dentro de una carpeta dada. "
                "Nunca borra la carpeta raíz. Úsalo cuando te pidan limpiar carpetas vacías. "
                "Recibe una ruta absoluta o relativa a DEFAULT_FOLDER_BASE."
            ),
        ),
    ]

    llm = get_openai_model()
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
