import os

AGENT_ROOT_DIR = "/mnt/c/Users/osian/Desktop/AI_File_Testing"

def resolve_path(relative_path: str) -> str:
    """
    Resolves a relative path inside AGENT_ROOT_DIR and ensures no access outside is allowed.
    
    Args:
        relative_path (str): File or folder path relative to AGENT_ROOT_DIR.
    
    Returns:
        str: Absolute path within AGENT_ROOT_DIR.
    
    Raises:
        ValueError: If path resolves outside of AGENT_ROOT_DIR.
    """
    full_path = os.path.abspath(os.path.join(AGENT_ROOT_DIR, relative_path))

    # Prevent path traversal
    if not os.path.commonpath([AGENT_ROOT_DIR, full_path]) == AGENT_ROOT_DIR:
        raise ValueError(f"Access denied outside agent directory: {full_path}")

    return full_path
