import logging
import sys
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler

from settings import settings


def setup_logging(
    log_file: str = "cluedogpt.log",
    console_level: str = "INFO",
    file_level: str = "INFO",
    max_bytes: int = 10 * 1024 * 1024,  # 10 MB
    backup_count: int = 5,
) -> None:
    """
    Configure logging with console and rotating file handlers.

    - Console: prints to stdout with configurable level (default INFO)
    - Rotating file: writes to log_file with configurable level, rotates at max_bytes, keeps backup_count files
    """
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": console_level,
                "formatter": "standard",
                "stream": sys.stdout,
            },
            "rotating_file": {
                "()": RotatingFileHandler,
                "level": file_level,
                "formatter": "standard",
                "filename": log_file,
                "mode": "a",
                "encoding": "utf-8",
                "maxBytes": max_bytes,
                "backupCount": backup_count,
            },
        },
        "root": {
            "handlers": ["console", "rotating_file"],
            "level": console_level,
        },
    }

    dictConfig(log_config)


def initialize_logging_from_settings():
    """Initialize logging using settings from the environment."""
    # Import here to avoid circular imports

    setup_logging(
        console_level=settings().console_log_level,
        file_level=settings().file_log_level,
    )


# Initialize with default settings on import
setup_logging()

# Export logger for application use
logger = logging.getLogger("cluedogpt")
