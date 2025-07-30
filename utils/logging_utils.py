import logging
import os
from datetime import datetime
from typing import Optional
from utils.path_utils import AGENT_ROOT_DIR

# Configurar el directorio de logs
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Crear el nombre del archivo de log con la fecha
log_file = os.path.join(
    LOGS_DIR, f"file_operations_{datetime.now().strftime('%Y%m%d')}.log"
)

# Configurar el logger principal
logger = logging.getLogger("file_operations")
logger.setLevel(logging.INFO)

# Configurar el formato del log
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

# Handler para archivo
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Handler para consola
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
    Registra una operación de archivo en el log.

    Args:
        operation: Tipo de operación (CREATE, READ, UPDATE, DELETE, MOVE, etc.)
        path: Ruta del archivo afectado
        success: Si la operación fue exitosa
        details: Detalles adicionales de la operación
        error: Excepción si ocurrió un error
    """
    # Asegurarse de que la ruta es relativa a AGENT_ROOT_DIR
    try:
        relative_path = os.path.relpath(path, AGENT_ROOT_DIR)
    except ValueError:
        relative_path = path  # Si la ruta está fuera de AGENT_ROOT_DIR

    # Construir el mensaje base
    msg = f"{operation} - Path: {relative_path}"

    # Añadir detalles si existen
    if details:
        msg += f" - Details: {details}"

    # Log según el resultado
    if success:
        logger.info(f"✅ {msg}")
    else:
        error_msg = f" - Error: {str(error)}" if error else ""
        logger.error(f"❌ {msg}{error_msg}")


def log_security_event(
    event_type: str, description: str, severity: str = "INFO"
) -> None:
    """
    Registra un evento de seguridad en el log.

    Args:
        event_type: Tipo de evento de seguridad
        description: Descripción del evento
        severity: Nivel de severidad (INFO, WARNING, ERROR)
    """
    level = getattr(logging, severity.upper())
    logger.log(level, f"🔒 SECURITY - {event_type} - {description}")
