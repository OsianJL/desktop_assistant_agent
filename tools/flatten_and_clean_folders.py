import os
import shutil
from rich import print
from rich.console import Console

console = Console()

DEFAULT_FOLDER_BASE = "/mnt/c/Users/osian/Desktop"

def flatten_and_clean_folders(target_folder: str) -> str:
    """
    Flattens all files from subdirectories into the root folder and deletes the subdirectories.

    Args:
        target_folder (str): Absolute path or relative folder name (relative to DEFAULT_FOLDER_BASE)

    Returns:
        str: Summary report of the operation
    """
    # Step 1: Resolve folder path
    if not os.path.isabs(target_folder):
        folder_path = os.path.join(DEFAULT_FOLDER_BASE, target_folder)
    else:
        folder_path = target_folder

    console.print(f"[bold green]📁 Target folder resolved to:[/bold green] {folder_path}")

    # Check if folder exists
    if not os.path.exists(folder_path):
        console.print(f"[bold red]❌ Folder does not exist:[/bold red] {folder_path}")
        return f"Folder not found: {folder_path}"

    moved_files = 0
    conflicts = 0
    errors = 0

    for root, dirs, files in os.walk(folder_path, topdown=False):
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

                # Ensure uniqueness with numeric suffix if still in conflict
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
        f"Flattened and cleaned: {folder_path} — "
        f"{moved_files} files moved, {conflicts} renamed, {errors} errors."
    )
