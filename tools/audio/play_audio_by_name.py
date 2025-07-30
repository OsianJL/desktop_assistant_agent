import os
from tools.audio.open_audio_with_vlc import open_audio_with_vlc
from utils.path_utils import AGENT_ROOT_DIR
from langchain.tools import Tool

def play_audio_by_name(input_str: str = "") -> str:
    """
    Recursively searches and plays an audio file by name inside AI_File_Testing.
    """
    target_name = input_str.strip().strip("'\"")

    for root, _, files in os.walk(AGENT_ROOT_DIR):
        for file in files:
            if file.lower() == target_name.lower():
                relative_path = os.path.relpath(os.path.join(root, file), AGENT_ROOT_DIR)
                return open_audio_with_vlc(relative_path)

    return f"❌ File '{target_name}' not found anywhere inside AI_File_Testing."


# ToolLoader-compatible export
tool = Tool(
    name="ReproducirAudio",
    func=play_audio_by_name,
    description=(
        "Reproduce un archivo de audio por su nombre. "
        "Lo busca automáticamente dentro de la carpeta AI_File_Testing y todas sus subcarpetas. "
        "Solo debes indicar el nombre exacto del archivo, por ejemplo: 'sotano 1 acustico.mp3'."
    )
)
