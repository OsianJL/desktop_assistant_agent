from langchain.agents import initialize_agent, Tool, AgentExecutor  # type: ignore
from langchain.agents.agent_types import AgentType
from langchain.tools import BaseTool
from tools.hello_tool import say_hello
from tools.filesystem.organize_by_year import organize_music_by_year
from tools.filesystem.flatten_and_clean_folders import flatten_and_clean_folders
from tools.filesystem.delete_empty_subdirs import delete_empty_subdirs
from tools.audio.open_audio_with_vlc import open_audio_with_vlc
from tools.audio.play_audio_by_name import play_audio_by_name
from config.settings import get_openai_model
from typing import List


def create_agent() -> AgentExecutor:
    tools: List[BaseTool] = [
        Tool(
            name="Saludo",
            func=say_hello,
            description="Devuelve un saludo simple. Úsalo cuando te pidan saludar.",
        ),
        Tool(
            name="OrganizadorMúsicaPorAño",
            func=organize_music_by_year,
            description="Organiza archivos en una carpeta según su año de modificación. Requiere el nombre o ruta absoluta de la carpeta.",
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
        Tool(
            name="ReproductorDeAudio",
            func=open_audio_with_vlc,
            description="Abre un archivo de audio con VLC. Recibe una ruta absoluta o relativa a DEFAULT_FOLDER_BASE.",
        ),
        Tool(
            name="ReproducirAudio",
            func=play_audio_by_name,
            description=(
                "Reproduce un archivo de audio por su nombre. "
                "Busca automáticamente en la carpeta AI_File_Testing y todas sus subcarpetas. "
                "Solo debes indicar el nombre exacto del archivo, por ejemplo: 'sotano 1 acustico.mp3'."
            ),
        ),
    ]

    llm = get_openai_model()
    return initialize_agent(
        tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )
