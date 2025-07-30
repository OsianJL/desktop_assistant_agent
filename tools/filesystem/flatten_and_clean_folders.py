import os
import shutil
from rich.console import Console
from utils.path_utils import resolve_path
from langchain.tools import Tool

console = Console()

def flatten_and_clean_folders(input_str: str = "") -> str:
    """
    Moves all files from subdirectories into the root of the specified folder.
    Resolves the path relative to AI_File_Testing.
    """
    folder_path = resolve_path(input_str.strip().strip("'\""))

    console.print(f"[bold green]📁 Target folder resolved to:[/bold green] {folder_path}")

    if not os.path.exists(folder_path):
        console.print(f"[bold red]❌ Folder does not exist:[/bold red] {folder_path}")
        return f"Folder not found: {folder_path}"

    moved_files = 0
    conflicts = 0
    errors = 0

    for root, _, files in os.walk(folder_path, topdown=False):
        if root == folder_path:
            continue  # Skip root folder itself

        relative_subdir = os.path.relpath(root, folder_path)

        for filename in files:
            src_path = os.path.join(root, filename)
            new_filename = filename
            dst_path = os.path.join(folder_path, new_filename)

            # Handle name conflict
            if os.path.exists(dst_path):
                base, ext = os.path.splitext(filename)
                new_filename = f"{relative_subdir.replace(os.sep, '_')}_{base}{ext}"
                dst_path = os.path.join(folder_path, new_filename)

                counter = 1
                while os.path.exists(dst_path):
                    new_filename = f"{relative_subdir.replace(os.sep, '_')}_{base}_{counter}{ext}"
                    dst_path = os.path.join(folder_path, new_filename)
                    counter += 1

                conflicts += 1

            try:
                shutil.move(src_path, dst_path)
                console.print(f"[cyan]📦 Moved:[/cyan] {src_path} → {dst_path}")
                moved_files += 1
            except Exception as e:
                console.print(f"[red]⚠️ Error moving {src_path} → {dst_path}: {e}[/red]")
                errors += 1

    return (
        f"Flattened: {folder_path} — "
        f"{moved_files} files moved, {conflicts} renamed, "
        f"{errors} errors."
    )


# Tool object for ToolLoader
tool = Tool(
    name="DesorganizadorDeCarpetas",
    func=flatten_and_clean_folders,
    description=(
        "Mueve todos los archivos de subcarpetas a la carpeta raíz dentro de AI_File_Testing. "
        "Evita sobrescrituras renombrando archivos si es necesario. "
        "Úsalo con un path relativo como '2023' o con '' para actuar sobre la raíz."
    )
)
