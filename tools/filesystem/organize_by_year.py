import os
import shutil
import datetime
from rich import print
from utils.path_utils import resolve_path  # 👈 nuevo import

def organize_music_by_year(folder_name_or_path: str) -> str:
    folder_path = resolve_path(folder_name_or_path)  # 👈 ruta resuelta automáticamente

    if not os.path.exists(folder_path):
        return f"[red]Ruta no encontrada:[/] {folder_path}"

    print(f"[blue]📂 Usando ruta:[/] {folder_path}")

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            try:
                mod_time = os.path.getmtime(file_path)
                year = datetime.datetime.fromtimestamp(mod_time).year
            except Exception as e:
                print(f"[yellow]Error al obtener fecha de {file}: {e}[/]")
                continue

            year_folder = os.path.join(folder_path, str(year))
            os.makedirs(year_folder, exist_ok=True)

            try:
                shutil.move(file_path, os.path.join(year_folder, file))
                print(f"[green]✔️ {file} → {year_folder}[/]")
            except Exception as e:
                print(f"[red]❌ Error al mover {file}: {e}[/]")

    return f"[bold green]Organización completada en[/] {folder_path}"
