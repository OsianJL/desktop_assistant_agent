import os
from rich.console import Console
from utils.path_utils import resolve_path

console = Console()

def delete_empty_subdirs(folder_path: str) -> str:
    """
    Deletes all empty subdirectories within the given folder path.

    Args:
        folder_path (str): Absolute path or relative folder name

    Returns:
        str: Summary of deletion process
    """
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
