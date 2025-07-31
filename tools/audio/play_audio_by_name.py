import os
from rich.console import Console
from tools.audio.open_audio_with_vlc import open_audio_with_vlc
from utils.path_utils import AGENT_ROOT_DIR
from utils.file_safety import validate_file_operation
from langchain.tools import Tool

console = Console()


def play_audio_by_name(input_str: str = "") -> str:
    """
    Recursively searches and plays an audio file by name inside AI_File_Testing.
    Only allows playing audio files within the AGENT_ROOT_DIR.
    """
    target_name = input_str.strip().strip("'\"")

    if not target_name:
        return "❌ Please provide a file name to search for."

    # First validate that we can read from AGENT_ROOT_DIR
    is_safe, message = validate_file_operation(
        operation="read",
        target_path="",  # Root directory
    )

    if not is_safe:
        console.print(f"[bold red]❌ Security check failed:[/bold red] {message}")
        return f"Security error: {message}"

    try:
        for root, _, files in os.walk(AGENT_ROOT_DIR):
            for file in files:
                if file.lower() == target_name.lower():
                    # Get path relative to AGENT_ROOT_DIR for validation
                    relative_path = os.path.relpath(
                        os.path.join(root, file), AGENT_ROOT_DIR
                    )

                    # Debug logging
                    console.print(f"[blue]Debug - Found file:[/blue]")
                    console.print(f"  Original: {os.path.join(root, file)}")
                    console.print(f"  Relative to AI_File_Testing: {relative_path}")

                    # Validate that we can read this specific file
                    is_safe_file, msg_file = validate_file_operation(
                        operation="read",
                        target_path=relative_path,
                        allowed_types=["audio"],  # Only allow audio files
                    )

                    if not is_safe_file:
                        console.print(
                            f"[red]⚠️ Security check failed for file:[/red] {msg_file}"
                        )
                        continue

                    return open_audio_with_vlc(relative_path)

        return f"❌ File '{target_name}' not found anywhere inside AI_File_Testing."

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        console.print(f"[bold red]❌ {error_msg}[/bold red]")
        return error_msg


# ToolLoader-compatible export
tool = Tool(
    name="ReproducirAudio",
    func=play_audio_by_name,
    description=(
        "Reproduce un archivo de audio por su nombre. "
        "Lo busca automáticamente dentro de la carpeta AI_File_Testing y todas sus subcarpetas. "
        "Solo debes indicar el nombre exacto del archivo, por ejemplo: 'sotano 1 acustico.mp3'."
    ),
)
