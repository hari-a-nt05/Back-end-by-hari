import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from app.core.constants import (
    ERROR_LOG_FILE_NAME,
    LOG_FILE_NAME,
    LOG_LEVEL,
    LOG_TO_FILE,
)


def setup_logger(name: str = "app") -> logging.Logger:
    log_level = LOG_LEVEL
    numeric_level = getattr(logging, log_level, logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)

    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if LOG_TO_FILE is True:
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        # Read file names from env or use defaults
        main_log_name = LOG_FILE_NAME
        error_log_name = ERROR_LOG_FILE_NAME

        # Main log file handler
        file_handler = TimedRotatingFileHandler(
            filename=log_dir / main_log_name,
            when="midnight",
            interval=1,
            backupCount=7,
            utc=True,
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Error-only file handler
        error_handler = TimedRotatingFileHandler(
            filename=log_dir / error_log_name,
            when="midnight",
            interval=1,
            backupCount=14,
            utc=True,
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)

    return logger
