import os
from rich.console import Console
from utils.path_utils import resolve_path
from langchain.tools import Tool

console = Console()

def delete_empty_subdirs(input_str: str = "") -> str:
    folder_path = input_str.strip().strip("'\"")
    folder_path = resolve_path(folder_path)
    deleted_folders = 0
    errors = 0

    if not os.path.exists(folder_path):
        console.print(f"[bold red]❌ Folder does not exist:[/bold red] {folder_path}")
        return f"Folder not found: {folder_path}"

    for root, _, _ in os.walk(folder_path, topdown=False):
        if root == folder_path:
            continue  # Never delete root

        try:
            if not os.listdir(root):
                os.rmdir(root)
                console.print(f"[green]🗑️ Deleted empty folder:[/green] {root}")
                deleted_folders += 1
        except Exception as e:
            console.print(f"[red]⚠️ Error deleting folder {root}: {e}[/red]")
            errors += 1

    return f"🧹 Deleted {deleted_folders} empty folders. Errors: {errors}."

# ToolLoader-compatible export
tool = Tool(
    name="BorradorDeCarpetasVacias",
    func=delete_empty_subdirs,
    description=(
        "Elimina subcarpetas vacías dentro de una carpeta relativa a AI_File_Testing. "
        "Por ejemplo: '2024', 'grabaciones', o simplemente '' para la raíz."
    )
)
