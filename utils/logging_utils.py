import logging
import os
from datetime import datetime
from typing import Optional
from utils.path_utils import AGENT_ROOT_DIR

# Configure logs directory
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Create log filename with date
log_file = os.path.join(
    LOGS_DIR, f"file_operations_{datetime.now().strftime('%Y%m%d')}.log"
)

# Configure main logger
logger = logging.getLogger("file_operations")
logger.setLevel(logging.INFO)

# Configure log format
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# File handler
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def log_file_operation(
    operation: str,
    path: str,
    success: bool,
    details: Optional[str] = None,
    error: Optional[Exception] = None,
) -> None:
    """
    Logs a file operation to the log file.

    Args:
        operation: Type of operation (CREATE, READ, UPDATE, DELETE, MOVE, etc.)
        path: Path of the affected file
        success: Whether the operation was successful
        details: Additional operation details
        error: Exception if an error occurred
    """
    # Ensure path is relative to AGENT_ROOT_DIR
    try:
        relative_path = os.path.relpath(path, AGENT_ROOT_DIR)
    except ValueError:
        relative_path = path  # If path is outside AGENT_ROOT_DIR

    # Build base message
    msg = f"{operation} - Path: {relative_path}"

    # Add details if they exist
    if details:
        msg += f" - Details: {details}"

    # Log based on result
    if success:
        logger.info(f"✅ {msg}")
    else:
        error_msg = f" - Error: {str(error)}" if error else ""
        logger.error(f"❌ {msg}{error_msg}")


def log_security_event(
    event_type: str, description: str, severity: str = "INFO"
) -> None:
    """
    Logs a security-related event.

    Args:
        event_type: Type of security event
        description: Detailed description of the event
        severity: Event severity level (default: INFO)
    """
    logger.log(
        getattr(logging, severity.upper(), logging.INFO),
        f"🔒 Security Event - {event_type}: {description}",
    )
