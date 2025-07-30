import os
import shutil
from rich.console import Console
from utils.path_utils import resolve_path  # 👈 nuevo import

console = Console()

def flatten_and_clean_folders(target_folder: str) -> str:
    """
    Flattens all files from subdirectories into the root folder.

    Args:
        target_folder (str): Absolute path or relative folder name (relative to DEFAULT_FOLDER_BASE)

    Returns:
        str: Summary report of the operation
    """
    folder_path = resolve_path(target_folder)  # 👈 unificación de resolución

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
