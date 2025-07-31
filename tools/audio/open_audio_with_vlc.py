import os
import subprocess
from utils.path_utils import resolve_path, AGENT_ROOT_DIR
from utils.file_safety import validate_file_operation
from rich.console import Console
from langchain.tools import Tool

console = Console()

# Correct VLC path for your system
VLC_PATH = "/mnt/c/Program Files (x86)/VideoLAN/VLC/vlc.exe"


def open_audio_with_vlc(input_str: str = "") -> str:
    """
    Opens an audio file with VLC media player.
    Input must be the relative path (e.g. '2023/test.mp3') or just 'test.mp3'.
    Only allows playing audio files within the AGENT_ROOT_DIR.
    """
    try:
        # First validate that the file path is within AGENT_ROOT_DIR
        file_path = input_str.strip().strip("'\"")
        is_safe, message = validate_file_operation(
            operation="read",
            target_path=file_path,
            allowed_types=["audio"],  # Only allow audio files
        )

        if not is_safe:
            console.print(f"[bold red]❌ Security check failed:[/bold red] {message}")
            return f"Security error: {message}"

        # If safe, resolve the path
        file_path = resolve_path(file_path)

        # Debug logging
        rel_path = os.path.relpath(file_path, AGENT_ROOT_DIR)
        console.print(f"[blue]Debug - Opening file:[/blue]")
        console.print(f"  Original: {file_path}")
        console.print(f"  Relative to AI_File_Testing: {rel_path}")

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
    name="AudioPlayer",
    func=open_audio_with_vlc,
    description=(
        "Opens an audio file with VLC. "
        "Takes a relative path to the AI_File_Testing folder, like '2023/test.mp3' or 'music/test2.m4a'. "
        "You can also use just the filename if the file is in the root."
    ),
)
