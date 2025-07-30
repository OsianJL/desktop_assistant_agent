import os
import subprocess
from utils.path_utils import resolve_path
from rich.console import Console

console = Console()

# Correct VLC path for your system
VLC_PATH = "/mnt/c/Program Files (x86)/VideoLAN/VLC/vlc.exe"

def open_audio_with_vlc(filepath: str) -> str:
    """
    Opens an audio file with VLC media player using the provided file path.
    """
    try:
        file_path = resolve_path(filepath)

        if not os.path.exists(file_path):
            msg = f"❌ File not found: {file_path}"
            console.print(f"[red]{msg}[/red]")
            return msg
        
        # Convert WSL path to Windows path
        windows_path = subprocess.check_output(["wslpath", "-w", file_path]).decode().strip()

        subprocess.Popen([VLC_PATH, windows_path])
        msg = f"🎵 Playing: {windows_path}"
        console.print(f"[green]{msg}[/green]")
        return msg
    except Exception as e:
        msg = f"⚠️ Failed to open file with VLC: {e}"
        console.print(f"[red]{msg}[/red]")
        return msg
