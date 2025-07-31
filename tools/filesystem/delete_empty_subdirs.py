import os
from rich.console import Console
from utils.path_utils import resolve_path, AGENT_ROOT_DIR
from utils.file_safety import validate_file_operation
from langchain.tools import Tool

console = Console()


def delete_empty_subdirs(input_str: str = "") -> str:
    """
    Deletes empty subdirectories within the specified folder.
    Only operates within AI_File_Testing directory.
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

        console.print(f"[blue]📂 Target folder:[/blue] {folder_path}")

        if not os.path.exists(folder_path):
            console.print(
                f"[bold red]❌ Folder does not exist:[/bold red] {folder_path}"
            )
            return f"Folder not found: {folder_path}"

        # Validate that it's a directory
        if not os.path.isdir(folder_path):
            console.print(f"[bold red]❌ Not a directory:[/bold red] {folder_path}")
            return f"Not a directory: {folder_path}"

        deleted_folders = 0
        errors = 0

        for root, _, _ in os.walk(folder_path, topdown=False):
            if root == folder_path:
                continue  # Never delete root folder

            try:
                # Get path relative to AGENT_ROOT_DIR for validation
                rel_path = os.path.relpath(root, AGENT_ROOT_DIR)

                # Debug logging
                console.print(f"[blue]Debug - Checking directory:[/blue]")
                console.print(f"  Original: {root}")
                console.print(f"  Relative to AI_File_Testing: {rel_path}")

                # Validate delete access
                is_safe_delete, msg_delete = validate_file_operation(
                    operation="delete",
                    target_path=rel_path,
                )

                if not is_safe_delete:
                    console.print(
                        f"[red]⚠️ Security check failed for deletion:[/red] {msg_delete}"
                    )
                    errors += 1
                    continue

                # Check if directory is empty
                if not os.listdir(root):
                    os.rmdir(root)
                    console.print(f"[green]🗑️ Deleted empty folder:[/green] {root}")
                    deleted_folders += 1

            except Exception as e:
                console.print(f"[red]⚠️ Error processing folder {root}: {e}[/red]")
                errors += 1

        return f"🧹 Deleted {deleted_folders} empty folders. Errors: {errors}."

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        console.print(f"[bold red]❌ {error_msg}[/bold red]")
        return error_msg


# ToolLoader-compatible export
tool = Tool(
    name="EmptyFolderCleaner",
    func=delete_empty_subdirs,
    description=(
        "Deletes empty subfolders within a folder relative to AI_File_Testing. "
        "For example: '2024', 'music', or just '' for root."
    ),
)
