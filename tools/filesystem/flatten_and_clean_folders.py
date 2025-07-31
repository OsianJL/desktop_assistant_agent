import os
import shutil
from rich.console import Console
from utils.path_utils import resolve_path, AGENT_ROOT_DIR
from utils.file_safety import validate_file_operation
from langchain.tools import Tool

console = Console()


def flatten_and_clean_folders(input_str: str = "") -> str:
    """
    Moves all files from subdirectories into the root of the specified folder.
    Resolves the path relative to AI_File_Testing.
    """
    # First validate that the target folder is within AGENT_ROOT_DIR
    folder_path = input_str.strip().strip("'\"")
    is_safe, message = validate_file_operation(
        operation="read",  # We need read access to scan the directory
        target_path=folder_path,
    )

    if not is_safe:
        console.print(f"[bold red]❌ Security check failed:[/bold red] {message}")
        return f"Security error: {message}"

    try:
        # If safe, resolve the path
        folder_path = resolve_path(folder_path)

        console.print(
            f"[bold green]📁 Target folder resolved to:[/bold green] {folder_path}"
        )

        if not os.path.exists(folder_path):
            console.print(
                f"[bold red]❌ Folder does not exist:[/bold red] {folder_path}"
            )
            return f"Folder not found: {folder_path}"

        # Validate that it's a directory
        if not os.path.isdir(folder_path):
            console.print(f"[bold red]❌ Not a directory:[/bold red] {folder_path}")
            return f"Not a directory: {folder_path}"

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

                # Validate the move operation for both source and destination
                rel_src_path = os.path.relpath(src_path, AGENT_ROOT_DIR)
                rel_dst_path = os.path.relpath(dst_path, AGENT_ROOT_DIR)

                # Debug logging
                console.print(f"[blue]Debug - Source path:[/blue]")
                console.print(f"  Original: {src_path}")
                console.print(f"  Relative to AI_File_Testing: {rel_src_path}")
                console.print(f"[blue]Debug - Destination path:[/blue]")
                console.print(f"  Original: {dst_path}")
                console.print(f"  Relative to AI_File_Testing: {rel_dst_path}")

                is_safe_src, msg_src = validate_file_operation(
                    operation="read", target_path=rel_src_path
                )
                is_safe_dst, msg_dst = validate_file_operation(
                    operation="write", target_path=rel_dst_path
                )

                if not is_safe_src:
                    console.print(
                        f"[red]⚠️ Security check failed for source:[/red] {msg_src}"
                    )
                    errors += 1
                    continue

                if not is_safe_dst:
                    console.print(
                        f"[red]⚠️ Security check failed for destination:[/red] {msg_dst}"
                    )
                    errors += 1
                    continue

                try:
                    shutil.move(src_path, dst_path)
                    console.print(f"[cyan]📦 Moved:[/cyan] {src_path} → {dst_path}")
                    moved_files += 1
                except Exception as e:
                    console.print(
                        f"[red]⚠️ Error moving {src_path} → {dst_path}: {e}[/red]"
                    )
                    errors += 1

        return (
            f"Flattened: {folder_path} — "
            f"{moved_files} files moved, {conflicts} renamed, "
            f"{errors} errors."
        )

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        console.print(f"[bold red]❌ {error_msg}[/bold red]")
        return error_msg


# ToolLoader-compatible export
tool = Tool(
    name="FolderFlattener",
    func=flatten_and_clean_folders,
    description=(
        "Moves all files from subfolders to the root folder within AI_File_Testing. "
        "Avoids overwriting by renaming files if necessary. "
        "Use with a relative path like '2023' or '' for root."
    ),
)
