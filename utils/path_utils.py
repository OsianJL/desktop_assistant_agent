import os

DEFAULT_FOLDER_BASE = "/mnt/c/Users/osian/Desktop"

def resolve_path(target_folder: str) -> str:
    """
    Converts a relative folder name into an absolute path using DEFAULT_FOLDER_BASE.
    If the input is already absolute, returns it unchanged.
    """
    return target_folder if os.path.isabs(target_folder) else os.path.join(DEFAULT_FOLDER_BASE, target_folder)
