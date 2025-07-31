import os
import shutil
import datetime
from rich import print
from utils.path_utils import resolve_path, AGENT_ROOT_DIR
from utils.file_safety import validate_file_operation
from langchain.tools import Tool


def organize_music_by_year(input_str: str = "") -> str:
    """
    Organizes files in a folder by year of modification.
    Accepts a relative path inside AI_File_Testing (e.g., '2023', 'grabaciones', '').
    """
    # First validate that the target folder is within AGENT_ROOT_DIR
    folder_path = input_str.strip().strip("'\"")
    is_safe, message = validate_file_operation(
        operation="read",  # We need read access to scan the directory
        target_path=folder_path,
    )

    if not is_safe:
        print(f"[bold red]❌ Error de seguridad:[/bold red] {message}")
        return f"Error de seguridad: {message}"

    try:
        # If safe, resolve the path
        folder_path = resolve_path(folder_path)

        print(f"[blue]📂 Usando ruta:[/] {folder_path}")

        if not os.path.exists(folder_path):
            print(f"[red]Ruta no encontrada:[/] {folder_path}")
            return f"Ruta no encontrada: {folder_path}"

        # Validate that it's a directory
        if not os.path.isdir(folder_path):
            print(f"[red]No es un directorio:[/] {folder_path}")
            return f"No es un directorio: {folder_path}"

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                try:
                    # Get paths relative to AGENT_ROOT_DIR for validation
                    rel_src_path = os.path.relpath(file_path, AGENT_ROOT_DIR)

                    # Debug logging
                    print(f"[blue]Debug - Archivo:[/blue]")
                    print(f"  Original: {file_path}")
                    print(f"  Relativo a AI_File_Testing: {rel_src_path}")

                    # Validate read access to source file
                    is_safe_src, msg_src = validate_file_operation(
                        operation="read", target_path=rel_src_path
                    )

                    if not is_safe_src:
                        print(f"[red]⚠️ Error de seguridad en origen:[/red] {msg_src}")
                        continue

                    # Get modification time and year
                    mod_time = os.path.getmtime(file_path)
                    year = datetime.datetime.fromtimestamp(mod_time).year

                    # Create and validate year folder
                    year_folder = os.path.join(folder_path, str(year))
                    os.makedirs(year_folder, exist_ok=True)

                    # Get destination path and validate
                    dst_path = os.path.join(year_folder, file)
                    rel_dst_path = os.path.relpath(dst_path, AGENT_ROOT_DIR)

                    print(f"[blue]Debug - Destino:[/blue]")
                    print(f"  Original: {dst_path}")
                    print(f"  Relativo a AI_File_Testing: {rel_dst_path}")

                    # Validate write access to destination
                    is_safe_dst, msg_dst = validate_file_operation(
                        operation="write", target_path=rel_dst_path
                    )

                    if not is_safe_dst:
                        print(f"[red]⚠️ Error de seguridad en destino:[/red] {msg_dst}")
                        continue

                    # If all validations pass, perform the move
                    shutil.move(file_path, dst_path)
                    print(f"[green]✔️ {file} → {year_folder}[/]")

                except Exception as e:
                    print(f"[red]❌ Error al procesar {file}: {e}[/]")

        return f"[bold green]Organización completada en[/] {folder_path}"

    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        print(f"[bold red]❌ {error_msg}[/bold red]")
        return error_msg


# ToolLoader-compatible export
tool = Tool(
    name="OrganizadorMúsicaPorAño",
    func=organize_music_by_year,
    description=(
        "Organiza archivos en una carpeta agrupándolos por año de modificación. "
        "Úsalo con un path relativo como '2023' o '' para la raíz de AI_File_Testing."
    ),
)
