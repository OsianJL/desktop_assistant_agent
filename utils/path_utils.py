import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Get and validate AGENT_ROOT_DIR
_agent_root: Optional[str] = os.getenv("AGENT_ROOT_DIR")
if not _agent_root:
    raise ValueError("AGENT_ROOT_DIR must be set in .env file")

# Convert to absolute path and validate
AGENT_ROOT_DIR: str = os.path.abspath(_agent_root)
if not os.path.exists(AGENT_ROOT_DIR):
    raise ValueError(f"AGENT_ROOT_DIR does not exist: {AGENT_ROOT_DIR}")

if not os.path.isdir(AGENT_ROOT_DIR):
    raise ValueError(f"AGENT_ROOT_DIR is not a directory: {AGENT_ROOT_DIR}")


def resolve_path(relative_path: str) -> str:
    """
    Resolves a relative path inside AGENT_ROOT_DIR and ensures no access outside is allowed.

    Args:
        relative_path (str): File or folder path relative to AGENT_ROOT_DIR.
            If empty, returns AGENT_ROOT_DIR itself.

    Returns:
        str: Absolute path within AGENT_ROOT_DIR.

    Raises:
        ValueError: If path resolves outside of AGENT_ROOT_DIR.
    """
    # If path is empty or just whitespace, return AGENT_ROOT_DIR
    if not relative_path or relative_path.strip() == "":
        return AGENT_ROOT_DIR

    # Normalize path to handle any '..' or '.' components
    normalized_path = os.path.normpath(relative_path)

    # Create absolute path
    full_path = os.path.abspath(os.path.join(AGENT_ROOT_DIR, normalized_path))

    # Prevent path traversal by comparing common path prefix
    if os.path.commonpath([AGENT_ROOT_DIR, full_path]) != AGENT_ROOT_DIR:
        raise ValueError(f"Access denied outside agent directory: {full_path}")

    return full_path
