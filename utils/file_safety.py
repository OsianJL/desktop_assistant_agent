import os
import magic
from typing import List, Optional, Tuple
from utils.path_utils import AGENT_ROOT_DIR, resolve_path

# Define safe file types and their magic numbers/MIME types
SAFE_FILE_TYPES = {
    "audio": [
        "audio/mpeg",  # MP3
        "audio/wav",  # WAV
        "audio/x-wav",  # WAV alternative
        "audio/flac",  # FLAC
        "audio/ogg",  # OGG
        "audio/x-m4a",  # M4A
    ],
    "document": [
        "text/plain",  # TXT
        "application/pdf",  # PDF
        "application/json",  # JSON
    ],
}

# Maximum file size (in bytes) - default 500MB
MAX_FILE_SIZE = 500 * 1024 * 1024


def validate_file_operation(
    operation: str,
    target_path: str,
    allowed_types: Optional[List[str]] = None,
    max_size: Optional[int] = None,
) -> Tuple[bool, str]:
    """
    Validates a file operation for safety.

    Args:
        operation: The operation to perform ('read', 'write', 'delete', 'move')
        target_path: The path to validate
        allowed_types: List of allowed file type categories from SAFE_FILE_TYPES
        max_size: Maximum allowed file size in bytes

    Returns:
        Tuple[bool, str]: (is_safe, message)
        - is_safe: True if operation is safe, False otherwise
        - message: Description of why operation was denied, or 'OK' if safe
    """
    try:
        # 1. Basic path validation
        full_path = resolve_path(target_path)

        # 2. Check if path exists (for operations that require existing files)
        if operation in ["read", "delete", "move"]:
            if not os.path.exists(full_path):
                return False, f"Path does not exist: {target_path}"

        # 3. Check if path is within AGENT_ROOT_DIR (redundant with resolve_path but explicit)
        if not os.path.commonpath([AGENT_ROOT_DIR, full_path]) == AGENT_ROOT_DIR:
            return (
                False,
                f"Access denied outside AI_File_Testing directory: {target_path}",
            )

        # 4. For existing files, validate file type if specified
        if os.path.exists(full_path) and allowed_types:
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(full_path)

            allowed_mime_types = []
            for type_category in allowed_types:
                if type_category in SAFE_FILE_TYPES:
                    allowed_mime_types.extend(SAFE_FILE_TYPES[type_category])

            if file_type not in allowed_mime_types:
                return (
                    False,
                    f"File type {file_type} not allowed. Allowed types: {', '.join(allowed_types)}",
                )

        # 5. Check file size for existing files
        if os.path.exists(full_path):
            file_size = os.path.getsize(full_path)
            size_limit = max_size if max_size is not None else MAX_FILE_SIZE

            if file_size > size_limit:
                return (
                    False,
                    f"File size {file_size} bytes exceeds limit of {size_limit} bytes",
                )

        # 6. Operation-specific checks
        if operation == "write":
            # Check if parent directory exists
            parent_dir = os.path.dirname(full_path)
            if not os.path.exists(parent_dir):
                return False, f"Parent directory does not exist: {parent_dir}"

            # Check if we have write permission to parent directory
            if not os.access(parent_dir, os.W_OK):
                return False, f"No write permission to directory: {parent_dir}"

        elif operation == "read":
            if not os.access(full_path, os.R_OK):
                return False, f"No read permission for file: {target_path}"

        elif operation == "delete":
            if not os.access(full_path, os.W_OK):
                return False, f"No delete permission for file: {target_path}"

            # Extra safety: don't delete directories unless empty
            if os.path.isdir(full_path) and os.listdir(full_path):
                return False, f"Cannot delete non-empty directory: {target_path}"

        return True, "OK"

    except Exception as e:
        return False, f"Validation error: {str(e)}"


def is_safe_file_operation(
    operation: str,
    target_path: str,
    allowed_types: Optional[List[str]] = None,
    max_size: Optional[int] = None,
) -> bool:
    """
    Convenience wrapper that returns just the boolean result of validate_file_operation.
    """
    is_safe, _ = validate_file_operation(
        operation, target_path, allowed_types, max_size
    )
    return is_safe
