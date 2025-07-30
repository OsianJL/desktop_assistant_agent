import os
import subprocess
from utils.path_utils import resolve_path
from rich.console import Console
from langchain.tools import Tool

console = Console()

# Correct VLC path for your system
VLC_PATH = "/mnt/c/Program Files (x86)/VideoLAN/VLC/vlc.exe"


def open_audio_with_vlc(input_str: str = "") -> str:
    """
    Opens an audio file with VLC media player.
    Input must be the relative path (e.g. '2023/test.mp3') or just 'test.mp3'.
    """
    try:
        file_path = resolve_path(input_str.strip().strip("'\""))

        if not os.path.exists(file_path):
            msg = f"❌ File not found: {file_path}"
            console.print(f"[red]{msg}[/red]")
            return msg

        # Convert WSL path to Windows path
        windows_path = (
            subprocess.check_output(["wslpath", "-w", file_path]).decode().strip()
        )

        subprocess.Popen([VLC_PATH, windows_path])
        msg = f"🎵 Playing: {windows_path}"
        console.print(f"[green]{msg}[/green]")
        return msg
    except Exception as e:
        msg = f"⚠️ Failed to open file with VLC: {e}"
        console.print(f"[red]{msg}[/red]")
        return msg


# ToolLoader-compatible export
tool = Tool(
    name="ReproductorDeAudio",
    func=open_audio_with_vlc,
    description=(
        "Abre un archivo de audio con VLC. "
        "Recibe una ruta relativa a la carpeta AI_File_Testing, como '2023/test.mp3' o 'grabaciones/test2.m4a'. "
        "También puedes usar solo el nombre si el archivo está en la raíz."
    ),
)
