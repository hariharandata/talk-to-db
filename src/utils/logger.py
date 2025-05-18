import logging
import sys
from pathlib import Path


def setup_logger(name: str, log_file: Path = None) -> logging.Logger:
    """
    Set up a logger with console and optional file handlers.

    Args:
        name (str): Name of the logger.
        log_file (Path, optional): Path to the log file. If None, only console logging is set.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set base level to DEBUG (lowest, capture all)

    # Formatter (same for all handlers)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-8s - %(message)s - %(name)s:%(lineno)d",
        datefmt="%Y-%m-%dT%H:%M:%S.%f",
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # Only INFO and above to console
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # Optional: File Handler
    if log_file:
        file_handler = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)  # Capture everything to the file
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Avoid duplicated handlers if the logger is called multiple times
    logger.propagate = False

    return logger
